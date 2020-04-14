# Constantes de MilleGrillesPython
import datetime

LOGGING_FORMAT = '%(asctime)s %(threadName)s %(levelname)s: %(message)s'

CONFIG_FICHIER_JSON = 'mg_config_json'  # Fichier de configuration JSON a combiner avec les autres configurations

# Configuration MQ
CONFIG_MQ_HOST = 'mq_host'
CONFIG_MQ_PORT = 'mq_port'
CONFIG_MQ_VIRTUAL_HOST = 'mq_virtual_host'
# CONFIG_MQ_EXCHANGE_EVENEMENTS = 'mq_exchange_evenements'
CONFIG_MQ_EXCHANGE_MIDDLEWARE = 'mq_exchange_middleware'
CONFIG_MQ_EXCHANGE_PRIVE = 'mq_exchange_prive'
CONFIG_MQ_EXCHANGE_NOEUDS = 'mq_exchange_noeuds'
CONFIG_MQ_EXCHANGE_PUBLIC = 'mq_exchange_public'
CONFIG_MQ_USER = 'mq_user'
CONFIG_MQ_PASSWORD = 'mq_password'
CONFIG_MQ_HEARTBEAT = 'mq_heartbeat'
CONFIG_MQ_SSL = 'mq_ssl'
CONFIG_MQ_AUTH_CERT = 'mq_auth_cert'
CONFIG_MQ_KEYFILE = 'mq_keyfile'
CONFIG_MQ_CERTFILE = 'mq_certfile'
CONFIG_MQ_CA_CERTS = 'mq_ca_certs'

CONFIG_QUEUE_NOUVELLES_TRANSACTIONS = 'mq_queue_nouvelles_transactions'
CONFIG_QUEUE_EVENEMENTS_TRANSACTIONS = 'mq_queue_evenements_transactions'
CONFIG_QUEUE_ERREURS_TRANSACTIONS = 'mq_queue_erreurs_transactions'
CONFIG_QUEUE_MGP_PROCESSUS = 'mq_queue_mgp_processus'
CONFIG_QUEUE_ERREURS_PROCESSUS = 'mq_queue_erreurs_processus'
CONFIG_QUEUE_GENERATEUR_DOCUMENTS = 'mq_queue_generateur_documents'
CONFIG_QUEUE_NOTIFICATIONS = 'mq_queue_notifications'

CONFIG_BACKUP_WORKDIR = 'backup_workdir'

# DEFAUT_MQ_EXCHANGE_EVENEMENTS = 'millegrilles.evenements'
DEFAUT_MQ_EXCHANGE_MIDDLEWARE = 'millegrilles.middleware'
DEFAUT_MQ_EXCHANGE_NOEUDS = 'millegrilles.noeuds'
DEFAUT_MQ_EXCHANGE_PRIVE = 'millegrilles.prive'
DEFAUT_MQ_EXCHANGE_PUBLIC = 'millegrilles.public'
DEFAUT_MQ_VIRTUAL_HOST = '/'
DEFAUT_MQ_HEARTBEAT = '30'
DEFAUT_QUEUE_NOUVELLES_TRANSACTIONS = 'transactions.nouvelles'
DEFAUT_QUEUE_EVENEMENTS_TRANSACTIONS = 'transactions.evenements'
DEFAUT_QUEUE_ERREURS_TRANSACTIONS = 'erreurs_transactions'
DEFAUT_QUEUE_ENTRETIEN_TRANSACTIONS = 'transactions.entretien'
DEFAUT_QUEUE_MGP_PROCESSUS = 'mgp_processus'
DEFAUT_QUEUE_ERREURS_PROCESSUS = 'processus.erreurs'
DEFAUT_QUEUE_GENERATEUR_DOCUMENTS = 'generateur_documents'
DEFAUT_QUEUE_NOTIFICATIONS = 'notifications'

DEFAUT_HOSTNAME = 'localhost'
DEFAUT_KEYFILE = '/usr/local/etc/millegrilles/keys/pki.millegrilles.ssl.key'
DEFAUT_KEYCERTFILE = '/usr/local/etc/millegrilles/keys/pki.millegrilles.ssl.key_cert'
DEFAUT_CERTFILE = '/usr/local/etc/millegrilles/certs/pki.millegrilles.ssl.cert'
DEFAUT_CA_CERTS = '/opt/millegrilles/etc/millegrilles.RootCA.pem'

DEFAUT_CONSIGNATIONFICHIERS_HOST = 'consignationfichiers'
DEFAUT_CONSIGNATIONFICHIERS_PORT = '443'

DEFAUT_BACKUP_WORKDIR = '/tmp/mgbackup'

# Configuration Mongo
CONFIG_MONGO_HOST = 'mongo_host'
CONFIG_MONGO_PORT = 'mongo_port'
CONFIG_MONGO_USER = 'mongo_username'
CONFIG_MONGO_PASSWORD = 'mongo_password'
CONFIG_MONGO_SSL = 'mongo_ssl'
CONFIG_MONGO_SSL_CAFILE = 'mongo_ssl_ca_certs'
CONFIG_MONGO_SSL_KEYFILE = 'mongo_ssl_certfile'

MONGO_DOC_ID = '_id'

# Configuration MilleGrilles
CONFIG_IDMG = 'idmg'

# Domaines
CONFIG_DOMAINES_CONFIGURATION = 'domaines_json'
LIBVAL_CONFIGURATION = 'configuration'

# Email notifications
CONFIG_EMAIL_HOST = 'email_host'
CONFIG_EMAIL_PORT = 'email_port'
CONFIG_EMAIL_USER = 'email_user'
CONFIG_EMAIL_PASSWORD = 'email_password'
CONFIG_EMAIL_TO = 'email_to'
CONFIG_EMAIL_FROM = 'email_from'

# Serveurs et liens externes
CONFIG_SERVEUR_CONSIGNATIONFICHIERS_HOST = 'consignationfichiers_host'
CONFIG_SERVEUR_CONSIGNATIONFICHIERS_PORT = 'consignationfichiers_port'

# Valeurs par defaut
DEFAUT_MQ_USER = 'transaction'
DEFAUT_IDMG = 'sansnom'

# PKI
CONFIG_PKI_WORKDIR = 'pki_workdir'
CONFIG_MAITREDESCLES_DIR = 'maitredescles_dir'
CONFIG_PKI_SECRET_DIR = 'pki_secrets'
CONFIG_CA_PASSWORDS = 'pki_ca_passwords'
CONFIG_PKI_CERT_MILLEGRILLE = 'pki_cert_millegrille'
CONFIG_PKI_KEY_MILLEGRILLE = 'pki_key_millegrille'
CONFIG_PKI_PASSWORD_MILLEGRILLE = 'pki_password_millegrille'
CONFIG_PKI_CERT_AUTORITE = 'pki_cert_autorite'
CONFIG_PKI_KEY_AUTORITE = 'pki_key_autorite'
CONFIG_PKI_PASSWORD_AUTORITE = 'pki_password_millegrille'
CONFIG_PKI_CERT_MAITREDESCLES = 'pki_cert_maitredescles'
CONFIG_PKI_KEY_MAITREDESCLES = 'pki_key_maitredescles'
CONFIG_PKI_PASSWORD_MAITREDESCLES = 'pki_password_maitredescles'

DEFAUT_PKI_WORKDIR = '/opt/millegrilles/dist/secure/pki'
DEFAUT_MAITREDESCLES_DIR = '/opt/millegrilles/dist/secure/maitredescles'
DEFAUT_PKI_SECRET_DIR = '/run/secrets'
DEFAULT_CA_PASSWORDS = 'pki.ca.passwords'
DEFAUT_PKI_CERT_MILLEGRILLE = 'pki.millegrille.cert'
DEFAUT_PKI_KEY_MILLEGRILLE = 'pki.millegrille.key'
DEFAUT_PKI_PASSWORD_MILLEGRILLE = 'pki.millegrille.password.txt'
DEFAUT_PKI_CERT_AUTORITE = 'pki.racine.cert'
DEFAUT_PKI_KEY_AUTORITE = 'pki.racine.key'
DEFAUT_PKI_PASSWORD_AUTORITE = 'pki.autorite.password.txt'
DEFAUT_PKI_CERT_MAITREDESCLES = 'pki.maitredescles.cert.pem'
DEFAUT_PKI_KEY_MAITREDESCLES = 'pki.maitredescles.key.pem'
DEFAUT_PKI_PASSWORD_MAITREDESCLES = 'pki.maitredescles.password.txt'

# Environnement
PREFIXE_ENV_MG = 'MG_'

TRANSACTION_MESSAGE_LIBELLE_IDMG = CONFIG_IDMG
TRANSACTION_MESSAGE_LIBELLE_IDMG_DESTINATION = 'destination'
# TRANSACTION_MESSAGE_LIBELLE_SOURCE_SYSTEME = 'source-systeme'   # Remplace par idmg
TRANSACTION_MESSAGE_LIBELLE_ID_MONGO = '_id-transaction'
TRANSACTION_MESSAGE_LIBELLE_UUID = 'uuid-transaction'
TRANSACTION_MESSAGE_LIBELLE_EVENEMENT = '_evenements'  # Precedemment evenements (sans underscore)
TRANSACTION_MESSAGE_LIBELLE_ORIGINE = '_akid'
TRANSACTION_MESSAGE_LIBELLE_ESTAMPILLE = 'estampille'
TRANSACTION_MESSAGE_LIBELLE_SIGNATURE = '_signature'
TRANSACTION_MESSAGE_LIBELLE_CONTRESIGNATURES = '_contresignatures'
TRANSACTION_MESSAGE_LIBELLE_CONTRESIGNATURE = 'signature'
TRANSACTION_MESSAGE_LIBELLE_INFO_TRANSACTION = 'en-tete'  # Precedemment info-transaction
TRANSACTION_MESSAGE_LIBELLE_EN_TETE = 'en-tete'
# TRANSACTION_MESSAGE_LIBELLE_CHARGE_UTILE = 'charge-utile'  # Deprecated
TRANSACTION_MESSAGE_LIBELLE_DOMAINE = 'domaine'
TRANSACTION_MESSAGE_LIBELLE_CERTIFICAT = 'certificat'
TRANSACTION_MESSAGE_LIBELLE_HACHAGE = 'hachage-contenu'
TRANSACTION_MESSAGE_LIBELLE_VERSION = 'version'
TRANSACTION_MESSAGE_LIBELLE_VERSION_6 = 6
TRANSACTION_MESSAGE_LIBELLE_VERSION_COURANTE = TRANSACTION_MESSAGE_LIBELLE_VERSION_6
TRANSACTION_MESSAGE_LIBELLE_PROPERTIES_MQ = 'properties'
TRANSACTION_MESSAGE_LIBELLE_RESOUMISSIONS = 'resoumissions'

