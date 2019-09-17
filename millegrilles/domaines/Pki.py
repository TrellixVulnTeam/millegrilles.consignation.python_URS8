# Domaine Public Key Infrastructure (PKI)

from millegrilles import Constantes
from millegrilles.Domaines import GestionnaireDomaineStandard, RegenerateurDeDocumentsSansEffet
from millegrilles.dao.MessageDAO import TraitementMessageDomaine
from millegrilles.MGProcessus import MGPProcesseur, MGProcessus, MGProcessusTransaction
from millegrilles.SecuritePKI import ConstantesSecurityPki, EnveloppeCertificat, VerificateurCertificats

import logging
import datetime


class ConstantesPki:

    DOMAINE_NOM = 'millegrilles.domaines.Pki'
    COLLECTION_TRANSACTIONS_NOM = 'millegrilles.domaines.Pki'
    COLLECTION_DOCUMENTS_NOM = ConstantesSecurityPki.COLLECTION_NOM
    COLLECTION_PROCESSUS_NOM = 'millegrilles.domaines.Pki/processus'
    QUEUE_NOM = DOMAINE_NOM

    LIBELLE_CERTIFICAT_PEM = ConstantesSecurityPki.LIBELLE_CERTIFICAT_PEM
    LIBELLE_FINGERPRINT = ConstantesSecurityPki.LIBELLE_FINGERPRINT
    LIBELLE_FINGERPRINT_ISSUER = 'fingerprint_issuer'
    LIBELLE_DOCID_ISSUER = '_id_issuer'
    LIBELLE_CHAINE_COMPLETE = 'chaine_complete'
    LIBELLE_SUBJECT = 'sujet'
    LIBELLE_ISSUER = 'issuer'
    LIBELLE_NOT_VALID_BEFORE = 'not_valid_before'
    LIBELLE_NOT_VALID_AFTER = 'not_valid_after'
    LIBELLE_SUBJECT_KEY = 'subject_key'
    LIBELLE_AUTHORITY_KEY = 'authority_key'

    LIBVAL_CONFIGURATION = 'configuration'
    LIBVAL_CERTIFICAT_ROOT = 'certificat.root'
    LIBVAL_CERTIFICAT_INTERMEDIAIRE = 'certificat.intermediaire'
    LIBVAL_CERTIFICAT_MILLEGRILLE = 'certificat.millegrille'
    LIBVAL_CERTIFICAT_NOEUD = 'certificat.noeud'

    TRANSACTION_EVENEMENT_CERTIFICAT = 'certificat'  # Indique que c'est une transaction avec un certificat a ajouter

    # Indique que c'est un evenement avec un certificat (reference)
    EVENEMENT_CERTIFICAT = ConstantesSecurityPki.EVENEMENT_CERTIFICAT
    # Indique que c'est une requete pour trouver un certificat par fingerprint
    EVENEMENT_REQUETE = ConstantesSecurityPki.EVENEMENT_REQUETE

    # Document par defaut pour la configuration de l'interface principale
    DOCUMENT_DEFAUT = {
        Constantes.DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION
    }

    DOCUMENT_CERTIFICAT_NOEUD = {
        Constantes.DOCUMENT_INFODOC_LIBELLE: LIBVAL_CERTIFICAT_NOEUD,
        LIBELLE_CERTIFICAT_PEM: '',
        LIBELLE_FINGERPRINT: '',
        LIBELLE_CHAINE_COMPLETE: False
    }


