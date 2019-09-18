# Domaine de gestion et d'administration de MilleGrilles
from millegrilles import Constantes
from millegrilles.Domaines import GestionnaireDomaineStandard, TraitementRequetesNoeuds
from millegrilles.dao.MessageDAO import TraitementMessageDomaine
from millegrilles.MGProcessus import  MGProcessusTransaction

import logging
import datetime


class ConstantesParametres:

    DOMAINE_NOM = 'millegrilles.domaines.Parametres'
    COLLECTION_NOM = DOMAINE_NOM

    COLLECTION_TRANSACTIONS_NOM = COLLECTION_NOM
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_NOM
    QUEUE_NOM = DOMAINE_NOM

    TRANSACTION_MODIFIER_EMAIL_SMTP = '%s.modifierEmailSmtp' % DOMAINE_NOM
    TRANSACTION_CLES_RECUES = '%s.clesRecues' % DOMAINE_NOM

    TRANSACTION_CHAMP_MGLIBELLE = 'mg-libelle'
    TRANSACTION_CHAMP_UUID = 'uuid'

    DOCUMENT_CHAMP_COURRIEL_ORIGINE = 'origine'
    DOCUMENT_CHAMP_COURRIEL_DESTINATIONS = 'destinations'
    DOCUMENT_CHAMP_HOST = 'host'
    DOCUMENT_CHAMP_PORT = 'port'
    DOCUMENT_CHAMP_USER = 'user'
    DOCUMENT_CHAMP_PASSWORD = 'password'

    DOCUMENT_CHAMP_ACTIF = 'actif'

    LIBVAL_CONFIGURATION = 'configuration'
    LIBVAL_EMAIL_SMTP = 'email.stmp'
    LIBVAL_VERSIONS_IMAGES_DOCKER = 'versions.images.docker'
    LIBVAL_CERTS_WEB = 'certs.web'
    LIBVAL_CERTS_SSL = 'certs.ssl'

    DOCUMENT_DEFAUT = {
        Constantes.DOCUMENT_INFODOC_LIBELLE: LIBVAL_CONFIGURATION
    }

    DOCUMENT_EMAIL_SMTP = {
        Constantes.DOCUMENT_INFODOC_LIBELLE: LIBVAL_EMAIL_SMTP,
        DOCUMENT_CHAMP_ACTIF: False,
        DOCUMENT_CHAMP_COURRIEL_ORIGINE: None,
        DOCUMENT_CHAMP_COURRIEL_DESTINATIONS: None,
        DOCUMENT_CHAMP_HOST: None,
        DOCUMENT_CHAMP_PORT: None,
        DOCUMENT_CHAMP_USER: None,
        Constantes.DOCUMENT_SECTION_CRYPTE: None,  # DOCUMENT_CHAMP_PASSWORD
    }


class GestionnaireParametres(GestionnaireDomaineStandard):

    def __init__(self, contexte):
        super().__init__(contexte)

        # Queue message handlers
        self.__handler_transaction = TraitementTransactionPersistee(self)
        self.__handler_cedule = TraitementMessageCedule(self)
        self.__handler_requetes_noeuds = TraitementRequetesNoeuds(self)

        self._logger = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))

    def configurer(self):
        super().configurer()
        self.initialiser_document(ConstantesParametres.LIBVAL_CONFIGURATION, ConstantesParametres.DOCUMENT_DEFAUT)
        self.initialiser_document(ConstantesParametres.LIBVAL_EMAIL_SMTP, ConstantesParametres.DOCUMENT_EMAIL_SMTP)

    def modifier_document_email_smtp(self, transaction):
        document_email_smtp = {
            Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: datetime.datetime.utcnow()
        }
        self.map_transaction_vers_document(transaction, document_email_smtp)  # Copier champs transaction vers doc

        operations = {
            '$set': document_email_smtp,
        }

        filtre = {
            Constantes.DOCUMENT_INFODOC_LIBELLE: ConstantesParametres.LIBVAL_EMAIL_SMTP
        }

        collection_domaine = self.document_dao.get_collection(self.get_nom_collection())
        resultat = collection_domaine.update_one(filtre, operations)

        return document_email_smtp

    def get_nom_queue(self):
        return ConstantesParametres.QUEUE_NOM

    def get_nom_collection(self):
        return ConstantesParametres.COLLECTION_DOCUMENTS_NOM

    def get_collection_transaction_nom(self):
        return ConstantesParametres.COLLECTION_TRANSACTIONS_NOM

    def get_collection_processus_nom(self):
        return ConstantesParametres.COLLECTION_PROCESSUS_NOM

    def get_nom_domaine(self):
        return ConstantesParametres.DOMAINE_NOM

    def get_handler_transaction(self):
        return self.__handler_transaction

    def get_handler_cedule(self):
        return self.__handler_cedule

    def get_handler_requetes_noeuds(self):
        return self.__handler_requetes_noeuds

    def identifier_processus(self, domaine_transaction):
        if domaine_transaction == ConstantesParametres.TRANSACTION_MODIFIER_EMAIL_SMTP:
            processus = "millegrilles_domaines_Parametres:ProcessusTransactionModifierEmailSmtp"
        elif domaine_transaction == ConstantesParametres.TRANSACTION_CLES_RECUES:
            processus = "millegrilles_domaines_Parametres:ProcessusTransactionClesRecues"
        else:
            processus = super().identifier_processus(domaine_transaction)

        return processus

    def traiter_cedule(self, evenement):
        pass