TRANSACTION_ROUTING_NOUVELLE = 'transaction.nouvelle'
TRANSACTION_ROUTING_EVENEMENT = 'transaction.evenement'
TRANSACTION_ROUTING_EVENEMENTTOKEN = 'transaction.evenementToken'
TRANSACTION_ROUTING_EVENEMENTRESET = 'transaction.evenementReset'
TRANSACTION_ROUTING_RESTAURER = 'transaction.restaurer'
TRANSACTION_ROUTING_DOCINITIAL = 'docInitial'
TRANSACTION_ROUTING_UPDATE_DOC = 'updateDoc'
PROCESSUS_DOCUMENT_LIBELLE_MOTEUR = 'moteur'
PROCESSUS_MESSAGE_LIBELLE_PROCESSUS = 'processus'
PROCESSUS_MESSAGE_LIBELLE_NOMETAPE = 'nom-etape'
PROCESSUS_MESSAGE_LIBELLE_ETAPESUIVANTE = 'etape-suivante'
PROCESSUS_MESSAGE_LIBELLE_ID_DOC_PROCESSUS = '_id_document_processus'
PROCESSUS_MESSAGE_LIBELLE_PARAMETRES = 'parametres'
PROCESSUS_MESSAGE_LIBELLE_COLLECTION_DONNEES = 'collection_donnees'

PROCESSUS_MESSAGE_LIBELLE_ID_DOC_PROCESSUS_DECLENCHEUR = '_id_document_processus_declencheur'
PROCESSUS_MESSAGE_LIBELLE_ID_DOC_PROCESSUS_ATTENTE = '_id_document_processus_attente'
PROCESSUS_MESSAGE_LIBELLE_RESUMER_TOKENS = 'resumer_tokens'

PROCESSUS_DOCUMENT_LIBELLE_PROCESSUS = PROCESSUS_MESSAGE_LIBELLE_PROCESSUS
PROCESSUS_DOCUMENT_LIBELLE_ETAPESUIVANTE = PROCESSUS_MESSAGE_LIBELLE_ETAPESUIVANTE
PROCESSUS_DOCUMENT_LIBELLE_ETAPES = 'etapes'
PROCESSUS_DOCUMENT_LIBELLE_NOMETAPE = 'nom-etape'
PROCESSUS_DOCUMENT_LIBELLE_PARAMETRES = PROCESSUS_MESSAGE_LIBELLE_PARAMETRES
PROCESSUS_DOCUMENT_LIBELLE_DATEEXECUTION = 'date'
PROCESSUS_DOCUMENT_LIBELLE_TOKENS = 'tokens'
PROCESSUS_DOCUMENT_LIBELLE_TOKEN_ATTENTE = 'attente_token'
PROCESSUS_DOCUMENT_LIBELLE_TOKEN_RESUMER = 'resumer_token'
PROCESSUS_DOCUMENT_LIBELLE_TOKEN_CONNECTES = 'connecte_token'
PROCESSUS_DOCUMENT_LIBELLE_RESUMER_COMPTEUR = 'resumer_compteur'
PROCESSUS_DOCUMENT_LIBELLE_INFO = 'info'

# Documents (collections)
DOCUMENT_COLLECTION_TRANSACTIONS = 'transactions'
DOCUMENT_COLLECTION_PROCESSUS = 'processus'
DOCUMENT_COLLECTION_INFORMATION_DOCUMENTS = 'information-documents'
DOCUMENT_COLLECTION_INFORMATION_GENEREE = 'information-generee'

# Collections
COLLECTION_TRANSACTION_STAGING = 'transactions.staging'

# DOCUMENT_INFODOC_CHEMIN = '_mg-chemin'
# DOCUMENT_INFODOC_UUID = '_mg-uuid-doc'
DOCUMENT_INFODOC_LIBELLE = '_mg-libelle'
DOCUMENT_INFODOC_DERNIERE_MODIFICATION = '_mg-derniere-modification'
DOCUMENT_INFODOC_DATE_CREATION = '_mg-creation'
DOCUMENT_INFODOC_SOUSDOCUMENT = 'document'

# Section cryptee d'un document
DOCUMENT_SECTION_CRYPTE = 'crypte'

# Evenements
EVENEMENT_MESSAGE_EVENEMENT = 'evenement'
EVENEMENT_MESSAGE_EVENEMENT_TOKEN = 'evenement_token'
EVENEMENT_MESSAGE_TYPE_TOKEN = 'type_token'
EVENEMENT_MESSAGE_TOKEN = 'token'
EVENEMENT_MESSAGE_EVENEMENTS = 'evenements'
EVENEMENT_MESSAGE_UNSET = 'unset'
EVENEMENT_MESSAGE_EVENEMENT_TIMESTAMP = 'timestamp'
EVENEMENT_TRANSACTION_NOUVELLE = 'transaction_nouvelle'
EVENEMENT_TRANSACTION_ESTAMPILLE = '_estampille'
EVENEMENT_TRANSACTION_COMPLETE = 'transaction_complete'
EVENEMENT_TRANSACTION_TRAITEE = 'transaction_traitee'
EVENEMENT_TRANSACTION_PERSISTEE = 'transaction_persistee'
EVENEMENT_TRANSACTION_ERREUR_TRAITEMENT = 'erreur_traitement'
EVENEMENT_TRANSACTION_ERREUR_EXPIREE = 'erreur_expiree'
EVENEMENT_TRANSACTION_ERREUR_RESOUMISSION = 'erreur_resoumission'
EVENEMENT_TRANSACTION_BACKUP_FLAG = 'backup_flag'
EVENEMENT_TRANSACTION_BACKUP_HORAIRE_COMPLETE = 'backup_horaire'
EVENEMENT_TRANSACTION_BACKUP_ERREUR = 'backup_erreur'
EVENEMENT_TRANSACTION_BACKUP_RESTAURE = 'transaction_restauree'
EVENEMENT_DOCUMENT_PERSISTE = 'document_persiste'
EVENEMENT_SIGNATURE_VERIFIEE = 'signature_verifiee'
EVENEMENT_TRANSACTION_DATE_RESOUMISE = 'resoumise'
EVENEMENT_TRANSACTION_COMPTE_RESOUMISE = 'compte_resoumise'
EVENEMENT_DOCUMENT_MAJ = 'document_maj'
EVENEMENT_DOCUMENT_SUPPRIME = 'document_supprime'
EVENEMENT_DOCUMENT_AJOUTE = 'document_ajoute'
EVENEMENT_CEDULEUR = 'ceduleur'
EVENEMENT_NOTIFICATION = 'notification'
EVENEMENT_RESUMER = 'resumer'
EVENEMENT_REPONSE = 'reponse'
EVENEMENT_VERIFIER_RESUMER = 'verifier.resumer'
EVENEMENT_PKI = 'pki'

EVENEMENT_TOKEN_ATTENTE = 'attente'
EVENEMENT_TOKEN_RESUMER = 'resumer'
EVENEMENT_TOKEN_CONNECTE = 'connecte'

DOCUMENT_TACHE_NOTIFICATION = 'tache_notification'

SECURITE_PUBLIC = '1.public'    # Niveau 1, le moins securitaire. Accessible a n'importe qui.
SECURITE_PRIVE = '2.prive'      # Niveau 2, accessible aux personnes authentifiees
SECURITE_PROTEGE = '3.protege'  # Niveau 3, accessible aux personnes autorisees (delegues, autorise individuellement)
SECURITE_SECURE = '4.secure'    # Niveau 4, accessible uniquement a l'usager et aux delegues directs

SECURITE_LIBELLE_REPONSE = 'acces'
SECURITE_ACCES_REFUSE = '0.refuse'
SECURITE_ACCES_PERMIS = '1.permis'
SECURITE_ACCES_ERREUR = '2.erreur'

CLE_CERT_CA = 'pki.millegrille'


class ConstantesSecurite:

    EXCHANGE_SECURE = 'millegrilles.middleware'
    EXCHANGE_PROTEGE = 'millegrilles.noeuds'
    EXCHANGE_PRIVE = 'millegrilles.prive'
    EXCHANGE_PUBLIC = 'millegrilles.public'


class ConstantesDomaines:

    COMMANDE_REGENERER = 'regenerer'
    COMMANDE_GLOBAL_REGENERER = 'commande.global.regenerer'


class ConstantesPrincipale:
    """ Constantes pour le domaine de l'interface principale """

    DOMAINE_NOM = 'millegrilles.domaines.Principale'
    COLLECTION_TRANSACTIONS_NOM = DOMAINE_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_TRANSACTIONS_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_TRANSACTIONS_NOM
    QUEUE_NOM = 'millegrilles.domaines.Principale'

    LIBVAL_CONFIGURATION = 'configuration'
    LIBVAL_PROFIL_USAGER = 'profil.usager'
    LIBVAL_PROFIL_MILLEGRILLE = 'profil.millegrille'
    LIBVAL_ALERTES = 'alertes'
    LIBVAL_DOMAINES = 'domaines'
    LIBVAL_CLES = 'cles'

    LIBELLE_NOM = 'nom'
    LIBELLE_PRENOM = 'prenom'
    LIBELLE_COURRIEL = 'courriel'
    LIBELLE_TWITTER = 'twitter'
    LIBELLE_FACEBOOK = 'facebook'
    LIBELLE_NOM_MILLEGRILLE = 'nomMilleGrille'
    LIBELLE_NOM_MILLEGRILLE_PAR_LANGUE = 'nomMilleGrilleParLangue'
    LIBELLE_LANGUE_PRINCIPALE = 'langue'
    LIBELLE_LANGUES_ADDITIONNELLES = 'languesAdditionnelles'
    LIBELLE_DOMAINES = 'domaines'
    LIBELLE_MENU = 'menu'

    TRANSACTION_ACTION_FERMERALERTE = '%s.fermerAlerte' % DOMAINE_NOM
    TRANSACTION_ACTION_CREERALERTE = '%s.creerAlerte' % DOMAINE_NOM
    TRANSACTION_ACTION_CREEREMPREINTE = '%s.creerEmpreinte' % DOMAINE_NOM
    TRANSACTION_ACTION_AJOUTER_TOKEN = '%s.ajouterToken' % DOMAINE_NOM
    TRANSACTION_ACTION_MAJ_PROFILUSAGER = '%s.majProfilUsager' % DOMAINE_NOM
    TRANSACTION_ACTION_MAJ_PROFILMILLEGRILLE = '%s.majProfilMilleGrille' % DOMAINE_NOM
    TRANSACTION_MAJ_MENU = '%s.majMenu' % DOMAINE_NOM

    DOCUMENT_ALERTES = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_ALERTES,
        'alertes': [
            {'message': "Interface principale initialisee", 'ts': int(datetime.datetime.utcnow().timestamp()*1000)}
        ]
    }

    DOCUMENT_CLES = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CLES,
        'cles': [],
        'challenge_authentification': None,
        'empreinte_absente': True,
    }

    DOCUMENT_DOMAINES = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_DOMAINES,
        LIBVAL_DOMAINES: {
            'SenseursPassifs': {
                'rang': 5,
                'description': 'SenseursPassifs'
            },
            'GrosFichiers': {
                'rang': 3,
                'description': 'GrosFichiers'
            },
            'Principale': {
                'rang': 1,
                'description': 'Principale'
            },
            'Plume': {
                'rang': 1,
                'description': 'Plume'
            },
            'Pki': {
                'rang': 1,
                'description': 'Pki'
            },
            'Parametres': {
                'rang': 1,
                'description': 'Parametres'
            },
            'Annuaire': {
                'rang': 1,
                'description': 'Annuaire'
            },
            'Backup': {
                'rang': 1,
                'description': 'Backup'
            }
        },
        "menu": [
            'Principale',
            'Annuaire',
            'GrosFichiers',
            'Plume',
            'SenseursPassifs',
            'Pki',
            'Parametres',
            'Backup',
        ]
    }

    # Document par defaut pour la configuration de l'interface principale
    DOCUMENT_DEFAUT = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION,
        TRANSACTION_MESSAGE_LIBELLE_VERSION: 7,
    }

    DOCUMENT_PROFIL_USAGER = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_PROFIL_USAGER,
        LIBELLE_COURRIEL: None,
        LIBELLE_PRENOM: None,
        LIBELLE_NOM: None,
        LIBELLE_TWITTER: None,
        LIBELLE_FACEBOOK: None,
    }

    DOCUMENT_PROFIL_MILLEGRILLE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_PROFIL_MILLEGRILLE,
        LIBELLE_NOM_MILLEGRILLE: 'Sans nom',
        LIBELLE_LANGUE_PRINCIPALE: None,
        LIBELLE_LANGUES_ADDITIONNELLES: list(),
    }