class GestionnairePki(GestionnaireDomaineStandard):

    def __init__(self, contexte):
        super().__init__(contexte)
        self._logger = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))

        self._pki_document_helper = None
        self._traitement_message = None

    def configurer(self):
        super().configurer()
        self._pki_document_helper = PKIDocumentHelper(self._contexte, self.demarreur_processus)
        self._traitement_message = TraitementMessagePki(self, self._pki_document_helper)

        self.initialiser_document(ConstantesPki.LIBVAL_CONFIGURATION, ConstantesPki.DOCUMENT_DEFAUT)
        self.initialiser_mgca()

        # Index collection domaine
        collection_domaine = self.get_collection()
        # Index par fingerprint de certificat
        collection_domaine.create_index([
            (ConstantesPki.LIBELLE_FINGERPRINT, 1)
        ], unique=True)
        # Index par chaine de certificat verifie
        collection_domaine.create_index([
            (ConstantesPki.LIBELLE_CHAINE_COMPLETE, 2),
            (Constantes.DOCUMENT_INFODOC_LIBELLE, 1)
        ])
        # Index pour trouver l'autorite qui a signe un certificat (par son subject)
        collection_domaine.create_index([
            (ConstantesPki.LIBELLE_SUBJECT_KEY, 1),
            (ConstantesPki.LIBELLE_NOT_VALID_BEFORE, 1),
            (ConstantesPki.LIBELLE_NOT_VALID_AFTER, 1)
        ])

    def get_queue_configuration(self):
        configuration = super().get_queue_configuration()

        configuration_pki = [
            {
                'nom': '%s.%s' % (self.get_nom_queue(), 'certificats'),
                'routing': [
                    'pki.#',
                ],
                'exchange': self.configuration.exchange_middleware,
                'callback': self.traiter_transaction
            },
            {
                'nom': '%s.%s' % (self.get_nom_queue(), 'certificats'),
                'routing': [
                    'pki.#',
                ],
                'exchange': self.configuration.exchange_noeuds,
                'callback': self.traiter_requete_noeud
            },
            {
                'nom': '%s.%s' % (self.get_nom_queue(), 'certificats'),
                'routing': [
                    'pki.#',
                ],
                'exchange': self.configuration.exchange_inter,
                'callback': self.traiter_requete_inter
            },
        ]

        configuration.extend(configuration_pki)

        return configuration

    def traiter_transaction(self, ch, method, properties, body):
        self._traitement_message.callbackAvecAck(ch, method, properties, body)

    def traiter_requete_noeud(self, ch, method, properties, body):
        return self.traiter_transaction(ch, method, properties, body)

    def traiter_requete_inter(self, ch, method, properties, body):
        return self.traiter_transaction(ch, method, properties, body)

    def traiter_cedule(self, evenement):

        indicateurs = evenement['indicateurs']
        self._logger.debug("Cedule webPoll: %s" % str(indicateurs))

        # Faire la liste des cedules a declencher
        if 'heure' in indicateurs:
            # declencher workflow pour trouver les certificats dans MongoDB qui ne sont pas encore valides
            processus = "%s:%s" % (
                ConstantesPki.DOMAINE_NOM,
                ProcessusVerifierChaineCertificatsNonValides.__name__
            )
            self.demarrer_processus(processus, dict())

    def get_nom_queue(self):
        return ConstantesPki.QUEUE_NOM

    def get_nom_collection(self):
        return ConstantesPki.COLLECTION_DOCUMENTS_NOM

    def get_collection_transaction_nom(self):
        return ConstantesPki.COLLECTION_TRANSACTIONS_NOM

    def get_collection_processus_nom(self):
        return ConstantesPki.COLLECTION_PROCESSUS_NOM

    def initialiser_mgca(self):
        """ Initialise les root CA et noeud middleware (ou local) """
        ca_file = self.configuration.mq_cafile

        with open(ca_file) as f:
            contenu = f.read()
            cles = contenu.split(ConstantesSecurityPki.DELIM_DEBUT_CERTIFICATS)[1:]
            self._logger.debug("Certificats ROOT configures: %s" % cles)

        for cle in cles:
            certificat_pem = '%s%s' % (ConstantesSecurityPki.DELIM_DEBUT_CERTIFICATS, cle)
            enveloppe = EnveloppeCertificat(certificat_pem=bytes(certificat_pem, 'utf-8'))
            self._logger.debug("OUN pour cert = %s" % enveloppe.subject_organizational_unit_name)
            self._pki_document_helper.inserer_certificat(enveloppe, upsert=True, trusted=True)

        mq_certfile = self.configuration.mq_certfile
        with open(mq_certfile) as f:
            contenu_pem = f.read()
            enveloppe = EnveloppeCertificat(certificat_pem=bytes(contenu_pem, 'utf-8'))
            self._logger.debug("Certificats noeud local: %s" % contenu)
            self._pki_document_helper.inserer_certificat(enveloppe, upsert=True, trusted=False)

        # Demarrer validation des certificats
        # declencher workflow pour trouver les certificats dans MongoDB qui ne sont pas encore valides
        # processus = "%s:%s" % (
        #     ConstantesPki.DOMAINE_NOM,
        #     ProcessusVerifierChaineCertificatsNonValides.__name__
        # )
        # self.demarrer_processus(processus, dict())

    def get_nom_domaine(self):
        return ConstantesPki.DOMAINE_NOM

    def identifier_processus(self, domaine_transaction):
        if domaine_transaction == ConstantesPki.TRANSACTION_EVENEMENT_CERTIFICAT:
            processus = "millegrilles_domaines_Pki:ProcessusAjouterCertificat"
        else:
            processus = super().identifier_processus(domaine_transaction)
        return processus

    def creer_regenerateur_documents(self):
        return RegenerateurDeDocumentsSansEffet(self)


