# Script de test pour transmettre message de transaction

import datetime, time
import json

from millegrilles.dao.Configuration import ContexteRessourcesMilleGrilles
from millegrilles.dao.MessageDAO import BaseCallback
from millegrilles.transaction.GenerateurTransaction import GenerateurTransaction
from millegrilles import Constantes
from millegrilles.domaines.MaitreDesCles import ConstantesMaitreDesCles
from millegrilles.domaines.Parametres import ConstantesParametres
from millegrilles.util.X509Certificate import EnveloppeCleCert

from threading import Event, Thread
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat import primitives
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64encode
from uuid import uuid4


contexte = ContexteRessourcesMilleGrilles()
contexte.initialiser()


class MessagesSample(BaseCallback):

    def __init__(self):
        super().__init__(contexte)
        self.contexte.message_dao.register_channel_listener(self)
        self.generateur = GenerateurTransaction(self.contexte)
        self.channel = None
        self.event_recu = Event()
        # self.thread_ioloop = Thread(target=self.run_ioloop)

        self.certificat_maitredescles = None
        self.cert_maitredescles_recu = Event()

        self.mot_de_passe = 'sjdpo-1824-JWAZ'

        # Charger cert MaitreDesCles pour pouvoir crypter contenu a transmettre
        with open('/home/mathieu/mgdev/certs/pki.maitrecles.cert', 'rb') as certificat_pem:
            certificat_courant_pem = certificat_pem.read()
            cert = x509.load_pem_x509_certificate(
                certificat_courant_pem,
                backend=default_backend()
            )
            self.certificat_courant = cert
            self.certificat_courant_pem = certificat_courant_pem.decode('utf8')

    def on_channel_open(self, channel):
        # Enregistrer la reply-to queue
        self.channel = channel
        channel.queue_declare(durable=True, exclusive=True, callback=self.queue_open)

    def queue_open(self, queue):
        self.queue_name = queue.method.queue
        print("Queue: %s" % str(self.queue_name))

        self.channel.basic_consume(self.callbackAvecAck, queue=self.queue_name, no_ack=False)
        # self.event_recu.set()
        self.executer()

    # def run_ioloop(self):
    #     self.contexte.message_dao.run_ioloop()

    def deconnecter(self):
        self.contexte.message_dao.deconnecter()

    def traiter_message(self, ch, method, properties, body):
        print("Message recu, correlationId: %s" % properties.correlation_id)
        print(body)

        message_dict = json.loads(body)
        certificat_pem = message_dict.get('certificat')
        if certificat_pem is not None:
            cert = EnveloppeCleCert()
            cert.cert_from_pem_bytes(certificat_pem.encode('utf-8'))
            self.certificat_maitredescles = cert
            self.cert_maitredescles_recu.set()
        else:
            self.event_recu.set()
            if message_dict['resultats'].get('certificats_pem'):
                for cert in message_dict['resultats'].get('certificats_pem'):
                    print(cert)

            print(json.dumps(message_dict, indent=4))

    def requete_cert_maitredescles(self):
        requete_cert_maitredescles = {
            Constantes.TRANSACTION_MESSAGE_LIBELLE_EVENEMENT: ConstantesMaitreDesCles.REQUETE_CERT_MAITREDESCLES
        }
        enveloppe_requete = self.generateur.transmettre_requete(
            requete_cert_maitredescles,
            'millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.REQUETE_CERT_MAITREDESCLES,
            'abcd-1234',
            self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def requete_trousseau_hebergement(self):
        requete = {
            'idmg': ['2aMvfBTqyfeQsMgSsYbtJuMeqUJ5TZV2iNiy2ES']
        }
        enveloppe_requete = self.generateur.transmettre_requete(
            requete,
            'millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.REQUETE_TROUSSEAU_HEBERGEMENT,
            'abcd-1234',
            self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def requete_decryptage_cle_fuuid(self):
        requete_cert_maitredescles = {
            'fuuid': "b4ecca10-1c2b-11ea-904a-7b4d1a2d4432"
        }
        enveloppe_requete = self.generateur.transmettre_requete(
            requete_cert_maitredescles,
            'millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.REQUETE_DECRYPTAGE_GROSFICHIER,
            'abcd-1234',
            self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def requete_decryptage_cle_fuuid_avecfingerprint(self):
        requete_cert_maitredescles = {
            'fuuid': "b4ecca10-1c2b-11ea-904a-7b4d1a2d4432",
            'fingerprint': '74fd5742aec60dd37f99c75df423008a10149018'
        }
        enveloppe_requete = self.generateur.transmettre_requete(
            requete_cert_maitredescles,
            'millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.REQUETE_DECRYPTAGE_GROSFICHIER,
            'abcd-1234',
            self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def requete_cle_racine(self):
        # Attendre le certificat de maitre des cles pour chiffrer la cle
        self.cert_maitredescles_recu.wait(5)

        mot_de_passe_chiffre, fingerprint = self.certificat_maitredescles.chiffrage_asymmetrique(self.mot_de_passe.encode('utf-8'))

        requete_cle_racine = {
            'fingerprint': '',
            'mot_de_passe_chiffre': str(b64encode(mot_de_passe_chiffre), 'utf-8'),
        }
        enveloppe_requete = self.generateur.transmettre_requete(
            requete_cle_racine,
            'millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.REQUETE_CLE_RACINE,
            'abcd-1234',
            self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def commande_signer_cle_backup(self):
        with open ('/home/mathieu/mgdev/certs/pki.connecteur.key', 'rb') as fichier:
            key_bytes = fichier.read()

        enveloppe = EnveloppeCleCert()
        enveloppe.key_from_pem_bytes(key_bytes, None)
        public_bytes = enveloppe.public_bytes

        requete_cle_racine = {
            'cle_publique': public_bytes.decode('utf-8'),
        }
        enveloppe_requete = self.generateur.transmettre_commande(
            requete_cle_racine,
            'commande.millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.COMMANDE_SIGNER_CLE_BACKUP,
            correlation_id='abcd-1234',
            reply_to=self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def commande_restaurer_backup_cle(self):
        with open ('/home/mathieu/mgdev/certs/pki.connecteur.key', 'rb') as fichier:
            key_bytes = fichier.read()

        clecert = EnveloppeCleCert()
        clecert.key_from_pem_bytes(key_bytes, None)
        clecert.password = self.mot_de_passe.encode('utf-8')
        key_chiffree_bytes = clecert.private_key_bytes

        self.cert_maitredescles_recu.wait(5)
        mot_de_passe_chiffre, fingerprint = self.certificat_maitredescles.chiffrage_asymmetrique(self.mot_de_passe.encode('utf-8'))

        enveloppe = EnveloppeCleCert()
        enveloppe.key_from_pem_bytes(key_bytes, None)

        requete_cle_racine = {
            'cle_privee': key_chiffree_bytes.decode('utf-8'),
            'mot_de_passe_chiffre': str(b64encode(mot_de_passe_chiffre), 'utf-8'),
            # 'fingerprint_base64': 'Ut/UQ5aKomoGzXB7mpUduPk4Xzg=',
        }
        enveloppe_requete = self.generateur.transmettre_commande(
            requete_cle_racine,
            'commande.millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.COMMANDE_RESTAURER_BACKUP_CLES,
            correlation_id='abcd-1234',
            reply_to=self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def commande_creer_cles_millegrille_hebergee(self):
        enveloppe_requete = self.generateur.transmettre_commande(
            dict(),
            'commande.millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.COMMANDE_CREER_CLES_MILLEGRILLE_HEBERGEE,
            correlation_id='abcd-1234',
            reply_to=self.queue_name,
            exchange=Constantes.DEFAUT_MQ_EXCHANGE_MIDDLEWARE
        )

        print("Envoi commande: %s" % enveloppe_requete)
        return enveloppe_requete

    def nouvelle_cle_grosfichiers(self):

        cle_secrete = 'Mon mot de passe secret'
        cle_secrete_encryptee = self.certificat_courant.public_key().encrypt(
            cle_secrete.encode('utf8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        cle_secrete_encryptee_mime64 = b64encode(cle_secrete_encryptee).decode('utf8')

        nouvelle_cle = {
            "domaine": "millegrilles.domaines.GrosFichiers",
            Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID: "39c1e1b0-b6ee-11e9-b0cd-d30e8faa841c",
            ConstantesMaitreDesCles.TRANSACTION_CHAMP_IDENTIFICATEURS_DOCUMENTS: {
                "fuuid": "39c1e1b0-b6ee-11e9-b0cd-d30e8faa851a",
            },
            "fingerprint": "abcd",
            "cle": cle_secrete_encryptee_mime64,
            "iv": "gA8cRaiJE+8aN2c6/N1vTg==",
        }

        enveloppe_val = self.generateur.soumettre_transaction(
            nouvelle_cle,
            ConstantesMaitreDesCles.TRANSACTION_NOUVELLE_CLE_GROSFICHIER,
            reply_to=self.queue_name,
            correlation_id='efgh'
        )

        print("Sent: %s" % enveloppe_val)
        return enveloppe_val

    def nouvelle_cle_document(self):

        cle_secrete = 'Mon mot de passe secret'
        cle_secrete_encryptee = self.certificat_courant.public_key().encrypt(
            cle_secrete.encode('utf8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        cle_secrete_encryptee_mime64 = b64encode(cle_secrete_encryptee).decode('utf8')

        nouvelle_cle = {
            "domaine": "millegrilles.domaines.Parametres",
            Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID: "39c1e1b0-b6ee-11e9-b0cd-d30e8faa841c",
            ConstantesMaitreDesCles.TRANSACTION_CHAMP_IDENTIFICATEURS_DOCUMENTS: {
                Constantes.DOCUMENT_INFODOC_LIBELLE: ConstantesParametres.LIBVAL_EMAIL_SMTP,
            },
            "fingerprint": "abcd",
            "cle": cle_secrete_encryptee_mime64,
            "iv": "gA8cRaiJE+8aN2c6/N1vTg==",
        }

        enveloppe_val = self.generateur.soumettre_transaction(
            nouvelle_cle,
            ConstantesMaitreDesCles.TRANSACTION_NOUVELLE_CLE_DOCUMENT,
            reply_to=self.queue_name,
            correlation_id='efgh'
        )

        print("Sent: %s" % enveloppe_val)
        return enveloppe_val

    def transaction_declasser_grosfichier(self):

        transaction = {
            'fuuid': '3830311b-145f-4ab2-850e-f4defdb70767'
        }

        enveloppe_val = self.generateur.soumettre_transaction(
            transaction,
            ConstantesMaitreDesCles.TRANSACTION_DECLASSER_CLE_GROSFICHIER,
            reply_to=self.queue_name,
            correlation_id='efgh'
        )

        print("Sent: %s" % enveloppe_val)
        return enveloppe_val

    def transaction_signer_certificat_navigateur(self):

        public_key_str = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqYE8pRzlFVwAgc2uB3ot6Ffd8pPpG4Sb8btFdjArvYcbuWvsRntBUgm/w6c831GpEoOrDr/EoEPRgTjJ81zxa1tkFprsmw9t8HJ0IOV9WF6p1X8gvf4FZaeLW6wTcA6LGhk1lRoN0jIr0VhNBejX4Xl7m7B1hR+pgmafG9Qm9acAZx2+opi9cYkG0lcl33R/106x8nnaF3jwjhBjFEazH5roHN9W253Y1subRXYC0Uq6SIlzN2HDPLn0oHLujAmf0NP6PrqHmDxfrnWc+KKuSJD2Dyf8w07AjJwJgpmWa9JrcqvYjR/BViI06/CqrtJpSAHpCguSQB3QbidSzbFF3wIDAQAB'

        transaction = {
            'sujet': 'test-domaine_MaitreDescLes',
            'cle_publique': public_key_str,
        }

        enveloppe_val = self.generateur.soumettre_transaction(
            transaction,
            ConstantesMaitreDesCles.TRANSACTION_GENERER_CERTIFICAT_NAVIGATEUR,
            reply_to=self.queue_name,
            correlation_id='efgh'
        )

        print("Sent: %s" % enveloppe_val)
        return enveloppe_val

    def transaction_demande_inscription_tierce(self):
        transaction = {
            'idmg': '33KRMhqcWCKvMHyY5xymMCUEbT53Kg1NqUb9AU6'
        }
        domaine = ConstantesMaitreDesCles.TRANSACTION_GENERER_DEMANDE_INSCRIPTION

        enveloppe_val = self.generateur.soumettre_transaction(
            transaction,
            domaine,
            reply_to=self.queue_name,
            correlation_id='efgh'
        )

        print("Sent: %s" % enveloppe_val)
        return enveloppe_val

    def transaction_signature_inscription_tierce(self):
        with open('/home/mathieu/PycharmProjects/MilleGrilles.consignation.python/test/messages/demande_connexion.json') as fichier:
            transaction = json.load(fichier)
        domaine = ConstantesMaitreDesCles.TRANSACTION_GENERER_CERTIFICAT_POUR_TIERS

        enveloppe_val = self.generateur.soumettre_transaction(
            transaction,
            domaine,
            reply_to=self.queue_name,
            correlation_id='efgh'
        )

        print("Sent: %s" % enveloppe_val)
        return enveloppe_val

    def transaction_supprimer_trousseau_hebergement(self):
        domaine = ConstantesMaitreDesCles.TRANSACTION_HEBERGEMENT_SUPPRIMER

        enveloppe_val = self.generateur.soumettre_transaction(
            {'idmg': '3M87pZxVVWbT1dVLeRarQnge1mvADTs4trG7Caa'},
            domaine,
            reply_to=self.queue_name,
            correlation_id='efgh'
        )

        print("Sent: %s" % enveloppe_val)
        return enveloppe_val

    def commande_signer_csr(self):
        clecert = EnveloppeCleCert()
        clecert.generer_private_key(generer_password=True, keysize=4096)

        public_key = clecert.private_key.public_key()
        builder = x509.CertificateSigningRequestBuilder()
        name = x509.Name([
            x509.NameAttribute(x509.name.NameOID.ORGANIZATION_NAME, '3aeGLdmMbA1BrmRYwpPgNAZKH2WGWmSedBjKSxw'),
            x509.NameAttribute(x509.name.NameOID.ORGANIZATIONAL_UNIT_NAME, 'domaines'),
            x509.NameAttribute(x509.name.NameOID.COMMON_NAME, 'test')
        ])
        builder = builder.subject_name(name)
        request = builder.sign(
            clecert.private_key, hashes.SHA256(), default_backend()
        )
        request_pem = request.public_bytes(primitives.serialization.Encoding.PEM)

        commande = {
            'liste_csr': [request_pem.decode('utf-8')],
        }
        enveloppe_requete = self.generateur.transmettre_commande(
            commande,
            'commande.millegrilles.domaines.MaitreDesCles.%s' % ConstantesMaitreDesCles.COMMANDE_SIGNER_CSR,
            correlation_id='abcd-1234',
            reply_to=self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def commande_signer_csr_noeud_prive(self):
        clecert = EnveloppeCleCert()
        clecert.generer_private_key(keysize=2048)

        public_key = clecert.private_key.public_key()
        builder = x509.CertificateSigningRequestBuilder()
        name = x509.Name([
            # x509.NameAttribute(x509.name.NameOID.ORGANIZATION_NAME, '3aeGLdmMbA1BrmRYwpPgNAZKH2WGWmSedBjKSxw'),
            x509.NameAttribute(x509.name.NameOID.ORGANIZATIONAL_UNIT_NAME, 'intermediaire'),
            x509.NameAttribute(x509.name.NameOID.COMMON_NAME, str(uuid4()))
        ])
        builder = builder.subject_name(name)
        request = builder.sign(
            clecert.private_key, hashes.SHA256(), default_backend()
        )
        request_pem = request.public_bytes(primitives.serialization.Encoding.PEM)

        commande = {
            'liste_csr': [request_pem.decode('utf-8')],
            'role': 'prive'
        }
        enveloppe_requete = self.generateur.transmettre_commande(
            commande,
            'commande.MaitreDesCles.%s' % ConstantesMaitreDesCles.COMMANDE_SIGNER_CSR,
            correlation_id='abcd-1234',
            reply_to=self.queue_name
        )

        print("Envoi requete: %s" % enveloppe_requete)
        return enveloppe_requete

    def executer(self):
        # self.event_recu.wait(5)
        # self.event_recu.clear()

        # enveloppe = self.requete_cert_maitredescles()
        # self.requete_trousseau_hebergement()

        # enveloppe = self.nouvelle_cle_grosfichiers()
        # enveloppe = self.nouvelle_cle_document()
        # enveloppe = self.transaction_declasser_grosfichier()
        # enveloppe = self.transaction_signer_certificat_navigateur()
        # enveloppe = self.requete_decryptage_cle_fuuid()
        # enveloppe = self.requete_decryptage_cle_fuuid_avecfingerprint()
        # self.transaction_demande_inscription_tierce()
        # self.transaction_signature_inscription_tierce()
        # self.transaction_supprimer_trousseau_hebergement()

        # self.requete_cle_racine()
        # self.commande_signer_cle_backup()
        # self.commande_restaurer_backup_cle()
        # self.commande_creer_cles_millegrille_hebergee()
        # self.commande_signer_csr()
        self.commande_signer_csr_noeud_prive()


# --- MAIN ---
sample = MessagesSample()

# TEST
# sample.executer()

# FIN TEST
sample.event_recu.wait(10)
sample.deconnecter()