class ConstantesSecurityPki:

    DELIM_DEBUT_CERTIFICATS = '-----BEGIN CERTIFICATE-----'
    COLLECTION_NOM = 'millegrilles.domaines.Pki/documents'

    LIBELLE_CERTIFICAT_PEM = 'certificat_pem'
    LIBELLE_FINGERPRINT = 'fingerprint'
    LIBELLE_CHAINE_PEM = 'chaine_pem'
    LIBELLE_CA_APPROUVE = 'ca_approuve'
    LIBELLE_IDMG = 'idmg'
    LIBELLE_CORRELATION_CSR = 'csr_correlation'

    EVENEMENT_CERTIFICAT = 'pki.certificat'  # Indique que c'est un evenement avec un certificat (reference)
    EVENEMENT_REQUETE = 'pki.requete'  # Indique que c'est une requete pour trouver un certificat par fingerprint

    LIBVAL_CERTIFICAT_RACINE = 'certificat.root'
    LIBVAL_CERTIFICAT_MILLEGRILLE = 'certificat.millegrille'
    LIBVAL_CERTIFICAT_NOEUD = 'certificat.noeud'

    REQUETE_CORRELATION_CSR = 'pki.correlation_csr'

    REGLE_LIMITE_CHAINE = 4  # Longeur maximale de la chaine de certificats

    SYMETRIC_PADDING = 128

    ROLE_CONNECTEUR = 'connecteur'
    ROLE_MAITREDESCLES = 'maitrecles'

    # Document utilise pour publier un certificat
    DOCUMENT_EVENEMENT_CERTIFICAT = {
        EVENEMENT_MESSAGE_EVENEMENT: EVENEMENT_CERTIFICAT,
        LIBELLE_FINGERPRINT: None,
        LIBELLE_CERTIFICAT_PEM: None
    }


class ConstantesPki:
    DOMAINE_NOM = 'millegrilles.domaines.Pki'
    COLLECTION_TRANSACTIONS_NOM = 'millegrilles.domaines.Pki'
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_TRANSACTIONS_NOM
    COLLECTION_PROCESSUS_NOM = 'millegrilles.domaines.Pki/processus'
    QUEUE_NOM = DOMAINE_NOM
    QUEUE_NOM_CERTIFICATS = '%s.certificats' % QUEUE_NOM

    TRANSACTION_DOMAINE_NOUVEAU_CERTIFICAT = '%s.nouveauCertificat' % DOMAINE_NOM
    TRANSACTION_WEB_NOUVEAU_CERTIFICAT = '%s.nouveauCertificat.web' % DOMAINE_NOM
    TRANSACTION_CLES_RECUES = '%s.clesRecues' % DOMAINE_NOM
    TRANSACTION_RENOUVELLER_CERT_DOCKER = '%s.renouvellerCertDocker' % DOMAINE_NOM

    LIBELLE_CERTIFICAT_PEM = ConstantesSecurityPki.LIBELLE_CERTIFICAT_PEM
    LIBELLE_FINGERPRINT = ConstantesSecurityPki.LIBELLE_FINGERPRINT
    LIBELLE_IDMG = 'idmg'
    LIBELLE_FINGERPRINT_ISSUER = 'fingerprint_issuer'
    LIBELLE_DOCID_ISSUER = '_id_issuer'
    LIBELLE_CHAINE_COMPLETE = 'chaine_complete'
    LIBELLE_SUBJECT = 'sujet'
    LIBELLE_ISSUER = 'issuer'
    LIBELLE_NOT_VALID_BEFORE = 'not_valid_before'
    LIBELLE_NOT_VALID_AFTER = 'not_valid_after'
    LIBELLE_SUBJECT_KEY = 'subject_key'
    LIBELLE_AUTHORITY_KEY = 'authority_key'
    LIBELLE_TRANSACTION_FAITE = 'transaction_faite'
    LIBELLE_CHAINES = 'chaines'
    LIBELLE_MGLIBELLE = 'mg-libelle'
    LIBELLE_CLE_CRYPTEE = 'cle_cryptee'
    LIBELLE_ROLES = 'roles'
    LIBELLE_EXCHANGES = 'exchanges'

    LIBVAL_CONFIGURATION = 'configuration'
    LIBVAL_CERTIFICAT_ROOT = 'certificat.root'
    LIBVAL_CERTIFICAT_INTERMEDIAIRE = 'certificat.intermediaire'
    LIBVAL_CERTIFICAT_MILLEGRILLE = 'certificat.millegrille'
    LIBVAL_CERTIFICAT_NOEUD = 'certificat.noeud'
    LIBVAL_CERTIFICAT_BACKUP = 'certificat.backup'
    LIBVAL_LISTE_CERTIFICATS_BACKUP = 'liste.certificats.backup'
    LIBVAL_PKI_WEB = 'pki.web'
    LIBVAL_CONFIG_CERTDOCKER = 'configuration.certdocker'

    CHAMP_ALT_DOMAINS = 'altdomains'
    CHAMP_ROLES = 'roles'

    REQUETE_CONFIRMER_CERTIFICAT = 'confirmerCertificat'
    REQUETE_CERTIFICAT_EMIS = 'pki.certificat'
    REQUETE_CERTIFICAT_DEMANDE = 'certificat'
    REQUETE_CERTIFICAT_BACKUP = 'certificatBackup'
    REQUETE_LISTE_CA = 'pki.requete.ca'
    TRANSACTION_EVENEMENT_CERTIFICAT = 'certificat'  # Indique que c'est une transaction avec un certificat a ajouter

    # Indique que c'est un evenement avec un certificat (reference)
    EVENEMENT_CERTIFICAT = ConstantesSecurityPki.EVENEMENT_CERTIFICAT
    # Indique que c'est une requete pour trouver un certificat par fingerprint
    EVENEMENT_REQUETE = ConstantesSecurityPki.EVENEMENT_REQUETE

    # Document par defaut pour la configuration de l'interface principale
    DOCUMENT_DEFAUT = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION,
        LIBELLE_FINGERPRINT: LIBVAL_CONFIGURATION,
    }

    DOCUMENT_CERTIFICAT_NOEUD = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CERTIFICAT_NOEUD,
        LIBELLE_CERTIFICAT_PEM: '',
        LIBELLE_FINGERPRINT: '',
        LIBELLE_CHAINE_COMPLETE: False
    }

    DOCUMENT_CONFIG_CERTDOCKER = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIG_CERTDOCKER,
        LIBELLE_FINGERPRINT: LIBVAL_CONFIG_CERTDOCKER,
        CHAMP_ALT_DOMAINS: dict(),
    }