class PKIDocumentHelper:

    def __init__(self, contexte, mg_processus_demarreur):
        self._contexte = contexte
        # self._mg_processus_demarreur = MGPProcessusDemarreur(self._contexte)
        self._mg_processus_demarreur = mg_processus_demarreur

    def inserer_certificat(self, enveloppe, upsert=False, trusted=False):
        document_cert = ConstantesPki.DOCUMENT_CERTIFICAT_NOEUD.copy()
        fingerprint = enveloppe.fingerprint_ascii

        maintenant = datetime.datetime.now(tz=datetime.timezone.utc)
        document_cert[Constantes.DOCUMENT_INFODOC_DATE_CREATION] = maintenant
        document_cert[Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION] = maintenant

        document_cert[ConstantesPki.LIBELLE_CERTIFICAT_PEM] = enveloppe.certificat_pem
        document_cert[ConstantesPki.LIBELLE_FINGERPRINT] = fingerprint
        document_cert[ConstantesPki.LIBELLE_SUBJECT] = enveloppe.formatter_subject()
        document_cert[ConstantesPki.LIBELLE_NOT_VALID_BEFORE] = enveloppe.not_valid_before
        document_cert[ConstantesPki.LIBELLE_NOT_VALID_AFTER] = enveloppe.not_valid_after
        document_cert[ConstantesPki.LIBELLE_SUBJECT_KEY] = enveloppe.subject_key_identifier
        document_cert[ConstantesPki.LIBELLE_AUTHORITY_KEY] = enveloppe.authority_key_identifier

        if enveloppe.is_CA:
            if enveloppe.subject_organizational_unit_name == 'MilleGrille':
                document_cert[Constantes.DOCUMENT_INFODOC_LIBELLE] = ConstantesPki.LIBVAL_CERTIFICAT_MILLEGRILLE
            else:
                document_cert[Constantes.DOCUMENT_INFODOC_LIBELLE] = ConstantesPki.LIBVAL_CERTIFICAT_INTERMEDIAIRE

            if trusted and enveloppe.is_rootCA:
                document_cert[Constantes.DOCUMENT_INFODOC_LIBELLE] = ConstantesPki.LIBVAL_CERTIFICAT_ROOT
                # Le certificat root est trusted implicitement quand il est charge a partir d'un fichier local
                document_cert[ConstantesPki.LIBELLE_CHAINE_COMPLETE] = True

        filtre = {
            ConstantesPki.LIBELLE_FINGERPRINT: fingerprint
        }

        collection = self._contexte.document_dao.get_collection(ConstantesPki.COLLECTION_DOCUMENTS_NOM)
        if upsert:
            collection.update_one(filtre, {'$setOnInsert': document_cert}, upsert=upsert)
        else:
            collection.insert_one(document_cert)

        # Demarrer validation des certificats
        # declencher workflow pour trouver les certificats dans MongoDB qui ne sont pas encore valides
        processus = "%s:%s" % (
            ConstantesPki.DOMAINE_NOM,
            ProcessusVerifierChaineCertificatsNonValides.__name__
        )
        self._mg_processus_demarreur.demarrer_processus(processus, dict())

    def charger_certificat(self, fingerprint=None, subject=None):
        filtre = dict()
        if fingerprint is not None:
            filtre[ConstantesPki.LIBELLE_FINGERPRINT] = fingerprint
        if subject is not None:
            filtre[ConstantesPki.LIBELLE_SUBJECT_KEY] = subject

        # Lire les certificats et les charger dans des enveloppes
        collection = self._contexte.document_dao.get_collection(ConstantesPki.COLLECTION_DOCUMENTS_NOM)
        curseur = collection.find(filtre)
        liste_certificats = list()
        for certificat in curseur:
            # Charger l'enveloppe
            enveloppe = EnveloppeCertificat(certificat_pem=certificat[ConstantesPki.LIBELLE_CERTIFICAT_PEM])
            liste_certificats.append(enveloppe)

        return liste_certificats

    def identifier_certificats_non_valide(self, authority_key=None):
        """
        Fait une liste des fingerprints de certificats qui ne sont pas encore valides.
        :param authority_key: Optionnel, va charger tous les certificats pas encore valides associes a cette autorite.
        :return: Liste de fingerprints
        """
        filtre = {
            ConstantesPki.LIBELLE_CHAINE_COMPLETE: False
        }

        if authority_key is not None:
            filtre[ConstantesPki.LIBELLE_AUTHORITY_KEY] = authority_key

        collection = self._contexte.document_dao.get_collection(ConstantesPki.COLLECTION_DOCUMENTS_NOM)
        curseur = collection.find(filtre)
        fingerprints = list()
        for certificat in curseur:
            fingerprint = certificat[ConstantesPki.LIBELLE_FINGERPRINT]
            fingerprints.append(fingerprint)

        return fingerprints

    def marquer_certificats_valides(self, fingerprints):

        filtre = {
            ConstantesPki.LIBELLE_FINGERPRINT: {'$in': fingerprints}
        }

        operation = {
            '$set': {
                ConstantesPki.LIBELLE_CHAINE_COMPLETE: True
            }
        }

        collection = self._contexte.document_dao.get_collection(ConstantesPki.COLLECTION_DOCUMENTS_NOM)
        collection.update(filtre, operation, multi=True)