class TraitementMessageCedule(TraitementMessageDomaine):

    def __init__(self, gestionnaire):
        super().__init__(gestionnaire)

    def traiter_message(self, ch, method, properties, body):
        message_dict = self.json_helper.bin_utf8_json_vers_dict(body)
        evenement = message_dict.get(Constantes.EVENEMENT_MESSAGE_EVENEMENT)
        routing_key = method.routing_key


class TraitementTransactionPersistee(TraitementMessageDomaine):

    def __init__(self, gestionnaire):
        super().__init__(gestionnaire)

    def traiter_message(self, ch, method, properties, body):
        message_dict = self.json_helper.bin_utf8_json_vers_dict(body)
        evenement = message_dict.get(Constantes.EVENEMENT_MESSAGE_EVENEMENT)

        # Verifier quel processus demarrer.
        routing_key = method.routing_key
        routing_key_sansprefixe = routing_key.replace(
            'destinataire.domaine.',
            ''
        )

        processus = self.gestionnaire.identifier_processus(routing_key_sansprefixe)
        self._gestionnaire.demarrer_processus(processus, message_dict)


# ******************* Processus *******************
class ProcessusParametres(MGProcessusTransaction):

    def get_collection_transaction_nom(self):
        return ConstantesParametres.COLLECTION_TRANSACTIONS_NOM

    def get_collection_processus_nom(self):
        return ConstantesParametres.COLLECTION_PROCESSUS_NOM


class ProcessusTransactionModifierEmailSmtp(ProcessusParametres):
    """
    Processus de modification de document Plume
    """

    def initiale(self):
        """
        Certains messages contiennent de l'information cryptee. On doit s'assurer d'avoir recu la cle avant
        de poursuivre la mise a jour.
        :return:
        """
        transaction = self.charger_transaction()
        document_email_smtp = self._controleur.gestionnaire.modifier_document_email_smtp(transaction)

        tokens_attente = None
        if document_email_smtp.get(Constantes.DOCUMENT_SECTION_CRYPTE) is not None:
            # On doit attendre la confirmation de reception des cles
            uuid = transaction[Constantes.TRANSACTION_MESSAGE_LIBELLE_EN_TETE][
                Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID]
            tokens_attente = self._get_tokens_attente(uuid)

        self.set_etape_suivante(
            etape_suivante=ProcessusTransactionModifierEmailSmtp.sauvegarder_changements.__name__,
            token_attente=tokens_attente
        )

    def sauvegarder_changements(self):
        """ Mettre a jour le document """
        transaction = self.charger_transaction()
        document_email_smtp = self._controleur.gestionnaire.modifier_document_email_smtp(transaction)

        self.set_etape_suivante()  # Termine
        return {
            Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: document_email_smtp[Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION],
        }

    def _get_tokens_attente(self, uuid):
        tokens = [
            '%s:%s:%s' % (ConstantesParametres.TRANSACTION_CLES_RECUES, ConstantesParametres.LIBVAL_EMAIL_SMTP, uuid)
        ]

        return tokens


class ProcessusTransactionClesRecues(ProcessusParametres):

    def __init__(self, controleur, evenement):
        super().__init__(controleur, evenement)

    def traitement_regenerer(self, id_transaction, parametres_processus):
        pass  # Rien a faire pour cette transaction

    def initiale(self):
        """
        Emet un evenement pour indiquer que les cles sont recues par le MaitreDesCles.
        """
        transaction = self.charger_transaction()
        identificateurs_documents = transaction['identificateurs_document']
        mg_libelle = identificateurs_documents[Constantes.DOCUMENT_INFODOC_LIBELLE]
        uuid = transaction[Constantes.TRANSACTION_MESSAGE_LIBELLE_UUID]

        token_resumer = '%s:%s:%s' % (ConstantesParametres.TRANSACTION_CLES_RECUES, mg_libelle, uuid)
        self.resumer_processus([token_resumer])

        self.set_etape_suivante()  # Termine
        return {ConstantesParametres.TRANSACTION_CHAMP_MGLIBELLE: mg_libelle}