class ConstantesParametres:

    DOMAINE_NOM = 'millegrilles.domaines.Parametres'
    COLLECTION_NOM = DOMAINE_NOM

    COLLECTION_TRANSACTIONS_NOM = COLLECTION_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_NOM
    COLLECTION_ERREURS = '%s/erreurs' % COLLECTION_NOM
    QUEUE_NOM = DOMAINE_NOM
    QUEUE_ROUTING_CHANGEMENTS = 'noeuds.source.millegrilles_domaines_Parametres.documents'

    TRANSACTION_MODIFIER_EMAIL_SMTP = '%s.modifierEmailSmtp' % DOMAINE_NOM
    TRANSACTION_CLES_RECUES = '%s.clesRecues' % DOMAINE_NOM
    TRANSACTION_ETAT_ROUTEUR = '%s.public.routeur.etatRouteur' % DOMAINE_NOM
    TRANSACTION_EXPOSER_PORTS_ROUTEUR = '%s.public.routeur.exposerPorts' % DOMAINE_NOM
    TRANSACTION_RETIRER_PORTS_ROUTEUR = '%s.public.routeur.retirerPorts' % DOMAINE_NOM
    TRANSACTION_CONFIRMATION_ROUTEUR = '%s.public.routeur.confirmerAction' % DOMAINE_NOM
    TRANSACTION_SAUVER_CONFIG_PUBLIC = '%s.public.sauvegarder' % DOMAINE_NOM
    TRANSACTION_DEPLOYER_ACCES_PUBLIC = '%s.public.deployer' % DOMAINE_NOM
    TRANSACTION_RETIRER_ACCES_PUBLIC = '%s.public.retirer' % DOMAINE_NOM
    TRANSACTION_RENOUVELLER_CERTIFICAT_PUBLIC = '%s.public.renouvellerCertificat' % DOMAINE_NOM
    TRANSACTION_MAJ_CERTIFICAT_PUBLIC = '%s.public.majCertificat' % DOMAINE_NOM
    TRANSACTION_PRIVATISER_NOEUD = '%s.public.privatiser' % DOMAINE_NOM
    TRANSACTION_FERMER_MILLEGRILLE = '%s.fermerMilleGrilles' % DOMAINE_NOM
    TRANSACTION_MAJ_NOEUD_PUBLIC = '%s.majNoeudPublic' % DOMAINE_NOM
    TRANSACTION_SUPPRIMER_NOEUD_PUBLIC = '%s.supprimerNoeudPublic' % DOMAINE_NOM
    TRANSACTION_RECEPTION_CLES_MAJNOEUDPUBLIC = '%s.majNoeudPublic.clesRecues' % DOMAINE_NOM

    TRANSACTION_CHAMP_MGLIBELLE = 'mg-libelle'
    TRANSACTION_CHAMP_UUID = 'uuid'

    REQUETE_NOEUD_PUBLIC = DOMAINE_NOM + '.noeudPublic'
    REQUETE_ERREURS = DOMAINE_NOM + '.erreurs'
    REQUETE_SUPPRIMER_ERREUR = DOMAINE_NOM + '.supprimerErreur'

    # Courriel
    DOCUMENT_CHAMP_COURRIEL_ORIGINE = 'origine'
    DOCUMENT_CHAMP_COURRIEL_DESTINATIONS = 'destinations'
    DOCUMENT_CHAMP_HOST = 'host'
    DOCUMENT_CHAMP_PORT = 'port'
    DOCUMENT_CHAMP_USER = 'user'
    DOCUMENT_CHAMP_PASSWORD = 'password'
    DOCUMENT_CHAMP_IDMG = 'idmg'
    DOCUMENT_CHAMP_URL_BASE = 'adresse_url_base'
    DOCUMENT_CHAMP_ACTIF = 'actif'

    DOCUMENT_CHAMP_MODE_DEPLOIEMENT = 'mode_deploiement'

    DOCUMENT_CHAMP_AWS_ACCESS_KEY = 'awsAccessKeyId'
    DOCUMENT_CHAMP_AWS_SECRET_KEY_CHIFFRE = 'awsSecretAccessKeyChiffre'
    DOCUMENT_CHAMP_AWS_CRED_REGION = 'awsCredentialRegion'
    DOCUMENT_CHAMP_AWS_BUCKET_NAME= 'awsBucketName'
    DOCUMENT_CHAMP_AWS_BUCKET_REGION = 'awsBucketRegion'
    DOCUMENT_CHAMP_AWS_BUCKET_URL = 'awsBucketUrl'
    DOCUMENT_CHAMP_AWS_BUCKET_DIR = 'awsBucketDir'

    TOKEN_ATTENTE_CLE = 'confirmer_reception_cle'

    LIBVAL_CONFIGURATION = 'configuration'
    LIBVAL_EMAIL_SMTP = 'email.stmp'
    LIBVAL_VERSIONS_IMAGES_DOCKER = 'versions.images.docker'
    LIBVAL_CERTS_WEB = 'certs.web'
    LIBVAL_CERTS_SSL = 'certs.ssl'
    LIBVAL_ID_MILLEGRILLE = 'millegrille.id'
    LIBVAL_CONFIGURATION_NOEUDPUBLIC = 'configuration.noeudPublic'

    # Configuration Publique
    LIBVAL_CONFIGURATION_PUBLIQUE = 'publique.configuration'
    DOCUMENT_PUBLIQUE_ACTIF = 'actif'
    DOCUMENT_PUBLIQUE_UPNP_SUPPORTE = 'upnp_supporte'
    DOCUMENT_PUBLIQUE_NOEUD_DOCKER = 'noeud_docker_hostname'
    DOCUMENT_PUBLIQUE_NOEUD_DOCKER_ID = 'noeud_docker_id'
    DOCUMENT_PUBLIQUE_URL_WEB = 'url_web'
    DOCUMENT_PUBLIQUE_URL_COUPDOEIL = 'url_coupdoeil'
    DOCUMENT_PUBLIQUE_URL_MQ = 'url_mq'
    DOCUMENT_PUBLIQUE_PORT_HTTP = 'port_http'
    DOCUMENT_PUBLIQUE_PORT_HTTPS = 'port_https'
    DOCUMENT_PUBLIQUE_PORT_MQ = 'port_mq'
    DOCUMENT_PUBLIQUE_PORT_EXTERIEUR = 'port_ext'
    DOCUMENT_PUBLIQUE_PORT_INTERNE = 'port_int'
    DOCUMENT_PUBLIQUE_IPV4_EXTERNE = 'ipv4_externe'
    DOCUMENT_PUBLIQUE_IPV4_INTERNE = 'ipv4_interne'
    DOCUMENT_PUBLIQUE_PROTOCOL = 'protocol'
    DOCUMENT_PUBLIQUE_PORT_MAPPING_NOM = 'port_mapping_nom'
    DOCUMENT_PUBLIQUE_MAPPINGS_IPV4 = 'mappings_ipv4'
    DOCUMENT_PUBLIQUE_MAPPINGS_IPV4_DEMANDES = 'mappings_ipv4_demandes'
    DOCUMENT_PUBLIQUE_ROUTEUR_STATUS = 'status_info'
    DOCUMENT_PUBLIQUE_ACTIVITE = 'activite'

    DOCUMENT_PUBLIQUE_ACTIVITE_DATE = 'date'
    DOCUMENT_PUBLIQUE_ACTIVITE_DESCRIPTION = 'description'

    DOCUMENT_PUBLIQUE_ACTIVITE_TAILLEMAX = 50

    DOCUMENT_PUBLIQUE_MENU = 'menu'

    DOCUMENT_DEFAUT = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION
    }

    DOCUMENT_ID_MILLEGRILLE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_ID_MILLEGRILLE,
        DOCUMENT_CHAMP_IDMG: 'Sansnom',
        DOCUMENT_CHAMP_URL_BASE: 'sansnom.millegrilles.com',
    }

    DOCUMENT_EMAIL_SMTP = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_EMAIL_SMTP,
        DOCUMENT_CHAMP_ACTIF: False,
        DOCUMENT_CHAMP_COURRIEL_ORIGINE: None,
        DOCUMENT_CHAMP_COURRIEL_DESTINATIONS: None,
        DOCUMENT_CHAMP_HOST: None,
        DOCUMENT_CHAMP_PORT: None,
        DOCUMENT_CHAMP_USER: None,
        DOCUMENT_SECTION_CRYPTE: None,  # DOCUMENT_CHAMP_PASSWORD
    }

    DOCUMENT_CONFIGURATION_PUBLIQUE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION_PUBLIQUE,
        DOCUMENT_PUBLIQUE_ACTIF: False,
        DOCUMENT_PUBLIQUE_NOEUD_DOCKER: None,
        DOCUMENT_PUBLIQUE_UPNP_SUPPORTE: False,
        DOCUMENT_PUBLIQUE_URL_WEB: None,
        DOCUMENT_PUBLIQUE_URL_MQ: None,
        DOCUMENT_PUBLIQUE_IPV4_EXTERNE: None,
        DOCUMENT_PUBLIQUE_ROUTEUR_STATUS: None,
        DOCUMENT_PUBLIQUE_PORT_HTTP: 80,
        DOCUMENT_PUBLIQUE_PORT_HTTPS: 443,
        DOCUMENT_PUBLIQUE_PORT_MQ: 5673,

        # Cle: port exterieur, Valeur: DOCUMENT_CONFIGURATION_PUBLIQUE_MAPPINGS
        DOCUMENT_PUBLIQUE_MAPPINGS_IPV4: dict(),
        DOCUMENT_PUBLIQUE_MAPPINGS_IPV4_DEMANDES: dict(),
        DOCUMENT_PUBLIQUE_ACTIVITE: list(),
    }

    DOCUMENT_CONFIGURATION_PUBLIQUE_MAPPINGS = {
        DOCUMENT_PUBLIQUE_PORT_EXTERIEUR: None,
        DOCUMENT_PUBLIQUE_IPV4_INTERNE: None,
        DOCUMENT_PUBLIQUE_PORT_INTERNE: None,
        DOCUMENT_PUBLIQUE_PORT_MAPPING_NOM: None,
    }

    DOCUMENT_CONFIGURATION_PUBLIQUE_ACTIVITE = {
        DOCUMENT_PUBLIQUE_ACTIVITE_DATE: datetime.datetime.utcnow(),
        DOCUMENT_PUBLIQUE_ACTIVITE_DESCRIPTION: '',
    }


class ConstantesMaitreDesCles:

    DOMAINE_NOM = 'millegrilles.domaines.MaitreDesCles'
    COLLECTION_NOM = DOMAINE_NOM

    COLLECTION_TRANSACTIONS_NOM = COLLECTION_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_NOM
    QUEUE_NOM = DOMAINE_NOM

    LIBVAL_CONFIGURATION = 'configuration'

    TRANSACTION_NOUVELLE_CLE_GROSFICHIER = '%s.nouvelleCle.grosFichier' % DOMAINE_NOM
    TRANSACTION_NOUVELLE_CLE_DOCUMENT = '%s.nouvelleCle.document' % DOMAINE_NOM
    TRANSACTION_MAJ_DOCUMENT_CLES = '%s.majcles' % DOMAINE_NOM

    TRANSACTION_DOMAINES_DOCUMENT_CLESRECUES = 'clesRecues'
    TRANSACTION_RENOUVELLEMENT_CERTIFICAT = '%s.renouvellementCertificat' % DOMAINE_NOM
    TRANSACTION_SIGNER_CERTIFICAT_NOEUD = '%s.signerCertificatNoeud' % DOMAINE_NOM
    TRANSACTION_GENERER_CERTIFICAT_NAVIGATEUR = '%s.genererCertificatNavigateur' % DOMAINE_NOM
    TRANSACTION_DECLASSER_CLE_GROSFICHIER = '%s.declasserCleGrosFichier' % DOMAINE_NOM
    TRANSACTION_GENERER_DEMANDE_INSCRIPTION = '%s.genererDemandeInscription' % DOMAINE_NOM
    TRANSACTION_GENERER_CERTIFICAT_POUR_TIERS = '%s.genererCertificatPourTiers' % DOMAINE_NOM

    REQUETE_CLE_RACINE = 'requeteCleRacine'
    REQUETE_CERT_MAITREDESCLES = 'certMaitreDesCles'
    REQUETE_DECRYPTAGE_DOCUMENT = 'decryptageDocument'
    REQUETE_DECRYPTAGE_GROSFICHIER = 'decryptageGrosFichier'

    COMMANDE_SIGNER_CLE_BACKUP = 'signerCleBackup'
    COMMANDE_RESTAURER_BACKUP_CLES = 'restaurerBackupCles'
    COMMANDE_CREER_CLES_MILLEGRILLE_HEBERGEE = 'creerClesMilleGrilleHebergee'

    CORRELATION_CERTIFICATS_BACKUP = 'certificatsBackup'

    TRANSACTION_CHAMP_CLESECRETE = 'cle'
    TRANSACTION_CHAMP_CLES = 'cles'
    TRANSACTION_CHAMP_IV = 'iv'
    TRANSACTION_CHAMP_SUJET_CLE = 'sujet'
    TRANSACTION_CHAMP_DOMAINE = 'domaine'
    TRANSACTION_CHAMP_DOMAINES = 'domaines'
    TRANSACTION_CHAMP_IDDOC = 'id-doc'
    TRANSACTION_CHAMP_IDENTIFICATEURS_DOCUMENTS = 'identificateurs_document'
    TRANSACTION_CHAMP_MGLIBELLE = 'mg-libelle'
    TRANSACTION_CHAMP_ROLE_CERTIFICAT = 'role'
    TRANSACTION_CHAMP_CSR = 'csr'
    TRANSACTION_CHAMP_CSR_CORRELATION = 'csr_correlation'
    TRANSACTION_CHAMP_TYPEDEMANDE = 'type_demande'
    TRANSACTION_CHAMP_FULLCHAIN = 'certificat_fullchain_signataire'

    TYPE_DEMANDE_INSCRIPTION = 'inscription'

    TRANSACTION_VERSION_COURANTE = 5

    DOCUMENT_LIBVAL_CLES_GROSFICHIERS = 'cles.grosFichiers'
    DOCUMENT_LIBVAL_CLES_DOCUMENT = 'cles.document'

    DOCUMENT_SECURITE = 'securite'

    DOCUMENT_DEFAUT = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION,
        TRANSACTION_MESSAGE_LIBELLE_VERSION: TRANSACTION_VERSION_COURANTE
    }

    # Document utilise pour conserver un ensemble de cles lie a un document
    DOCUMENT_CLES_GROSFICHIERS = {
        DOCUMENT_INFODOC_LIBELLE: DOCUMENT_LIBVAL_CLES_GROSFICHIERS,

        # Template a remplir
        'fuuid': None,    # Identificateur unique de version de fichier
        'cles': dict(),   # Dictionnaire indexe par fingerprint de certificat signataire. Valeur: cle secrete cryptee
    }

    DOCUMENT_TRANSACTION_CONSERVER_CLES = {
        TRANSACTION_CHAMP_SUJET_CLE: DOCUMENT_LIBVAL_CLES_GROSFICHIERS,  # Mettre le sujet approprie
        'cles': dict(),  # Dictionnaire indexe par fingerprint de certificat signataire. Valeur: cle secrete cryptee
    }

    DOCUMENT_TRANSACTION_GROSFICHIERRESUME = {
        'fuuid': None,  # Identificateur unique de version de fichier
    }