class TraitementMessagePki(TraitementMessageDomaine):

    def __init__(self, gestionnaire, pki_document_helper):
        super().__init__(gestionnaire)
        # self._pki_document_helper = PKIDocumentHelper(gestionnaire.contexte)
        self._pki_document_helper = pki_document_helper

    def traiter_message(self, ch, method, properties, body):
        message_dict = self.json_helper.bin_utf8_json_vers_dict(body)
        evenement = message_dict.get(Constantes.EVENEMENT_MESSAGE_EVENEMENT)
        routing_key = method.routing_key

        if routing_key.split('.')[0:2] == ['processus', 'domaine']:
            # Chaining vers le gestionnaire de processus du domaine
            self._gestionnaire.traitement_evenements.traiter_message(ch, method, properties, body)

        elif evenement == Constantes.EVENEMENT_CEDULEUR:
            # Ceduleur, verifier si action requise
            self._gestionnaire.traiter_cedule(message_dict)
        elif evenement == Constantes.EVENEMENT_TRANSACTION_PERSISTEE:
            # Verifier quel processus demarrer. On match la valeur dans la routing key.
            routing_key = method.routing_key
            routing_key_sansprefixe = routing_key.replace(
                'destinataire.domaine.%s.' % ConstantesPki.DOMAINE_NOM,
                ''
            )

            processus = self.gestionnaire.identifier_processus(routing_key_sansprefixe)
            self._gestionnaire.demarrer_processus(processus, message_dict)

        elif evenement == ConstantesPki.EVENEMENT_CERTIFICAT:
            enveloppe = EnveloppeCertificat(certificat_pem=message_dict[ConstantesPki.LIBELLE_CERTIFICAT_PEM])
            # Enregistrer le certificat - le helper va verifier si c'est un nouveau certificat ou si on l'a deja
            self._pki_document_helper.inserer_certificat(enveloppe, upsert=True)

        else:
            # Type d'evenement inconnu, on lance une exception
            raise ValueError("Type d'evenement inconnu: %s" % str(evenement))


