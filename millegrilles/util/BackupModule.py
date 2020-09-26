import logging
import datetime
import pytz
import json
import lzma
import hashlib
import requests

from os import path
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from base64 import b64encode

from millegrilles import Constantes
from millegrilles.Constantes import ConstantesBackup, ConstantesPki
from millegrilles.util.JSONMessageEncoders import BackupFormatEncoder, DateFormatEncoder, decoder_backup
from millegrilles.SecuritePKI import HachageInvalide, CertificatInvalide
from millegrilles.util.X509Certificate import EnveloppeCleCert
from millegrilles.util.Chiffrage import CipherMsg1Chiffrer


class HandlerBackupDomaine:
    """
    Gestionnaire de backup des transactions d'un domaine.
    """

    def __init__(self, contexte, nom_domaine, nom_collection_transactions, nom_collection_documents,
                 niveau_securite=Constantes.SECURITE_PROTEGE):
        self._contexte = contexte
        self.__logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

        self._nom_domaine = nom_domaine
        self._nom_collection_transactions = nom_collection_transactions
        self._nom_collection_documents = nom_collection_documents
        self.__niveau_securite = niveau_securite

    def backup_domaine(self, heure: datetime.datetime, entete_backup_precedent: dict, info_cles: dict):
        """

        :param heure: Heure du backup horaire
        :param entete_backup_precedent: Entete du catalogue precedent, sert a creer une chaine de backups (merkle tree)
        :param info_cles: Reponse de requete ConstantesMaitreDesCles.REQUETE_CERT_MAITREDESCLES
        :return:
        """
        debut_backup = heure
        niveau_securite = Constantes.SECURITE_PROTEGE  # A FAIRE : supporter differents niveaux

        self.transmettre_evenement_backup(ConstantesBackup.EVENEMENT_BACKUP_HORAIRE_DEBUT, debut_backup)

        curseur = self._effectuer_requete_domaine(heure)

        # Utilise pour creer une chaine entre backups horaires
        chainage_backup_precedent = None
        if entete_backup_precedent:
            chainage_backup_precedent = {
                Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID: entete_backup_precedent[Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID],
                ConstantesBackup.LIBELLE_HACHAGE_ENTETE: self.calculer_hash_entetebackup(entete_backup_precedent)
            }

        heures_sous_domaines = dict()

        heure_plusvieille = heure

        for transanter in curseur:
            self.__logger.debug("Vieille transaction : %s" % str(transanter))
            heure_anterieure = pytz.utc.localize(transanter['_id']['timestamp'])
            for sous_domaine_gr in transanter['sousdomaine']:
                sous_domaine = '.'.join(sous_domaine_gr)

                # Conserver l'heure la plus vieille dans ce backup
                # Permet de declencher backup quotidiens anterieurs
                heure_plusvieille = heures_sous_domaines.get(sous_domaine)
                if heure_plusvieille is None or heure_plusvieille > heure_anterieure:
                    heure_plusvieille = heure_anterieure
                    heures_sous_domaines[sous_domaine] = heure_anterieure

                # Creer le fichier de backup
                dependances_backup = self._backup_horaire_domaine(
                    self._nom_collection_transactions,
                    sous_domaine,
                    heure_anterieure,
                    chainage_backup_precedent,
                    info_cles
                )

                catalogue_backup = dependances_backup.get('catalogue')
                if catalogue_backup is not None:
                    self.transmettre_evenement_backup(
                        ConstantesBackup.EVENEMENT_BACKUP_HORAIRE_CATALOGUE_PRET, debut_backup, niveau_securite)

                    hachage_entete = self.calculer_hash_entetebackup(catalogue_backup[Constantes.TRANSACTION_MESSAGE_LIBELLE_EN_TETE])
                    uuid_transaction_catalogue = catalogue_backup[Constantes.TRANSACTION_MESSAGE_LIBELLE_EN_TETE][Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID]

                    path_fichier_transactions = dependances_backup['path_fichier_backup']
                    nom_fichier_transactions = path.basename(path_fichier_transactions)

                    path_fichier_catalogue = dependances_backup['path_catalogue']
                    nom_fichier_catalogue = path.basename(path_fichier_catalogue)

                    self.__logger.debug("Information fichier backup:\n%s" % json.dumps(dependances_backup, indent=4, cls=BackupFormatEncoder))

                    # Transferer vers consignation_fichier
                    data = {
                        'timestamp_backup': int(heure_anterieure.timestamp()),
                        'fuuid_grosfichiers': json.dumps(catalogue_backup['fuuid_grosfichiers']),
                    }
                    transaction_maitredescles = dependances_backup.get('transaction_maitredescles')
                    if transaction_maitredescles is not None:
                        data['transaction_maitredescles'] = json.dumps(transaction_maitredescles)

                    # Preparer URL de connexion a consignationfichiers
                    url_consignationfichiers = 'https://%s:%s' % (
                        self._contexte.configuration.serveur_consignationfichiers_host,
                        self._contexte.configuration.serveur_consignationfichiers_port
                    )

                    with open(path_fichier_transactions, 'rb') as transactions_fichier:
                        with open(path_fichier_catalogue, 'rb') as catalogue_fichier:
                            files = {
                                'transactions': (nom_fichier_transactions, transactions_fichier, 'application/x-xz'),
                                'catalogue': (nom_fichier_catalogue, catalogue_fichier, 'application/x-xz'),
                            }

                            certfile = self._contexte.configuration.mq_certfile
                            keyfile = self._contexte.configuration.mq_keyfile

                            r = requests.put(
                                '%s/backup/domaine/%s' % (url_consignationfichiers, nom_fichier_catalogue),
                                data=data,
                                files=files,
                                verify=self._contexte.configuration.mq_cafile,
                                cert=(certfile, keyfile)
                            )

                    if r.status_code == 200:
                        self.transmettre_evenement_backup(
                            ConstantesBackup.EVENEMENT_BACKUP_HORAIRE_UPLOAD_CONFIRME, debut_backup, niveau_securite)

                        reponse_json = json.loads(r.text)
                        self.__logger.debug("Reponse backup\nHeaders: %s\nData: %s" % (r.headers, str(reponse_json)))

                        # Verifier si le SHA512 du fichier de backup recu correspond a celui calcule localement
                        if reponse_json['fichiersDomaines'][nom_fichier_transactions] != \
                                catalogue_backup[ConstantesBackup.LIBELLE_TRANSACTIONS_HACHAGE]:
                            raise ValueError(
                                "Le SHA512 du fichier de backup de transactions ne correspond pas a celui recu de consignationfichiers")

                        # Transmettre la transaction au domaine de backup
                        # L'enveloppe est deja prete, on fait juste l'emettre
                        self._contexte.message_dao.transmettre_nouvelle_transaction(catalogue_backup, None, None)

                        # Marquer les transactions comme inclue dans le backup
                        liste_uuids = dependances_backup['uuid_transactions']
                        self.marquer_transactions_backup_complete(self._nom_collection_transactions, liste_uuids)

                        transaction_sha512_catalogue = {
                            ConstantesBackup.LIBELLE_DOMAINE: sous_domaine,
                            ConstantesBackup.LIBELLE_SECURITE: dependances_backup['catalogue'][ConstantesBackup.LIBELLE_SECURITE],
                            ConstantesBackup.LIBELLE_HEURE: int(heure_anterieure.timestamp()),
                            ConstantesBackup.LIBELLE_CATALOGUE_HACHAGE: dependances_backup[ConstantesBackup.LIBELLE_CATALOGUE_HACHAGE],
                            ConstantesBackup.LIBELLE_HACHAGE_ENTETE: hachage_entete,
                            Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID: uuid_transaction_catalogue,
                        }

                        self._contexte.generateur_transactions.soumettre_transaction(
                            transaction_sha512_catalogue, ConstantesBackup.TRANSACTION_CATALOGUE_HORAIRE_HACHAGE)

                    else:
                        raise Exception("Reponse %d sur upload backup %s" % (r.status_code, nom_fichier_catalogue))

                    # Calculer nouvelle entete
                    entete_backup_precedent = catalogue_backup[Constantes.TRANSACTION_MESSAGE_LIBELLE_EN_TETE]
                    chainage_backup_precedent = {
                        Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID: entete_backup_precedent[
                            Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID],
                        ConstantesBackup.LIBELLE_HACHAGE_ENTETE: hachage_entete
                    }

                else:
                    self.__logger.warning(
                        "Aucune transaction valide inclue dans le backup de %s a %s mais transactions en erreur presentes" % (
                            self._nom_collection_transactions, str(heure_anterieure))
                    )

                # Traiter les transactions invalides
                liste_uuids_invalides = dependances_backup.get('liste_uuids_invalides')
                if liste_uuids_invalides and len(liste_uuids_invalides) > 0:
                    self.__logger.error(
                        "Marquer %d transactions invalides exclue du backup de %s a %s" % (
                            len(liste_uuids_invalides), self._nom_collection_transactions, str(heure_anterieure))
                    )
                    self.marquer_transactions_invalides(self._nom_collection_transactions, liste_uuids_invalides)

        self.transmettre_evenement_backup(ConstantesBackup.EVENEMENT_BACKUP_HORAIRE_TERMINE, debut_backup, niveau_securite)

        self.transmettre_trigger_jour_precedent(heure_plusvieille)

    def _effectuer_requete_domaine(self, heure: datetime.datetime):
        # Verifier s'il y a des transactions qui n'ont pas ete traitees avant la periode actuelle
        idmg = self._contexte.idmg

        filtre_verif_transactions_anterieures = {
            '_evenements.transaction_complete': True,
            '_evenements.%s' % Constantes.EVENEMENT_TRANSACTION_BACKUP_FLAG: False,
            '_evenements.transaction_traitee': {'$lt': heure},
        }
        regroupement_periode = {
            'year': {'$year': '$_evenements.transaction_traitee'},
            'month': {'$month': '$_evenements.transaction_traitee'},
            'day': {'$dayOfMonth': '$_evenements.transaction_traitee'},
            'hour': {'$hour': '$_evenements.transaction_traitee'},
        }

        # Regroupeemnt par date et par domaine/sous-domaine (l'action est retiree du domaine pour grouper)
        regroupement = {
            '_id': {
                'timestamp': {
                    '$dateFromParts': regroupement_periode
                },
            },
            'sousdomaine': {
                '$addToSet': {
                    '$slice': [
                        {'$split': ['$en-tete.domaine', '.']},
                        {'$add': [{'$size': {'$split': ['$en-tete.domaine', '.']}}, -1]}
                    ]
                }
            }
        }
        sort = {
            '_id.timestamp': 1,
            # 'sousdomaine': 1
        }
        operation = [
            {'$match': filtre_verif_transactions_anterieures},
            {'$group': regroupement},
            {'$sort': sort},
        ]
        hint = {
            '_evenements.transaction_complete': 1,
            '_evenements.%s' % Constantes.EVENEMENT_TRANSACTION_BACKUP_FLAG: 1,
        }
        collection_transactions = self._contexte.document_dao.get_collection(self._nom_collection_transactions)

        return collection_transactions.aggregate(operation, hint=hint)

    def _backup_horaire_domaine(self, nom_collection_mongo: str, sous_domaine: str, heure: datetime,
                                chainage_backup_precedent: dict,
                                info_cles: dict) -> dict:
        heure_str = heure.strftime("%Y%m%d%H")
        heure_fin = heure + datetime.timedelta(hours=1)
        self.__logger.debug("Backup collection %s entre %s et %s" % (nom_collection_mongo, heure, heure_fin))

        prefixe_fichier = sous_domaine

        curseur = self.preparer_curseur_transactions(nom_collection_mongo, sous_domaine)

        # Creer repertoire backup et determiner path fichier
        backup_workdir = self._contexte.configuration.backup_workdir
        Path(backup_workdir).mkdir(mode=0o700, parents=True, exist_ok=True)

        # Determiner si on doit chiffrer le fichier de transactions
        chiffrer_transactions = self.__niveau_securite in [Constantes.SECURITE_PROTEGE, Constantes.SECURITE_SECURE]

        # Nom fichier transactions avec .jsonl, indique que chaque ligne est un message JSON
        if chiffrer_transactions:
            # Fichier va etre chiffre en format mgs1
            extension_transactions = 'jsonl.xz.mgs1'
        else:
            extension_transactions = 'jsonl.xz'

        backup_nomfichier = '%s_transactions_%s_%s.%s' % (prefixe_fichier, heure_str, self.__niveau_securite, extension_transactions)
        path_fichier_backup = path.join(backup_workdir, backup_nomfichier)

        catalogue_nomfichier = '%s_catalogue_%s_%s.json.xz' % (prefixe_fichier, heure_str, self.__niveau_securite)

        catalogue_backup = self.preparer_catalogue(backup_nomfichier, catalogue_nomfichier, chainage_backup_precedent,
                                                   heure, sous_domaine)

        liste_uuid_transactions = list()
        liste_uuids_invalides = list()
        info_backup = {
            'path_fichier_backup': path_fichier_backup,
            'uuid_transactions': liste_uuid_transactions,
            'liste_uuids_invalides': liste_uuids_invalides,
        }

        cles_set = ['certificats_racine', 'certificats_intermediaires', 'certificats', 'fuuid_grosfichiers']

        # Preparer chiffrage, cle
        if chiffrer_transactions:
            cipher, transaction_maitredescles = self.preparer_cipher(catalogue_backup, info_cles)

            # Inserer la transaction de maitre des cles dans l'info backup pour l'uploader avec le PUT
            info_backup['transaction_maitredescles'] = self._contexte.generateur_transactions.preparer_enveloppe(
                transaction_maitredescles,
                Constantes.ConstantesMaitreDesCles.TRANSACTION_NOUVELLE_CLE_BACKUPTRANSACTIONS
            )

        else:
            # Pas de chiffrage
            cipher = None

        with open(path_fichier_backup, 'wb') as fichier:
            lzma_compressor = lzma.LZMACompressor()

            if cipher is not None:
                fichier.write(cipher.start_encrypt())

            for transaction in curseur:
                uuid_transaction = transaction[Constantes.TRANSACTION_MESSAGE_LIBELLE_EN_TETE][Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID]
                try:
                    # Extraire metadonnees de la transaction
                    info_transaction = self._traiter_transaction(transaction, heure)
                    for cle in cles_set:
                        try:
                            catalogue_backup[cle].update(info_transaction[cle])
                        except KeyError:
                            pass

                    tran_json = json.dumps(transaction, sort_keys=True, ensure_ascii=True, cls=BackupFormatEncoder)
                    if cipher is not None:
                        fichier.write(cipher.update(lzma_compressor.compress(tran_json.encode('utf-8'))))
                    else:
                        fichier.write(lzma_compressor.compress(tran_json.encode('utf-8')))

                    # Une transaction par ligne
                    if cipher is not None:
                        fichier.write(cipher.update(lzma_compressor.compress(b'\n')))
                    else:
                        fichier.write(lzma_compressor.compress(b'\n'))

                    # La transaction est bonne, on l'ajoute a la liste inclue dans le backup
                    liste_uuid_transactions.append(uuid_transaction)
                except HachageInvalide:
                    self.__logger.error("Transaction hachage invalide %s: transaction exclue du backup de %s" % (uuid_transaction, nom_collection_mongo))
                    # Marquer la transaction comme invalide pour backup
                    liste_uuids_invalides.append(uuid_transaction)
                except CertificatInvalide:
                    self.__logger.error("Erreur, certificat de transaction invalide : %s" % uuid_transaction)

            if cipher is not None:
                fichier.write(cipher.update(lzma_compressor.flush()))
                fichier.write(cipher.finalize())
            else:
                fichier.write(lzma_compressor.flush())

        if len(liste_uuid_transactions) > 0:
            # Calculer SHA512 du fichier de backup des transactions
            hachage_catalogue = self.sauvegarder_catalogue(backup_nomfichier, backup_workdir, catalogue_backup,
                                                           catalogue_nomfichier, cles_set, info_backup,
                                                           path_fichier_backup)

            info_backup[ConstantesBackup.LIBELLE_CATALOGUE_HACHAGE] = hachage_catalogue

        else:
            self.__logger.info("Backup: aucune transaction, backup annule")
            info_backup = {
                'liste_uuids_invalides': liste_uuids_invalides
            }

        return info_backup

    def preparer_cipher(self, catalogue_backup, info_cles):
        """
        Prepare un objet cipher pour chiffrer le fichier de transactions

        :param catalogue_backup:
        :param info_cles: Cles publiques (certs) retournees par le maitre des cles. Utilisees pour chiffrer cle secrete.
        :return:
        """
        cipher = CipherMsg1Chiffrer()
        iv = b64encode(cipher.iv).decode('utf-8')

        # Conserver iv et cle chiffree avec cle de millegrille (restore dernier recours)
        enveloppe_millegrille = self._contexte.signateur_transactions.get_enveloppe_millegrille()
        catalogue_backup['cle'] = b64encode(cipher.chiffrer_motdepasse_enveloppe(enveloppe_millegrille)).decode('utf-8')
        catalogue_backup['iv'] = iv

        # Generer transaction pour sauvegarder les cles de ce backup avec le maitredescles
        certs_cles_backup = [
            info_cles['certificat'][0],  # Certificat de maitredescles
            info_cles['certificat_millegrille'],  # Certificat de millegrille
        ]
        certs_cles_backup.extend(info_cles['certificats_backup'].values())
        cles_chiffrees = self.chiffrer_cle(certs_cles_backup, cipher.password)
        transaction_maitredescles = {
            'domaine': self._nom_domaine,
            Constantes.ConstantesMaitreDesCles.TRANSACTION_CHAMP_IDENTIFICATEURS_DOCUMENTS: {
                ConstantesBackup.LIBELLE_TRANSACTIONS_NOMFICHIER: catalogue_backup[
                    ConstantesBackup.LIBELLE_TRANSACTIONS_NOMFICHIER]
            },
            'iv': iv,
            'cles': cles_chiffrees,
            'sujet': 'cles.backupTransactions',
        }

        return cipher, transaction_maitredescles

    def sauvegarder_catalogue(self, backup_nomfichier, backup_workdir, catalogue_backup, catalogue_nomfichier,
                              cles_set, info_backup, path_fichier_backup):
        sha512 = hashlib.sha512()
        with open(path_fichier_backup, 'rb') as fichier:
            sha512.update(fichier.read())
        sha512_digest = 'sha512_b64:' + b64encode(sha512.digest()).decode('utf-8')
        catalogue_backup[ConstantesBackup.LIBELLE_TRANSACTIONS_HACHAGE] = sha512_digest
        catalogue_backup[ConstantesBackup.LIBELLE_TRANSACTIONS_NOMFICHIER] = backup_nomfichier
        # Changer les set() par des list() pour extraire en JSON
        for cle in cles_set:
            if isinstance(catalogue_backup[cle], set):
                catalogue_backup[cle] = list(catalogue_backup[cle])
        # Generer l'entete et la signature pour le catalogue
        catalogue_json = json.dumps(catalogue_backup, sort_keys=True, ensure_ascii=True, cls=DateFormatEncoder)
        # Recharger le catalogue pour avoir le format exact (e.g. encoding dates)
        catalogue_backup = json.loads(catalogue_json)
        catalogue_backup = self._contexte.generateur_transactions.preparer_enveloppe(
            catalogue_backup, ConstantesBackup.TRANSACTION_CATALOGUE_HORAIRE, ajouter_certificats=True)
        catalogue_json = json.dumps(catalogue_backup, sort_keys=True, ensure_ascii=True, cls=DateFormatEncoder)
        info_backup['catalogue'] = catalogue_backup
        # Sauvegarder catlogue sur disque pour transferer
        path_catalogue = path.join(backup_workdir, catalogue_nomfichier)
        info_backup['path_catalogue'] = path_catalogue
        with lzma.open(path_catalogue, 'wt') as fichier:
            # Dump du catalogue en format de transaction avec DateFormatEncoder
            fichier.write(catalogue_json)
        sha512 = hashlib.sha512()
        with open(path_catalogue, 'rb') as fichier:
            sha512.update(fichier.read())
        sha512_digest = 'sha512_b64:' + b64encode(sha512.digest()).decode('utf-8')

        return sha512_digest

    def preparer_catalogue(self, backup_nomfichier, catalogue_nomfichier, chainage_backup_precedent, heure,
                           sous_domaine):
        catalogue_backup = {
            ConstantesBackup.LIBELLE_DOMAINE: sous_domaine,
            ConstantesBackup.LIBELLE_SECURITE: self.__niveau_securite,
            ConstantesBackup.LIBELLE_HEURE: heure,

            ConstantesBackup.LIBELLE_CATALOGUE_NOMFICHIER: catalogue_nomfichier,
            ConstantesBackup.LIBELLE_TRANSACTIONS_NOMFICHIER: backup_nomfichier,
            ConstantesBackup.LIBELLE_CATALOGUE_HACHAGE: None,

            # Conserver la liste des certificats racine, intermediaire et noeud necessaires pour
            # verifier toutes les transactions de ce backup
            ConstantesBackup.LIBELLE_CERTS_RACINE: set(),
            ConstantesBackup.LIBELLE_CERTS_INTERMEDIAIRES: set(),
            ConstantesBackup.LIBELLE_CERTS: set(),
            ConstantesBackup.LIBELLE_CERTS_CHAINE_CATALOGUE: list(),

            # Conserver la liste des grosfichiers requis pour ce backup
            ConstantesBackup.LIBELLE_FUUID_GROSFICHIERS: dict(),

            ConstantesBackup.LIBELLE_BACKUP_PRECEDENT: chainage_backup_precedent,
        }
        # Ajouter le certificat du module courant pour etre sur
        enveloppe_certificat_module_courant = self._contexte.signateur_transactions.enveloppe_certificat_courant
        # Conserver la chaine de validation du catalogue
        certificats_validation_catalogue = [
            enveloppe_certificat_module_courant.fingerprint_ascii
        ]
        catalogue_backup[ConstantesBackup.LIBELLE_CERTS_CHAINE_CATALOGUE] = certificats_validation_catalogue
        certs_pem = {
            enveloppe_certificat_module_courant.fingerprint_ascii: enveloppe_certificat_module_courant.certificat_pem
        }
        catalogue_backup[ConstantesBackup.LIBELLE_CERTS_PEM] = certs_pem
        liste_enveloppes_cas = self._contexte.verificateur_certificats.aligner_chaine_cas(
            enveloppe_certificat_module_courant)
        for cert_ca in liste_enveloppes_cas:
            fingerprint_ca = cert_ca.fingerprint_ascii
            certificats_validation_catalogue.append(fingerprint_ca)
            certs_pem[fingerprint_ca] = cert_ca.certificat_pem
        return catalogue_backup

    def preparer_curseur_transactions(self, nom_collection_mongo, sous_domaine):
        sous_domaine_regex = '^' + sous_domaine.replace('.', '\\.') + '\\.'
        coltrans = self._contexte.document_dao.get_collection(nom_collection_mongo)
        label_tran = '%s.%s' % (
        Constantes.TRANSACTION_MESSAGE_LIBELLE_EVENEMENT, Constantes.EVENEMENT_TRANSACTION_COMPLETE)
        label_backup = '%s.%s' % (
        Constantes.TRANSACTION_MESSAGE_LIBELLE_EVENEMENT, Constantes.EVENEMENT_TRANSACTION_BACKUP_FLAG)
        filtre = {
            label_tran: True,
            label_backup: False,
            'en-tete.domaine': {'$regex': sous_domaine_regex},
        }
        sort = [
            ('_evenements.transaction_traitee', 1)
        ]
        hint = [
            (label_tran, 1),
            (label_backup, 1),
        ]
        curseur = coltrans.find(filtre, sort=sort, hint=hint)
        return curseur

    def _traiter_transaction(self, transaction, heure: datetime.datetime):
        """
        Verifie la signature de la transaction et extrait les certificats requis pour le backup.

        :param transaction:
        :return:
        """
        enveloppe_initial = self._contexte.verificateur_transaction.verifier(transaction)
        enveloppe = enveloppe_initial

        liste_enveloppes_cas = self._contexte.verificateur_certificats.aligner_chaine_cas(enveloppe_initial)

        # S'assurer que le certificat racine correspond a la transaction
        ca_racine = liste_enveloppes_cas[-1]
        if ca_racine.fingerprint_base58 != transaction['en-tete']['idmg']:
            raise ValueError("Transaction IDMG ne correspond pas au certificat racine " + enveloppe.fingerprint_base58)

        # Extraire liste de fingerprints
        liste_cas = [enveloppe.fingerprint_ascii for enveloppe in liste_enveloppes_cas]

        return {
            'certificats': [enveloppe_initial.fingerprint_ascii],
            'certificats_intermediaires': liste_cas[:-1],
            'certificats_racine': [liste_cas[-1]],
        }

    def marquer_transactions_backup_complete(self, nom_collection_mongo: str, uuid_transactions: list):
        """
        Marquer une liste de transactions du domaine comme etat inclues dans un backup horaire.

        :param nom_collection_mongo: Nom de la collection des transactions du domaine
        :param uuid_transactions: Liste des uuid de transactions (en-tete)
        :return:
        """

        evenement = {
            Constantes.TRANSACTION_MESSAGE_LIBELLE_EVENEMENT: Constantes.EVENEMENT_MESSAGE_EVENEMENT,
            Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID: uuid_transactions,
            Constantes.TRANSACTION_MESSAGE_LIBELLE_DOMAINE: nom_collection_mongo,
            Constantes.EVENEMENT_MESSAGE_EVENEMENT: Constantes.EVENEMENT_TRANSACTION_BACKUP_HORAIRE_COMPLETE,
        }
        domaine_action = 'evenement.%s.transactionEvenement' % self._nom_domaine
        # self._contexte.message_dao.transmettre_message(evenement, domaine_action)
        self._contexte.generateur_transactions.emettre_message(evenement, domaine_action, exchanges=[Constantes.DEFAUT_MQ_EXCHANGE_MIDDLEWARE])

    def marquer_transactions_invalides(self, nom_collection_mongo: str, uuid_transactions: list):
        """
        Effectue une correction sur les transactions considerees invalides pour le backup. Ces transactions
        deja traitees sont dans un etat irrecuperable qui ne permet pas de les valider.

        :param nom_collection_mongo: Nom de la collection des transactions du domaine
        :param uuid_transactions: Liste des uuid de transactions (en-tete)
        :return:
        """

        evenement = {
            Constantes.TRANSACTION_MESSAGE_LIBELLE_EVENEMENT: Constantes.EVENEMENT_MESSAGE_EVENEMENT,
            Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID: uuid_transactions,
            Constantes.TRANSACTION_MESSAGE_LIBELLE_DOMAINE: nom_collection_mongo,
            Constantes.EVENEMENT_MESSAGE_EVENEMENT: Constantes.EVENEMENT_TRANSACTION_BACKUP_ERREUR,
        }
        self._contexte.message_dao.transmettre_message(evenement, Constantes.TRANSACTION_ROUTING_EVENEMENT)

    def restaurer_domaines_horaires(self, nom_collection_mongo):

        url_consignationfichiers = 'https://%s:%s' % (
            self._contexte.configuration.serveur_consignationfichiers_host,
            self._contexte.configuration.serveur_consignationfichiers_port,
        )

        backup_workdir = self._contexte.configuration.backup_workdir
        Path(backup_workdir).mkdir(mode=0o700, parents=True, exist_ok=True)

        data = {
            'domaine': nom_collection_mongo
        }

        with requests.get(
                '%s/backup/liste/backups_horaire' % url_consignationfichiers,
                data=data,
                verify=self._contexte.configuration.mq_cafile,
                cert=(self._contexte.configuration.mq_certfile, self._contexte.configuration.mq_keyfile)
        ) as r:

            if r.status_code == 200:
                reponse_json = json.loads(r.text)
            else:
                raise Exception("Erreur chargement liste backups horaire")

        self.__logger.debug("Reponse liste backups horaire:\n" + json.dumps(reponse_json, indent=4))

        for heure, backups in reponse_json['backupsHoraire'].items():
            self.__logger.debug("Telechargement fichiers backup %s" % heure)
            path_fichier_transaction = backups['transactions']
            nom_fichier_transaction = path.basename(path_fichier_transaction)

            with requests.get(
                    '%s/backup/horaire/transactions/%s' % (url_consignationfichiers, path_fichier_transaction),
                    verify=self._contexte.configuration.mq_cafile,
                    cert=(self._contexte.configuration.mq_certfile, self._contexte.configuration.mq_keyfile),
            ) as r:

                r.raise_for_status()

                # Sauvegarder le fichier
                with open(path.join(backup_workdir, nom_fichier_transaction), 'wb') as fichier:
                    for chunk in r.iter_content(chunk_size=8192):
                        fichier.write(chunk)

            path_fichier_catalogue = backups['catalogue']
            nom_fichier_catalogue = path.basename(path_fichier_catalogue)

            # Verifier l'integrite du fichier de transactions
            with lzma.open(path.join(backup_workdir, nom_fichier_catalogue), 'rt') as fichier:
                catalogue = json.load(fichier, object_hook=decoder_backup)

            self.__logger.debug("Verifier signature catalogue %s\n%s" % (nom_fichier_catalogue, catalogue))
            self._contexte.verificateur_transaction.verifier(catalogue)

            with requests.get(
                    '%s/backup/horaire/catalogues/%s' % (url_consignationfichiers, path_fichier_catalogue),
                    verify=self._contexte.configuration.mq_cafile,
                    cert=(self._contexte.configuration.mq_certfile, self._contexte.configuration.mq_keyfile),
            ) as r:

                r.raise_for_status()

                # Sauvegarder le fichier
                with open(path.join(backup_workdir, nom_fichier_catalogue), 'wb') as fichier:
                    for chunk in r.iter_content(chunk_size=8192):
                        fichier.write(chunk)

                    fichier.flush()

            # Catalogue ok, on verifie fichier de transactions
            self.__logger.debug("Verifier SHA_512 sur le fichier de transactions %s" % nom_fichier_transaction)
            transactions_sha512 = catalogue[ConstantesBackup.LIBELLE_TRANSACTIONS_HACHAGE]
            sha512 = hashlib.sha512()
            with open(path.join(backup_workdir, nom_fichier_transaction), 'rb') as fichier:
                sha512.update(fichier.read())
            sha512_digest_calcule = 'sha512_b64:' + b64encode(sha512.digest()).decode('utf-8')

            if transactions_sha512 != sha512_digest_calcule:
                raise Exception(
                    "Le fichier de transactions %s est incorrect, SHA512 ne correspond pas a celui du catalogue" %
                    nom_fichier_transaction
                )

        # Une fois tous les fichiers telecharges et verifies, on peut commencer le
        # chargement dans la collection des transactions du domaine

        for heure, backups in reponse_json['backupsHoraire'].items():
            path_fichier_transaction = backups['transactions']
            nom_fichier_transaction = path.basename(path_fichier_transaction)

            with lzma.open(path.join(backup_workdir, nom_fichier_transaction), 'rt') as fichier:
                for transaction in fichier:
                    self.__logger.debug("Chargement transaction restauree vers collection:\n%s" % str(transaction))
                    # Emettre chaque transaction vers le consignateur de transaction
                    self._contexte.generateur_transactions.restaurer_transaction(transaction)

    def creer_backup_quoditien(self, domaine: str, jour: datetime.datetime):
        coldocs = self._contexte.document_dao.get_collection(ConstantesBackup.COLLECTION_DOCUMENTS_NOM)

        # Calculer la fin du jour comme etant le lendemain, on fait un "<" dans la selection
        fin_jour = jour + datetime.timedelta(days=1)

        # Faire la liste des catalogues de backups qui sont dus
        filtre_backups_quotidiens_dirty = {
            Constantes.DOCUMENT_INFODOC_LIBELLE: ConstantesBackup.LIBVAL_CATALOGUE_QUOTIDIEN,
            ConstantesBackup.LIBELLE_DOMAINE: {'$regex': '^' + domaine},
            ConstantesBackup.LIBELLE_DIRTY_FLAG: True,
            ConstantesBackup.LIBELLE_JOUR: {'$lt': fin_jour}
        }
        curseur_catalogues = coldocs.find(filtre_backups_quotidiens_dirty)
        plus_vieux_jour = jour

        for catalogue in curseur_catalogues:

            # Identifier le plus vieux backup qui est effectue
            # Utilise pour transmettre trigger backup annuel
            jour_backup = pytz.utc.localize(catalogue[ConstantesBackup.LIBELLE_JOUR])
            if plus_vieux_jour > jour_backup:
                plus_vieux_jour = jour_backup

            # Filtrer catalogue pour retirer les champs Mongo
            for champ in catalogue.copy().keys():
                if champ.startswith('_') or champ in [ConstantesBackup.LIBELLE_DIRTY_FLAG]:
                    del catalogue[champ]

            # Generer l'entete et la signature pour le catalogue
            catalogue_json = json.dumps(catalogue, sort_keys=True, ensure_ascii=True, cls=DateFormatEncoder)
            catalogue = json.loads(catalogue_json)
            catalogue_quotidien = self._contexte.generateur_transactions.preparer_enveloppe(
                catalogue, ConstantesBackup.TRANSACTION_CATALOGUE_QUOTIDIEN, ajouter_certificats=True)
            self.__logger.debug("Catalogue:\n%s" % catalogue_quotidien)

            # Transmettre le catalogue au consignateur de fichiers sous forme de commande. Ceci declenche la
            # creation de l'archive de backup. Une fois termine, le consignateur de fichier va transmettre une
            # transaction de catalogue quotidien.
            self._contexte.generateur_transactions.transmettre_commande(
                {'catalogue': catalogue_quotidien}, ConstantesBackup.COMMANDE_BACKUP_QUOTIDIEN)

        self.transmettre_trigger_annee_precedente(plus_vieux_jour)

    def creer_backup_mensuel(self, domaine: str, mois: datetime.datetime):
        coldocs = self._contexte.document_dao.get_collection(ConstantesBackup.COLLECTION_DOCUMENTS_NOM)
        collection_pki = self._contexte.document_dao.get_collection(ConstantesPki.COLLECTION_DOCUMENTS_NOM)

        # Calculer la fin du jour comme etant le lendemain, on fait un "<" dans la selection
        annee_fin = mois.year
        mois_fin = mois.month + 1
        if mois_fin > 12:
            annee_fin = annee_fin + 1
            mois_fin = 1
        fin_mois = datetime.datetime(year=annee_fin, month=mois_fin, day=1)

        # Faire la liste des catalogues de backups qui sont dus
        filtre_backups_mensuels_dirty = {
            Constantes.DOCUMENT_INFODOC_LIBELLE: ConstantesBackup.LIBVAL_CATALOGUE_MENSUEL,
            ConstantesBackup.LIBELLE_DOMAINE: domaine,
            ConstantesBackup.LIBELLE_DIRTY_FLAG: True,
            ConstantesBackup.LIBELLE_MOIS: {'$lt': fin_mois}
        }
        curseur_catalogues = coldocs.find(filtre_backups_mensuels_dirty)
        plus_vieux_mois = mois

        for catalogue in curseur_catalogues:

            # Identifier le plus vieux backup qui est effectue
            # Utilise pour transmettre trigger backup mensuel
            mois_backup = pytz.utc.localize(catalogue[ConstantesBackup.LIBELLE_MOIS])
            if plus_vieux_mois > mois_backup:
                plus_vieux_mois = mois_backup

            # Ajouter le certificat du module courant pour etre sur de pouvoir valider le catalogue mensuel
            enveloppe_certificat_module_courant = self._contexte.signateur_transactions.enveloppe_certificat_courant

            try:
                certs_pem = catalogue[ConstantesBackup.LIBELLE_CERTS_PEM]
            except KeyError:
                certs_pem = dict()
                catalogue[ConstantesBackup.LIBELLE_CERTS_PEM] = certs_pem

            certificats_validation_catalogue = [
                enveloppe_certificat_module_courant.fingerprint_ascii
            ]
            catalogue[ConstantesBackup.LIBELLE_CERTS_CHAINE_CATALOGUE] = certificats_validation_catalogue

            certs_pem[enveloppe_certificat_module_courant.fingerprint_ascii] = enveloppe_certificat_module_courant.certificat_pem

            liste_enveloppes_cas = self._contexte.verificateur_certificats.aligner_chaine_cas(enveloppe_certificat_module_courant)
            for cert_ca in liste_enveloppes_cas:
                fingerprint_ca = cert_ca.fingerprint_ascii
                certificats_validation_catalogue.append(fingerprint_ca)
                certs_pem[fingerprint_ca] = cert_ca.certificat_pem

            # Filtrer catalogue pour retirer les champs Mongo
            for champ in catalogue.copy().keys():
                if champ.startswith('_') or champ in [ConstantesBackup.LIBELLE_DIRTY_FLAG]:
                    del catalogue[champ]

            # Generer l'entete et la signature pour le catalogue
            catalogue_json = json.dumps(catalogue, sort_keys=True, ensure_ascii=True, cls=DateFormatEncoder)
            catalogue = json.loads(catalogue_json)
            catalogue_mensuel = self._contexte.generateur_transactions.preparer_enveloppe(
                catalogue, ConstantesBackup.TRANSACTION_CATALOGUE_MENSUEL)
            self.__logger.debug("Catalogue:\n%s" % catalogue_mensuel)

            # Transmettre le catalogue au consignateur de fichiers sous forme de commande. Ceci declenche la
            # creation de l'archive de backup. Une fois termine, le consignateur de fichier va transmettre une
            # transaction de catalogue quotidien.
            self._contexte.generateur_transactions.transmettre_commande(
                {'catalogue': catalogue_mensuel}, ConstantesBackup.COMMANDE_BACKUP_MENSUEL)

        self.transmettre_trigger_annee_precedente(mois)

    def creer_backup_annuel(self, domaine: str, annee: datetime.datetime):
        pass

    def transmettre_evenement_backup(self, evenement: str, heure: datetime.datetime, info: dict = None):
        evenement_contenu = {
            Constantes.EVENEMENT_MESSAGE_EVENEMENT: evenement,
            ConstantesBackup.LIBELLE_DOMAINE: self._nom_domaine,
            Constantes.EVENEMENT_MESSAGE_EVENEMENT_TIMESTAMP: int(heure.timestamp()),
            ConstantesBackup.LIBELLE_SECURITE: self.__niveau_securite,
        }
        if info:
            evenement_contenu['info'] = info

        domaine = 'evenement.%s.%s' % (self._nom_domaine, evenement)

        self._contexte.generateur_transactions.emettre_message(
            evenement_contenu, domaine, exchanges=[Constantes.DEFAUT_MQ_EXCHANGE_NOEUDS]
        )

    def transmettre_trigger_jour_precedent(self, heure_plusvieille):
        """
        Determiner le jour avant la plus vieille transaction. On va transmettre un declencheur de
        backup quotidien, mensuel et annuel pour les aggregations qui peuvent etre generees

        :param heure_plusvieille:
        :return:
        """

        veille = heure_plusvieille - datetime.timedelta(days=1)
        veille = datetime.datetime(year=veille.year, month=veille.month, day=veille.day, tzinfo=datetime.timezone.utc)
        self.__logger.debug("Veille: %s" % str(veille))

        commande_backup_quotidien = {
            ConstantesBackup.LIBELLE_JOUR: int(veille.timestamp()),
            ConstantesBackup.LIBELLE_DOMAINE: self._nom_domaine,
            ConstantesBackup.LIBELLE_SECURITE: Constantes.SECURITE_PRIVE,
        }
        self._contexte.generateur_transactions.transmettre_commande(
            commande_backup_quotidien,
            ConstantesBackup.COMMANDE_BACKUP_DECLENCHER_QUOTIDIEN.replace(
                '_DOMAINE_', self._nom_domaine),
            exchange=Constantes.DEFAUT_MQ_EXCHANGE_MIDDLEWARE
        )

    def transmettre_trigger_annee_precedente(self, date: datetime.datetime):
        mois_moins_18 = date - datetime.timedelta(days=-549)  # 18 mois
        annee_precedente = datetime.datetime(year=mois_moins_18.year, month=1, day=1, tzinfo=datetime.timezone.utc)

        commande_backup_annuel = {
            ConstantesBackup.LIBELLE_ANNEE: int(annee_precedente.timestamp()),
            ConstantesBackup.LIBELLE_DOMAINE: self._nom_domaine,
            ConstantesBackup.LIBELLE_SECURITE: Constantes.SECURITE_PRIVE,
        }
        self._contexte.generateur_transactions.transmettre_commande(
            commande_backup_annuel,
            ConstantesBackup.COMMANDE_BACKUP_DECLENCHER_ANNUEL.replace('_DOMAINE_', self._nom_domaine),
            exchange=Constantes.DEFAUT_MQ_EXCHANGE_MIDDLEWARE
        )

    def calculer_hash_entetebackup(self, entete):
        """
        Generer une valeur de hachage a partir de l'entete
        :param entete:
        :return:
        """
        hachage_backup = self._contexte.verificateur_transaction.hacher_contenu(entete, hachage=hashes.SHA512())
        hachage_backup = 'sha512_b64:' + hachage_backup
        return hachage_backup

    def chiffrer_cle(self, pems: list, cle_secrete: bytes):
        cles = dict()
        for pem in pems:
            clecert = EnveloppeCleCert()
            clecert.cert_from_pem_bytes(pem.encode('utf-8'))
            fingerprint_b64 = clecert.fingerprint_b64
            cle_chiffree, fingerprint = clecert.chiffrage_asymmetrique(cle_secrete)

            cle_chiffree_b64 = b64encode(cle_chiffree).decode('utf-8')
            cles[fingerprint_b64] = cle_chiffree_b64

        return cles