class ConstantesAnnuaire:

    DOMAINE_NOM = 'millegrilles.domaines.Annuaire'
    QUEUE_SUFFIXE = DOMAINE_NOM
    COLLECTION_TRANSACTIONS_NOM = QUEUE_SUFFIXE
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_TRANSACTIONS_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_TRANSACTIONS_NOM
    QUEUE_ROUTING_CHANGEMENTS = 'document.millegrilles_domaines_Annuaire'

    LIBVAL_INDEX_MILLEGRILLES = 'index.millegrilles'
    LIBVAL_FICHE_PRIVEE = 'fiche.privee'      # Fiche privee de la millegrille locale
    LIBVAL_FICHE_PUBLIQUE = 'fiche.publique'  # Fiche publique de la millegrille locale signee par le maitredescles
    LIBVAL_FICHE_TIERS = 'fiche.tiers'        # Fiche d'une MilleGrille tierce

    LIBELLE_DOC_LISTE = 'liste'
    LIBELLE_DOC_SECURITE = '_securite'
    LIBELLE_DOC_LIENS_PUBLICS_HTTPS = 'public_https'
    LIBELLE_DOC_LIENS_PRIVES_MQ = 'prive_mq'
    LIBELLE_DOC_LIENS_PRIVES_HTTPS = 'prive_https'
    LIBELLE_DOC_LIENS_RELAIS = 'relais'
    LIBELLE_DOC_USAGER = 'usager'
    LIBELLE_DOC_DESCRIPTIF = ConstantesPrincipale.LIBELLE_NOM_MILLEGRILLE
    LIBELLE_DOC_CERTIFICAT_RACINE = 'certificat_racine'
    LIBELLE_DOC_CERTIFICAT = 'certificat'
    LIBELLE_DOC_CERTIFICATS_INTERMEDIAIRES = 'certificats_intermediaires'
    LIBELLE_DOC_CERTIFICAT_ADDITIONNELS = 'certificats_additionnels'
    LIBELLE_DOC_EXPIRATION_INSCRIPTION = 'expiration_inscription'
    LIBELLE_DOC_RENOUVELLEMENT_INSCRIPTION = 'renouvellement_inscription'
    LIBELLE_DOC_ABONNEMENTS = 'abonnements'
    LIBELLE_DOC_NOMBRE_FICHES = 'nombre_fiches'
    LIBELLE_DOC_TYPE_FICHE = 'type'
    LIBELLE_DOC_FICHE_PRIVEE = 'fiche_privee'
    LIBELLE_DOC_FICHE_PUBLIQUE = 'fiche_publique'
    LIBELLE_DOC_DATE_DEMANDE = 'date'
    LIBELLE_DOC_DEMANDES_TRANSMISES = 'demandes_transmises'
    LIBELLE_DOC_DEMANDES_RECUES = 'demandes_recues'
    LIBELLE_DOC_DEMANDES_CSR = 'csr'
    LIBELLE_DOC_DEMANDES_CORRELATION = 'csr_correlation'
    LIBELLE_DOC_DEMANDES_ORIGINALE = 'demande_originale'
    LIBELLE_DOC_IDMG_SOLLICITE = 'idmg_sollicite'
    LIBELLE_DOC_EXPIRATION = 'expiration_inscription'
    LIBELLE_DOC_INSCRIPTIONS_TIERS_VERS_LOCAL = 'inscriptions_tiers'
    LIBELLE_DOC_INSCRIPTIONS_LOCAL_VERS_TIERS = 'inscriptions_local'

    TRANSACTION_MAJ_FICHEPRIVEE = '%s.maj.fichePrivee' % DOMAINE_NOM
    TRANSACTION_MAJ_FICHEPUBLIQUE = '%s.maj.fichePublique' % DOMAINE_NOM
    TRANSACTION_MAJ_FICHETIERCE = '%s.maj.ficheTierce' % DOMAINE_NOM
    TRANSACTION_DEMANDER_INSCRIPTION = '%s.demanderInscription' % DOMAINE_NOM
    TRANSACTION_INSCRIRE_TIERS = '%s.inscrireTiers' % DOMAINE_NOM
    TRANSACTION_SIGNATURE_INSCRIPTION_TIERS = '%s.signatureInscriptionTiers' % DOMAINE_NOM

    REQUETE_FICHE_PRIVEE = 'millegrilles.domaines.Annuaire.fichePrivee'
    REQUETE_FICHE_PUBLIQUE = 'millegrilles.domaines.Annuaire.fichePublique'

    TEMPLATE_DOCUMENT_INDEX_MILLEGRILLES = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_INDEX_MILLEGRILLES,
        LIBELLE_DOC_LISTE: dict(),  # Dict de ENTREE_INDEX, key=IDMG
    }

    TEMPLATE_DOCUMENT_ENTREE_INDEX = {
        LIBELLE_DOC_DESCRIPTIF: None,
        TRANSACTION_MESSAGE_LIBELLE_IDMG: None,
        LIBELLE_DOC_SECURITE: SECURITE_PROTEGE
    }

    TEMPLATE_DOCUMENT_FICHE_MILLEGRILLE_PRIVEE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_FICHE_PRIVEE,
        TRANSACTION_MESSAGE_LIBELLE_IDMG: None,
        LIBELLE_DOC_LIENS_PRIVES_MQ: list(),
        LIBELLE_DOC_LIENS_RELAIS: list(),
        LIBELLE_DOC_USAGER: dict(),
        LIBELLE_DOC_DESCRIPTIF: None,
        ConstantesPrincipale.LIBELLE_LANGUE_PRINCIPALE: 'fr',
        LIBELLE_DOC_CERTIFICAT_RACINE: None,  # str
        LIBELLE_DOC_CERTIFICAT: None,  # Certificat du maitredescles
        LIBELLE_DOC_CERTIFICATS_INTERMEDIAIRES: None,  # Liste certificats du maitredescles + intermediaires
        LIBELLE_DOC_CERTIFICAT_ADDITIONNELS: None,  # Liste de certificats maitredescles additionnels
    }

    TEMPLATE_DOCUMENT_FICHE_MILLEGRILLE_PUBLIQUE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_FICHE_PUBLIQUE,
        TRANSACTION_MESSAGE_LIBELLE_IDMG: None,
        LIBELLE_DOC_USAGER: dict(),
        LIBELLE_DOC_DESCRIPTIF: None,
        LIBELLE_DOC_CERTIFICAT_RACINE: None,  # str
        ConstantesPrincipale.LIBELLE_LANGUE_PRINCIPALE: 'fr',
    }

    TEMPLATE_DOCUMENT_FICHE_MILLEGRILLE_TIERCE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_FICHE_TIERS,
        TRANSACTION_MESSAGE_LIBELLE_IDMG: None,
        LIBELLE_DOC_LIENS_PUBLICS_HTTPS: list(),
        LIBELLE_DOC_LIENS_PRIVES_MQ: list(),
        LIBELLE_DOC_LIENS_RELAIS: list(),
        LIBELLE_DOC_USAGER: dict(),
        LIBELLE_DOC_DESCRIPTIF: None,
        LIBELLE_DOC_CERTIFICAT_RACINE: None,     # str
        LIBELLE_DOC_CERTIFICATS_INTERMEDIAIRES: None,  # Liste certificats du maitredescles + intermediaires
        LIBELLE_DOC_CERTIFICAT_ADDITIONNELS: None,  # Liste de certificats maitredescles additionnels
        LIBELLE_DOC_SECURITE: SECURITE_PROTEGE,
        LIBELLE_DOC_EXPIRATION_INSCRIPTION: None,  # Date d'expiration du certificat
        LIBELLE_DOC_ABONNEMENTS: dict(),  # Dict d'abonnements pour cette MilleGrille
    }