class ProcessusAjouterCertificat(MGProcessusTransaction):

    def __init__(self, controleur: MGPProcesseur, evenement):
        super().__init__(controleur, evenement)

    def initiale(self):
        transaction = self.charger_transaction(ConstantesPki.COLLECTION_DOCUMENTS_NOM)
        fingerprint = transaction['fingerprint']
        self._logger.debug("Chargement certificat fingerprint: %s" % fingerprint)

        # Verifier si on a deja les certificats
        collection = self.document_dao.get_collection(ConstantesPki.COLLECTION_DOCUMENTS_NOM)
        certificat_existant = collection.find_one({'fingerprint': fingerprint})

        if certificat_existant is None:
            # Si on n'a pas le certificat, on le conserve et on lance la verification de chaine
            enveloppe_certificat = EnveloppeCertificat(certificat_pem=bytes(transaction['certificat_pem'], 'utf-8'))

            # Sauvegarder certificat #
            document_certificat = ConstantesPki.DOCUMENT_CERTIFICAT_NOEUD.copy()
            document_certificat[ConstantesPki.LIBELLE_CERTIFICAT_PEM] = transaction['certificat_pem']
            document_certificat[ConstantesPki.LIBELLE_FINGERPRINT] = enveloppe_certificat.fingerprint_ascii

            collection.insert_one(document_certificat)

            self.set_etape_suivante(ProcessusAjouterCertificat.verifier_chaine.__name__)
        else:
            self.set_etape_suivante()  # Termine

    def verifier_chaine(self):
        self.set_etape_suivante()  # Termine

    def get_collection_transaction_nom(self):
        return ConstantesPki.COLLECTION_TRANSACTIONS_NOM

    def get_collection_processus_nom(self):
        return ConstantesPki.COLLECTION_PROCESSUS_NOM


class ProcessusVerifierChaineCertificatsNonValides(MGProcessus):

    PARAM_A_VERIFIER = 'fingerprints_a_verifier'
    PARAM_VALIDE = 'fingerprints_valides'
    PARAM_INVALIDE = 'fingerprints_invalides'

    def __init__(self, controleur: MGPProcesseur, evenement):
        super().__init__(controleur, evenement)
        self._helper = PKIDocumentHelper(self._controleur.contexte, self._controleur.demarreur_processus)

    def initiale(self):
        liste_fingerprints = self._helper.identifier_certificats_non_valide()

        resultat = {}
        if len(liste_fingerprints) > 0:
            resultat[ProcessusVerifierChaineCertificatsNonValides.PARAM_A_VERIFIER] = liste_fingerprints
            self.set_etape_suivante(ProcessusVerifierChaineCertificatsNonValides.verifier_chaines.__name__)
        else:
            self.set_etape_suivante()

        return resultat

    def verifier_chaines(self):

        parametres = self.parametres
        fingerprints = parametres.get(ProcessusVerifierChaineCertificatsNonValides.PARAM_A_VERIFIER)

        verificateur = VerificateurCertificats(self._controleur.contexte)

        liste_valide = list()
        liste_invalide = list()
        for fingerprint in fingerprints:
            # Charger le certificat et verifier si on peut valider la chaine
            try:
                enveloppe = verificateur.charger_certificat(fingerprint=fingerprint)
                if enveloppe is not None:
                    verificateur.verifier_chaine(enveloppe)
                    liste_valide.append(fingerprint)
            except Exception as e:
                self._logger.warn("Certificat invalide: %s" % fingerprint)
                self._logger.debug("Certificat pas encore valide %s: %s" % (fingerprint, str(e)))

            if fingerprint not in liste_valide:
                liste_invalide.append(fingerprint)

        resultat = {
            ProcessusVerifierChaineCertificatsNonValides.PARAM_VALIDE: liste_valide,
            ProcessusVerifierChaineCertificatsNonValides.PARAM_INVALIDE: liste_invalide
        }

        if len(liste_valide) > 0:
            self.set_etape_suivante(ProcessusVerifierChaineCertificatsNonValides.marquer_certificats_valides.__name__)
        elif len(liste_invalide) > 0:
            self.set_etape_suivante(ProcessusVerifierChaineCertificatsNonValides.chercher_certificats_invalides.__name__)
        else:
            self.set_etape_suivante()

        return resultat

    def marquer_certificats_valides(self):
        parametres = self.parametres

        fingerprints = parametres.get(ProcessusVerifierChaineCertificatsNonValides.PARAM_VALIDE)
        self._helper.marquer_certificats_valides(fingerprints)

        if len(parametres[ProcessusVerifierChaineCertificatsNonValides.PARAM_INVALIDE]) > 0:
            self.set_etape_suivante(ProcessusVerifierChaineCertificatsNonValides.chercher_certificats_invalides.__name__)
        else:
            self.set_etape_suivante()

    def chercher_certificats_invalides(self):
        self.set_etape_suivante()

    def get_collection_transaction_nom(self):
        return ConstantesPki.COLLECTION_TRANSACTIONS_NOM

    def get_collection_processus_nom(self):
        return ConstantesPki.COLLECTION_PROCESSUS_NOM