class ConstantesPlume:

    DOMAINE_NOM = 'millegrilles.domaines.Plume'
    COLLECTION_NOM = DOMAINE_NOM

    COLLECTION_TRANSACTIONS_NOM = COLLECTION_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_NOM
    QUEUE_NOM = DOMAINE_NOM
    QUEUE_ROUTING_CHANGEMENTS = 'noeuds.source.millegrilles_domaines_Plume.documents'

    TRANSACTION_NOUVEAU_DOCUMENT = '%s.nouveauDocument' % DOMAINE_NOM
    TRANSACTION_MODIFIER_DOCUMENT = '%s.modifierDocument' % DOMAINE_NOM
    TRANSACTION_SUPPRIMER_DOCUMENT = '%s.supprimerDocument' % DOMAINE_NOM
    TRANSACTION_PUBLIER_DOCUMENT = '%s.publierDocument' % DOMAINE_NOM
    TRANSACTION_DEPUBLIER_DOCUMENT = '%s.depublierDocument' % DOMAINE_NOM
    TRANSACTION_CREER_ANNONCE = '%s.creerAnnonce' % DOMAINE_NOM
    TRANSACTION_SUPPRIMER_ANNONCE = '%s.supprimerAnnonce' % DOMAINE_NOM
    TRANSACTION_MAJ_ACCUEIL_VITRINE = '%s.majAccueilVitrine' % DOMAINE_NOM
    TRANSACTION_MAJ_BLOGPOST = '%s.majBlogpostVitrine' % DOMAINE_NOM
    TRANSACTION_PUBLIER_BLOGPOST = '%s.publierBlogpostVitrine' % DOMAINE_NOM
    TRANSACTION_RETIRER_BLOGPOST = '%s.retirerBlogpostVitrine' % DOMAINE_NOM
    TRANSACTION_SUPPRIMER_BLOGPOST = '%s.supprimerBlogpostVitrine' % DOMAINE_NOM

    REQUETE_CHARGER_ANNONCES_RECENTES = DOMAINE_NOM + '.chargerAnnoncesRecentes'
    REQUETE_CHARGER_ACCUEIL = DOMAINE_NOM + '.chargerAccueil'
    REQUETE_CHARGER_BLOGPOSTS_RECENTS = DOMAINE_NOM + '.chargerBlogpostsRecents'

    LIBELLE_DOC_PLUME_UUID = 'uuid'
    LIBELLE_DOC_SECURITE = 'securite'
    LIBELLE_DOC_TITRE = 'titre'
    LIBELLE_DOC_CATEGORIES = 'categories'
    LIBELLE_DOC_TEXTE = 'texte'
    LIBELLE_DOC_SUJET = 'sujet'
    LIBELLE_DOC_QUILL_DELTA = 'quilldelta'
    LIBELLE_DOC_LISTE = 'documents'
    LIBELLE_DOC_DATE_PUBLICATION = 'datePublication'
    LIBELLE_DOC_REMPLACE = 'remplace'
    LIBELLE_DOC_DATE_ATTENTE_PUBLICATION = 'dateAttentePublication'
    LIBELLE_DOC_ANNONCES = 'annonces'
    LIBELLE_DOC_IMAGE = 'image'
    LIBELLE_DOC_BLOGPOSTS = 'blogposts'

    LIBELLE_DOC_VITRINE_BIENVENUE = 'messageBienvenue'
    LIBELLE_DOC_VITRINE_TITRE_COLONNES = 'titreCol'
    LIBELLE_DOC_VITRINE_TEXTE_COLONNES = 'texteCol'

    DEFAUT_ATTENTE_PUBLICATION_SECS = 120   # Delai de publication par defaut
    DEFAUT_NOMBRE_ANNONCES_RECENTES = 200   # Nombre max d'annonces dans annonces.recentes

    LIBVAL_CONFIGURATION = 'configuration'
    LIBVAL_PLUME = 'plume'
    LIBVAL_ANNONCE = 'annonce'
    LIBVAL_ANNONCES_RECENTES = 'annonces.recentes'
    LIBVAL_CATALOGUE = 'catalogue'
    LIBVAL_CATEGORIE = 'categorie'
    LIBVAL_VITRINE_ACCUEIL = 'vitrine.accueil'
    LIBVAL_BLOGPOST = 'blogpost'
    LIBVAL_BLOGPOSTS_RECENTS = 'blogposts.recents'

    DOCUMENT_DEFAUT = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION
    }

    DOCUMENT_PLUME = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_PLUME,
        LIBELLE_DOC_PLUME_UUID: None,  # Identificateur unique du document plume
        LIBELLE_DOC_SECURITE: SECURITE_PRIVE,  # Niveau de securite
        LIBELLE_DOC_TITRE: None,               # Titre
        LIBELLE_DOC_CATEGORIES: None,          # Categorie du fichier
        LIBELLE_DOC_QUILL_DELTA: None,         # Contenu, delta Quill
        LIBELLE_DOC_TEXTE: None,               # Texte sans formattage
    }

    DOCUMENT_CATALOGUE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CATALOGUE,
        LIBELLE_DOC_SECURITE: SECURITE_PUBLIC,     # Niveau de securite du catalogue
        LIBELLE_DOC_CATEGORIES: {},                # Dict des categories de Plume. Valeur est 'True' (bidon)
        LIBELLE_DOC_LISTE: {},                     # Dict des documents du catalogue. Cle est uuid,
                                                # valeur est: {titre, uuid, _mg-derniere-modification, categories).
    }

    DOCUMENT_ANNONCE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_ANNONCE,
        LIBELLE_DOC_SUJET: None,                        # Sujet du message (opt)
        LIBELLE_DOC_TEXTE: None,                        # Texte sans formattage
        LIBELLE_DOC_REMPLACE: None,                     # uuid de l'annonce remplacee (opt)
        LIBELLE_DOC_DATE_ATTENTE_PUBLICATION: None,     # Date de prise d'effet de l'annonce
    }

    DOCUMENT_ANNONCES_RECENTES = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_ANNONCES_RECENTES,
        LIBELLE_DOC_ANNONCES: list(),   # Liste triee par date, plus recente annonce en premier
    }

    DOCUMENT_VITRINE_ACCUEIL = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_VITRINE_ACCUEIL,
    }

    DOCUMENT_BLOGPOSTS_RECENTS = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_BLOGPOSTS_RECENTS,
        LIBELLE_DOC_BLOGPOSTS: dict(),
    }

    FILTRE_DOC_ANNONCES_RECENTES = [
        DOCUMENT_INFODOC_DATE_CREATION,
        DOCUMENT_INFODOC_DERNIERE_MODIFICATION,
        LIBELLE_DOC_PLUME_UUID,
        LIBELLE_DOC_DATE_ATTENTE_PUBLICATION,
        LIBELLE_DOC_TEXTE,
        LIBELLE_DOC_SUJET
    ]


class ConstantesGrosFichiers:
    """ Constantes pour le domaine de GrosFichiers """

    DOMAINE_NOM = 'millegrilles.domaines.GrosFichiers'
    COLLECTION_TRANSACTIONS_NOM = DOMAINE_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_TRANSACTIONS_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_TRANSACTIONS_NOM
    QUEUE_NOM = 'millegrilles.domaines.GrosFichiers'
    QUEUE_ROUTING_CHANGEMENTS = 'noeuds.source.millegrilles_domaines_GrosFichiers'

    TRANSACTION_TYPE_METADATA = 'millegrilles.domaines.GrosFichiers.nouvelleVersion.metadata'
    TRANSACTION_TYPE_TRANSFERTCOMPLETE = 'millegrilles.domaines.GrosFichiers.nouvelleVersion.transfertComplete'

    TRANSACTION_CHAMP_ETIQUETTE = 'etiquette'

    LIBVAL_CONFIGURATION = 'configuration'
    LIBVAL_FICHIER = 'fichier'
    LIBVAL_COLLECTION = 'collection'
    LIBVAL_COLLECTION_FIGEE = 'collection.figee'
    LIBVAL_FAVORIS = 'favoris'
    LIBVAL_RAPPORT = 'rapport'
    LIBVAL_RAPPORT_ACTIVITE = 'rapport.activite'

    LIBVAL_VITRINE_FICHIERS = 'vitrine.fichiers'
    LIBVAL_VITRINE_ALBUMS = 'vitrine.albums'

    LIBELLE_PUBLICATION_CACHERFICHIERS = 'cacherfichiers'
    LIBELLE_PUBLICATION_TOP = 'top'
    LIBELLE_PUBLICATION_CAROUSEL = 'carousel'

    DOCUMENT_SECURITE = 'securite'
    DOCUMENT_COMMENTAIRES = 'commentaires'

    DOCUMENT_REPERTOIRE_FICHIERS = 'fichiers'

    DOCUMENT_FICHIER_NOMFICHIER = 'nom'
    DOCUMENT_FICHIER_COMMENTAIRES = 'commentaires'
    DOCUMENT_FICHIER_EXTENSION_ORIGINAL = 'extension'
    DOCUMENT_FICHIER_UUID_DOC = 'uuid'                    # UUID du document de fichier (metadata)
    DOCUMENT_UUID_GENERIQUE = 'documentuuid'            # Represente un UUID de n'import quel type de document
    DOCUMENT_FICHIER_FUUID = 'fuuid'                    # UUID (v1) du fichier
    DOCUMENT_FICHIER_DATEVCOURANTE = 'date_v_courante'  # Date de la version courante
    DOCUMENT_FICHIER_UUIDVCOURANTE = 'fuuid_v_courante'  # FUUID de la version courante
    DOCUMENT_FICHIER_VERSIONS = 'versions'
    DOCUMENT_FICHIER_MIMETYPE = 'mimetype'
    DOCUMENT_FICHIER_TAILLE = 'taille'
    DOCUMENT_FICHIER_SHA256 = 'sha256'
    DOCUMENT_FICHIER_SUPPRIME = 'supprime'
    DOCUMENT_FICHIER_ETIQUETTES = 'etiquettes'
    DOCUMENT_FICHIER_THUMBNAIL = 'thumbnail'
    DOCUMENT_FICHIER_DATA_VIDEO = 'data_video'
    DOCUMENT_FICHIER_FUUID_PREVIEW = 'fuuid_preview'
    DOCUMENT_FICHIER_METADATA = "metadata"
    DOCUMENT_FICHIER_METADATA_VIDEO = "data_video"
    DOCUMENT_FICHIER_MIMETYPE_PREVIEW = 'mimetype_preview'
    DOCUMENT_FICHIER_FUUID_480P = "fuuidVideo480p"
    DOCUMENT_FICHIER_MIMETYPE_480P = "mimetypeVideo480p"
    DOCUMENT_FICHIER_TAILLE_480P = "tailleVideo480p"
    DOCUMENT_FICHIER_SHA256_480P = "sha256Video480p"

    DOCUMENT_FICHIER_FUUID_DECRYPTE = 'fuuid_decrypte'

    DOCUMENT_COLLECTION_FICHIERS = 'fichiers'
    DOCUMENT_COLLECTION_LISTEDOCS = 'documents'
    DOCUMENT_COLLECTION_UUID_SOURCE_FIGEE = 'uuid_source_figee'
    DOCUMENT_COLLECTIONS_FIGEES = 'figees'
    DOCUMENT_COLLECTION_UUID = 'uuid-collection'
    DOCUMENT_TORRENT_COLLECTION_UUID = 'uuid_collection_torrent'
    DOCUMENT_COLLECTION_FIGEE_DATE = 'date'

    DOCUMENT_FAVORIS_LISTE = 'favoris'

    DOCUMENT_VITRINE_TOP = 'top'
    DOCUMENT_VITRINE_COLLECTIONS = 'collections'

    DOCUMENT_VERSION_NOMFICHIER = 'nom'
    DOCUMENT_VERSION_DATE_FICHIER = 'date_fichier'
    DOCUMENT_VERSION_DATE_VERSION = 'date_version'
    DOCUMENT_VERSION_DATE_SUPPRESSION = 'date_suppression'

    DOCUMENT_DEFAULT_MIMETYPE = 'application/binary'

    DOCUMENT_TORRENT_HASHSTRING = 'torrent_hashstring'

    TRANSACTION_NOUVELLEVERSION_METADATA = '%s.nouvelleVersion.metadata' % DOMAINE_NOM
    TRANSACTION_DEMANDE_THUMBNAIL_PROTEGE = '%s.demandeThumbnailProtege' % DOMAINE_NOM
    TRANSACTION_NOUVELLEVERSION_TRANSFERTCOMPLETE = '%s.nouvelleVersion.transfertComplete' % DOMAINE_NOM
    TRANSACTION_NOUVELLEVERSION_CLES_RECUES = '%s.nouvelleVersion.clesRecues' % DOMAINE_NOM
    TRANSACTION_COPIER_FICHIER = '%s.copierFichier' % DOMAINE_NOM
    TRANSACTION_RENOMMER_FICHIER = '%s.renommerFichier' % DOMAINE_NOM
    TRANSACTION_COMMENTER_FICHIER = '%s.commenterFichier' % DOMAINE_NOM
    TRANSACTION_CHANGER_ETIQUETTES_FICHIER = '%s.changerEtiquettesFichier' % DOMAINE_NOM
    TRANSACTION_SUPPRIMER_FICHIER = '%s.supprimerFichier' % DOMAINE_NOM
    TRANSACTION_RECUPERER_FICHIER = '%s.recupererFichier' % DOMAINE_NOM
    TRANSACTION_DECRYPTER_FICHIER = '%s.decrypterFichier' % DOMAINE_NOM
    TRANSACTION_CLESECRETE_FICHIER = '%s.cleSecreteFichier' % DOMAINE_NOM
    TRANSACTION_NOUVEAU_FICHIER_DECRYPTE = '%s.nouveauFichierDecrypte' % DOMAINE_NOM
    TRANSACTION_ASSOCIER_THUMBNAIL = '%s.associerThumbnail' % DOMAINE_NOM
    TRANSACTION_ASSOCIER_VIDEO_TRANSCODE = '%s.associerVideo' % DOMAINE_NOM

    TRANSACTION_NOUVELLE_COLLECTION = '%s.nouvelleCollection' % DOMAINE_NOM
    TRANSACTION_RENOMMER_COLLECTION = '%s.renommerCollection' % DOMAINE_NOM
    TRANSACTION_COMMENTER_COLLECTION = '%s.commenterCollection' % DOMAINE_NOM
    TRANSACTION_SUPPRIMER_COLLECTION = '%s.supprimerCollection' % DOMAINE_NOM
    TRANSACTION_RECUPERER_COLLECTION = '%s.recupererCollection' % DOMAINE_NOM
    TRANSACTION_FIGER_COLLECTION = '%s.figerCollection' % DOMAINE_NOM
    TRANSACTION_CHANGER_ETIQUETTES_COLLECTION = '%s.changerEtiquettesCollection' % DOMAINE_NOM
    TRANSACTION_CREERTORRENT_COLLECTION = '%s.creerTorrentCollection' % DOMAINE_NOM
    TRANSACTION_AJOUTER_FICHIERS_COLLECTION = '%s.ajouterFichiersCollection' % DOMAINE_NOM
    TRANSACTION_RETIRER_FICHIERS_COLLECTION = '%s.retirerFichiersCollection' % DOMAINE_NOM
    TRANSACTION_CHANGER_SECURITE_COLLECTION = '%s.changerSecuriteCollection' % DOMAINE_NOM

    TRANSACTION_AJOUTER_FAVORI = '%s.ajouterFavori' % DOMAINE_NOM
    TRANSACTION_SUPPRIMER_FAVORI = '%s.supprimerFavori' % DOMAINE_NOM

    TRANSACTION_TORRENT_NOUVEAU = '%s.nouveauTorrent' % DOMAINE_NOM
    TRANSACTION_TORRENT_SEEDING = '%s.seedingTorrent' % DOMAINE_NOM

    TRANSACTION_PUBLIER_COLLECTION = '%s.publierCollection' % DOMAINE_NOM

    REQUETE_VITRINE_FICHIERS = '%s.vitrineFichiers' % DOMAINE_NOM
    REQUETE_VITRINE_ALBUMS = '%s.vitrineAlbums' % DOMAINE_NOM
    REQUETE_COLLECTION_FIGEE = '%s.collectionFigee' % DOMAINE_NOM

    COMMANDE_DECRYPTER_FICHIER = 'commande.grosfichiers.decrypterFichier'
    COMMANDE_GENERER_THUMBNAIL_PROTEGE = 'commande.grosfichiers.genererThumbnailProtege'

    # Document par defaut pour la configuration de l'interface GrosFichiers
    DOCUMENT_DEFAUT = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION,
    }

    DOCUMENT_FICHIER = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_FICHIER,
        DOCUMENT_FICHIER_UUID_DOC: None,  # Identificateur unique du fichier (UUID trans initiale)
        # DOCUMENT_SECURITE: Constantes.SECURITE_SECURE,      # Niveau de securite
        DOCUMENT_COMMENTAIRES: None,                        # Commentaires
        DOCUMENT_FICHIER_NOMFICHIER: None,                  # Nom du fichier (libelle affiche a l'usager)
        DOCUMENT_FICHIER_ETIQUETTES: list(),                # Liste de libelles du fichier
        DOCUMENT_FICHIER_SUPPRIME: False,                   # True si le fichier est supprime
    }

    SOUSDOCUMENT_VERSION_FICHIER = {
        DOCUMENT_FICHIER_FUUID: None,
        DOCUMENT_FICHIER_NOMFICHIER: None,
        DOCUMENT_FICHIER_MIMETYPE: DOCUMENT_DEFAULT_MIMETYPE,
        DOCUMENT_VERSION_DATE_FICHIER: None,
        DOCUMENT_VERSION_DATE_VERSION: None,
        DOCUMENT_FICHIER_TAILLE: None,
        DOCUMENT_FICHIER_SHA256: None,
        DOCUMENT_COMMENTAIRES: None,
    }

    DOCUMENT_COLLECTION = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_COLLECTION,
        DOCUMENT_FICHIER_UUID_DOC: None,        # Identificateur unique du fichier (UUID trans initiale)
        DOCUMENT_COLLECTION_LISTEDOCS: dict(),  # Dictionnaire de fichiers, key=uuid, value=DOCUMENT_COLLECTION_FICHIER
        DOCUMENT_FICHIER_ETIQUETTES: list(),    # Etiquettes de la collection
        DOCUMENT_FICHIER_SUPPRIME: False,       # True si la collection est supprimee
        DOCUMENT_COMMENTAIRES: None,
        DOCUMENT_SECURITE: SECURITE_PROTEGE,
    }

    DOCUMENT_COLLECTION_FICHIER = {
        DOCUMENT_FICHIER_UUID_DOC: None,    # uuid du fichier
        DOCUMENT_FICHIER_FUUID: None,       # fuuid de la version du fichier
        DOCUMENT_FICHIER_NOMFICHIER: None,  # Nom du fichier
        DOCUMENT_VERSION_DATE_FICHIER: None,
        DOCUMENT_FICHIER_TAILLE: None,
        DOCUMENT_COMMENTAIRES: None,
    }

    DOCUMENT_FAVORIS = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_FAVORIS,
        DOCUMENT_FAVORIS_LISTE: list(),     # Liste DOCUMENT_FAVORIS_INFO
    }

    DOCUMENT_FAVORIS_INFO = {
        DOCUMENT_INFODOC_LIBELLE: None,      # Type document
        'nom': None,                                    # Nom affiche a l'ecran
        'uuid': None,                                   # Lien vers document, doit etre unique dans la liste de favoris
    }

    DOCUMENT_VITRINE_FICHIERS = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_VITRINE_FICHIERS,
        DOCUMENT_VITRINE_TOP: dict(),
        DOCUMENT_VITRINE_COLLECTIONS: dict(),
    }

    DOCUMENT_VITRINE_ALBUMS = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_VITRINE_ALBUMS,
        DOCUMENT_VITRINE_TOP: dict(),
        DOCUMENT_VITRINE_COLLECTIONS: dict(),
    }

    # Prototype de document liste de recherche
    # Represente une liste maintenue et triee par un champ particulier (date) de resultats
    # pour acces rapide.
    # Peut etre utilise pour garder une liste des N derniers fichiers changes, fichiers
    # avec libelles '2019 et 'photos', etc.
    DOCUMENT_RAPPORT_RECHERCHE = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_RAPPORT,
        'description': None,                    # Description (nom) de la liste de recherche
        DOCUMENT_SECURITE: None,                # Niveau de securite de cette liste
        'filtre_libelles': dict(),              # Libelles utilises pour filtrer la liste des changements
        DOCUMENT_COLLECTION_FICHIERS: list(),   # Dictionnaire de fichiers, valeur=DOCUMENT_COLLECTION_FICHIER
        'tri': [{DOCUMENT_VERSION_DATE_FICHIER: -1}],   # Tri de la liste, utilise pour tronquer
        'compte_max': 100,                      # Nombre maximal d'entree dans la liste
    }


# Constantes pour SenseursPassifs
class SenseursPassifsConstantes:

    DOMAINE_NOM = 'millegrilles.domaines.SenseursPassifs'
    COLLECTION_TRANSACTIONS_NOM = DOMAINE_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_TRANSACTIONS_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_TRANSACTIONS_NOM
    QUEUE_NOM = DOMAINE_NOM
    QUEUE_NOEUDS_NOM = '%s.noeuds' % DOMAINE_NOM
    QUEUE_INTER_NOM = '%s.inter' % DOMAINE_NOM
    QUEUE_ROUTING_CHANGEMENTS = 'noeuds.source.millegrilles_domaines_SenseursPassifs.documents'

    LIBELLE_DOCUMENT_SENSEUR = 'senseur.individuel'
    LIBELLE_DOCUMENT_NOEUD = 'noeud.individuel'
    LIBELLE_DOCUMENT_GROUPE = 'groupe.senseurs'
    LIBELLE_DOCUMENT_SENSEUR_RAPPORT_HORAIRE = 'senseur.rapport.gq'
    LIBELLE_DOCUMENT_SENSEUR_RAPPORT_QUOTIDIEN = 'senseur.rapport.gh'
    LIBELLE_DOCUMENT_SENSEUR_RAPPORT_ANNEE = 'senseur.rapport.annee'
    LIBELLE_DOCUMENT_SENSEUR_RAPPORT_SEMAINE = 'senseur.rapport.semaine'
    LIBVAL_CONFIGURATION = 'configuration'
    LIBVAL_VITRINE_DASHBOARD = 'vitrine.dashboard'

    LIBELLE_NOEUDS = 'noeuds'

    TRANSACTION_NOEUD = 'noeud'
    TRANSACTION_ID_SENSEUR = 'uuid_senseur'
    TRANSACTION_DATE_LECTURE = 'timestamp'
    TRANSACTION_LOCATION = 'location'
    TRANSACTION_DOMAINE_LECTURE = '%s.lecture' % DOMAINE_NOM
    TRANSACTION_DOMAINE_CHANG_ATTRIBUT_SENSEUR = '%s.changementAttributSenseur' % DOMAINE_NOM
    TRANSACTION_DOMAINE_SUPPRESSION_SENSEUR = '%s.suppressionSenseur' % DOMAINE_NOM
    TRANSACTION_DOMAINE_GENERER_RAPPORT = '%s.genererRapport' % DOMAINE_NOM
    SENSEUR_REGLES_NOTIFICATIONS = 'regles_notifications'

    REQUETE_VITRINE_DASHBOARD = '%s.dashboard' % DOMAINE_NOM

    COMMANDE_RAPPORT_HEBDOMADAIRE = '%s.rapportHebdomadaire' % DOMAINE_NOM
    COMMANDE_RAPPORT_ANNUEL = '%s.rapportAnnuel' % DOMAINE_NOM
    COMMANDE_DECLENCHER_RAPPORTS = '%s.declencherRapports' % DOMAINE_NOM

    EVENEMENT_MAJ_HORAIRE = '%s.MAJHoraire' % DOMAINE_NOM
    EVENEMENT_MAJ_QUOTIDIENNE = '%s.MAJQuotidienne' % DOMAINE_NOM

    DOCUMENT_DEFAUT_CONFIGURATION = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION,
        TRANSACTION_MESSAGE_LIBELLE_VERSION: TRANSACTION_MESSAGE_LIBELLE_VERSION_6
    }

    DOCUMENT_DEFAUT_VITRINE_DASHBOARD = {
        DOCUMENT_INFODOC_LIBELLE: LIBVAL_VITRINE_DASHBOARD,
        LIBELLE_NOEUDS: dict(),
    }


# Constantes pour le domaine Backup
class ConstantesBackup:

    DOMAINE_NOM = 'millegrilles.domaines.Backup'
    COLLECTION_TRANSACTIONS_NOM = DOMAINE_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_TRANSACTIONS_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_TRANSACTIONS_NOM
    QUEUE_NOM = DOMAINE_NOM
    QUEUE_NOEUDS_NOM = '%s.noeuds' % DOMAINE_NOM
    QUEUE_INTER_NOM = '%s.inter' % DOMAINE_NOM

    TRANSACTION_CATALOGUE_HORAIRE = '%s.catalogueHoraire' % DOMAINE_NOM
    TRANSACTION_CATALOGUE_HORAIRE_SHA3_512 = '%s.catalogueHoraireSHA3_512' % DOMAINE_NOM
    TRANSACTION_CATALOGUE_HORAIRE_SHA_ENTETE = '%s.catalogueHoraireSHAEntete' % DOMAINE_NOM
    TRANSACTION_CATALOGUE_QUOTIDIEN = '%s.catalogueQuotidienFinaliser' % DOMAINE_NOM
    TRANSACTION_CATALOGUE_MENSUEL = '%s.catalogueMensuelFinaliser' % DOMAINE_NOM
    TRANSACTION_CATALOGUE_ANNUEL = '%s.catalogueAnnuelFinaliser' % DOMAINE_NOM

    TRANSACTION_ARCHIVE_QUOTIDIENNE_INFO = '%s.archiveQuotidienneInfo' % DOMAINE_NOM
    TRANSACTION_ARCHIVE_MENSUELLE_INFO = '%s.archiveMensuelleInfo' % DOMAINE_NOM

    COMMANDE_BACKUP_QUOTIDIEN = 'commande.backup.genererBackupQuotidien'
    COMMANDE_BACKUP_MENSUEL = 'commande.backup.genererBackupMensuel'
    COMMANDE_BACKUP_ANNUEL = 'commande.backup.genererBackupAnnuel'

    COMMANDE_BACKUP_DECLENCHER_HORAIRE_GLOBAL = 'commande.global.declencherBackupHoraire'
    COMMANDE_BACKUP_RESET_GLOBAL = 'commande.global.resetBackup'
    COMMANDE_BACKUP_DECLENCHER_HORAIRE = 'commande._DOMAINE_.declencherBackupHoraire'
    COMMANDE_BACKUP_DECLENCHER_QUOTIDIEN = 'commande._DOMAINE_.declencherBackupQuotidien'
    COMMANDE_BACKUP_DECLENCHER_MENSUEL = 'commande._DOMAINE_.declencherBackupMensuel'
    COMMANDE_BACKUP_DECLENCHER_ANNUEL = 'commande._DOMAINE_.declencherBackupAnnuel'

    COMMANDE_BACKUP_PREPARER_RESTAURATION = 'commande.backup.preparerStagingRestauration'

    REQUETE_BACKUP_DERNIERHORAIRE = '%s.backupDernierHoraire' % DOMAINE_NOM

    LIBVAL_CATALOGUE_HORAIRE = 'catalogue.horaire'
    LIBVAL_CATALOGUE_QUOTIDIEN = 'catalogue.quotidien'
    LIBVAL_CATALOGUE_MENSUEL = 'catalogue.mensuel'
    LIBVAL_CATALOGUE_ANNUEL = 'catalogue.annuel'

    LIBELLE_SECURITE = 'securite'
    LIBELLE_HEURE = 'heure'
    LIBELLE_JOUR = 'jour'
    LIBELLE_MOIS = 'mois'
    LIBELLE_ANNEE = 'annee'
    LIBELLE_DOMAINE = 'domaine'
    LIBELLE_CERTS_RACINE = 'certificats_racine'
    LIBELLE_CERTS_INTERMEDIAIRES = 'certificats_intermediaires'
    LIBELLE_CERTS = 'certificats'
    LIBELLE_CERTS_PEM = 'certificats_pem'
    LIBELLE_CERTS_CHAINE_CATALOGUE = 'certificats_chaine_catalogue'
    LIBELLE_FUUID_GROSFICHIERS = 'fuuid_grosfichiers'
    LIBELLE_FICHIERS_HORAIRE = 'fichiers_horaire'
    LIBELLE_FICHIERS_QUOTIDIEN = 'fichiers_quotidien'
    LIBELLE_FICHIERS_MENSUEL = 'fichiers_mensuel'
    LIBELLE_INFO_HORAIRE = 'info_horaire'
    LIBELLE_TRANSACTIONS_SHA3_512 = 'transactions_sha3_512'
    LIBELLE_TRANSACTIONS_NOMFICHIER = 'transactions_nomfichier'
    LIBELLE_CATALOGUE_SHA3_512 = 'catalogue_sha3_512'
    LIBELLE_CATALOGUE_NOMFICHIER = 'catalogue_nomfichier'
    LIBELLE_CATALOGUES = 'catalogues'
    LIBELLE_FICHIERS_TRANSACTIONS = 'fichiers_transactions'
    LIBELLE_DIRTY_FLAG = 'dirty_flag'
    LIBELLE_BACKUP_PRECEDENT = 'backup_precedent'
    LIBELLE_HACHAGE_ENTETE = 'hachage_entete'

    LIBELLE_ARCHIVE_SHA3_512 = 'archive_sha3_512'
    LIBELLE_ARCHIVE_NOMFICHIER = 'archive_nomfichier'


class ConstantesHebergement:

    DOMAINE_NOM = 'millegrilles.domaines.Hebergement'
    COLLECTION_TRANSACTIONS_NOM = DOMAINE_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_TRANSACTIONS_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_TRANSACTIONS_NOM
    QUEUE_NOM = DOMAINE_NOM


class CommandesSurRelai:
    """
    Commandes qui sont supportes dans l'espace relai pour permettre aux connecteurs d'interagir
    """

    HEADER_COMMANDE = 'connecteur_commande'
    HEADER_TRANSFERT_INTER_COMPLETE = 'transfert_inter_complete'
    HEADER_IDMG_ORIGINE = 'idmg_origine'

    # Une annonce est placee sur l'echange prive avec le routing key definit ci-bas
    BINDING_ANNONCES = 'annonce.#'
    ANNONCE_CONNEXION = 'annonce.connexion'  # Evenement de connexion sur echange prive
    ANNONCE_DECONNEXION = 'annonce.deconnexion'  # Evenement de deconnexion sur echange prive
    ANNONCE_RECHERCHE_CERTIFICAT = 'annonce.requete.certificat'  # Requete d'un certificat par fingerprint
    ANNONCE_PRESENCE = 'annonce.presence'  # Annonce la presence d'une millegrille (regulierement)

    # Le type de commande est place dans le header 'connecteur_commande' du message

    # -- Commandes sans inscription --
    BINDING_COMMANDES = 'commande.#'
    COMMANDE_DEMANDE_INSCRIPTION = 'commande.inscription'  # Transmet une demande d'inscription a une MilleGrille tierce

    # Transmet une demande de confirmation de presence a un connecteur de MilleGrille tierce qui repond par pong
    COMMANDE_PING = 'commande.ping'

    # -- Commandes avec inscription --
    # Une commande est dirigee vers une MilleGrille tierce specifique sur un echange direct (e.g. echange par defaut)
    COMMANDE_CONNEXION = 'commande.connexion'  # Demande de connexion vers une millegrille tierce presente sur relai
    COMMANDE_DECONNEXION = 'commande.deconnexion'  # Deconnexion d'une millegrille tierce presente sur relai
    COMMANDE_PRESENCE = 'commande.presence'  # Utilise pour indiquer presence/activite a un tiers (regulierement)
    COMMANDE_DEMANDE_FICHE = 'commande.demandeFiche'  # Demande la fiche privee d'une MilleGrille tierce

    # Commandes de relai de messages
    # Le contenu doit etre contre-signee par le certificat de connecteur pour etre admises
    COMMANDE_MESSAGE_RELAI = 'commande.message.relai'  # Relai message de la MilleGrille d'origine
