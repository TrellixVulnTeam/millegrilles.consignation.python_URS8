import logging
import datetime
import pytz

from millegrilles import Constantes
from millegrilles.Constantes import ConstantesSecurite, ConstantesForum
from millegrilles.Domaines import GestionnaireDomaineStandard, TraitementMessageDomaineRequete, \
    TraitementMessageDomaineCommande, TraitementCommandesProtegees
from millegrilles.MGProcessus import MGProcessusTransaction


class TraitementRequetesPubliques(TraitementMessageDomaineRequete):

    def traiter_requete(self, ch, method, properties, body, message_dict):
        routing_key = method.routing_key
        domaine_action = routing_key.split('.').pop()

        if domaine_action == ConstantesForum.REQUETE_FORUMS:
            reponse = self.gestionnaire.get_forums_publics(message_dict)
            reponse = {'resultats': reponse}
        elif domaine_action == ConstantesForum.REQUETE_FORUM_POSTS:
            reponse = self.gestionnaire.get_forums_posts_publics(message_dict)
            reponse = {'resultats': reponse}
        elif domaine_action == ConstantesForum.REQUETE_POSTS:
            reponse = self.gestionnaire.get_posts_publics(message_dict)
            reponse = {'resultats': reponse}
        else:
            reponse = {'err': 'Commande invalide', 'routing_key': routing_key, 'domaine_action': domaine_action}
            self.transmettre_reponse(message_dict, reponse, properties.reply_to, properties.correlation_id)
            raise Exception("Requete publique non supportee " + routing_key)

        if reponse:
            self.transmettre_reponse(
                message_dict, reponse, properties.reply_to, properties.correlation_id, ajouter_certificats=True)


class TraitementRequetesPrivees(TraitementMessageDomaineRequete):

    def traiter_requete(self, ch, method, properties, body, message_dict):
        routing_key = method.routing_key
        domaine_action = routing_key.split('.').pop()

        if domaine_action == ConstantesForum.REQUETE_FORUMS:
            message_dict['securite'] = Constantes.SECURITE_PRIVE
            reponse = self.gestionnaire.get_forums(message_dict)
            reponse = {'resultats': reponse}
        elif domaine_action == ConstantesForum.REQUETE_FORUM_POSTS:
            message_dict['securite'] = Constantes.SECURITE_PRIVE
            reponse = self.gestionnaire.get_forums_posts(message_dict)
            reponse = {'resultats': reponse}
        elif domaine_action == ConstantesForum.REQUETE_POSTS:
            message_dict['securite'] = Constantes.SECURITE_PRIVE
            reponse = self.gestionnaire.get_posts(message_dict)
            reponse = {'resultats': reponse}
        else:
            reponse = {'err': 'Commande invalide', 'routing_key': routing_key, 'domaine_action': domaine_action}
            self.transmettre_reponse(message_dict, reponse, properties.reply_to, properties.correlation_id)
            raise Exception("Requete publique non supportee " + routing_key)

        if reponse:
            self.transmettre_reponse(
                message_dict, reponse, properties.reply_to, properties.correlation_id, ajouter_certificats=True)


class TraitementRequetesProtegees(TraitementRequetesPrivees):

    def traiter_requete(self, ch, method, properties, body, message_dict):
        routing_key = method.routing_key
        domaine_action = routing_key.split('.').pop()

        if domaine_action == ConstantesForum.REQUETE_FORUMS:
            message_dict['securite'] = Constantes.SECURITE_PROTEGE
            reponse = self.gestionnaire.get_forums(message_dict)
            reponse = {'resultats': reponse}
        else:
            reponse = super().traiter_requete(ch, method, properties, body, message_dict)

        if reponse:
            self.transmettre_reponse(
                message_dict, reponse, properties.reply_to, properties.correlation_id, ajouter_certificats=True)


class TraitementCommandesPrivees(TraitementMessageDomaineCommande):

    def traiter_commande(self, enveloppe_certificat, ch, method, properties, body, message_dict):
        routing_key = method.routing_key
        action = routing_key.split('.')[-1]

        resultat: dict
        if action == ConstantesForum.COMMANDE_VOTER:
            resultat = self.gestionnaire.ajouter_vote(message_dict)
        else:
            resultat = super().traiter_commande(enveloppe_certificat, ch, method, properties, body, message_dict)

        return resultat


class TraitementCommandesForumProtegees(TraitementCommandesProtegees):

    def traiter_commande(self, enveloppe_certificat, ch, method, properties, body, message_dict):
        routing_key = method.routing_key
        action = routing_key.split('.')[-1]

        resultat: dict
        if action == ConstantesForum.COMMANDE_VOTER:
            resultat = self.gestionnaire.ajouter_vote(message_dict)
        else:
            resultat = super().traiter_commande(enveloppe_certificat, ch, method, properties, body, message_dict)

        return resultat


class GestionnaireForum(GestionnaireDomaineStandard):

    def __init__(self, contexte):
        super().__init__(contexte)
        self.__logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

        self.__handler_requetes = {
            Constantes.SECURITE_PUBLIC: TraitementRequetesPubliques(self),
            Constantes.SECURITE_PRIVE: TraitementRequetesPrivees(self),
            Constantes.SECURITE_PROTEGE: TraitementRequetesProtegees(self)
        }

        self.__handler_commandes = {
            Constantes.SECURITE_PRIVE: TraitementCommandesPrivees(self),
            Constantes.SECURITE_PROTEGE: TraitementCommandesProtegees(self)
        }

    def configurer(self):
        super().configurer()
        self.creer_index()  # Creer index dans MongoDB

    def demarrer(self):
        super().demarrer()

    def creer_index(self):
        pass
        collection_forums = self.document_dao.get_collection(ConstantesForum.COLLECTION_FORUMS_NOM)
        collection_forums.create_index([(ConstantesForum.CHAMP_REF_ID, 1)], name='ref_id', unique=True)

        # collection_posts = self.document_dao.get_collection(ConstantesPublication.COLLECTION_POSTS_NOM)
        #
        # # Index _mg-libelle
        # collection_sites.create_index([(ConstantesPublication.CHAMP_SITE_ID, 1)], name='site_id')
        # collection_posts.create_index([(Constantes.DOCUMENT_INFODOC_LIBELLE, 1)], name='mglibelle')
        #
        # collection_sites.create_index([(ConstantesPublication.CHAMP_NOEUDS_URLS, 1)], name='noeuds_urls')

    def traiter_cedule(self, evenement):
        super().traiter_cedule(evenement)

        # minutes = evenement['timestamp']['UTC'][4]
        #
        # if minutes % 15 == 3:
        #     self.resoumettre_conversions_manquantes()

    def identifier_processus(self, domaine_transaction):
        domaine_action = domaine_transaction.split('.').pop()
        if domaine_action == ConstantesForum.TRANSACTION_CREER_FORUM:
            processus = "millegrilles_domaines_Forum:ProcessusTransactionCreationForum"
        elif domaine_action == ConstantesForum.TRANSACTION_MODIFIER_FORUM:
            processus = "millegrilles_domaines_Forum:ProcessusTransactionModifierForum"
        elif domaine_action == ConstantesForum.TRANSACTION_AJOUTER_POST:
            processus = "millegrilles_domaines_Forum:ProcessusTransactionAjouterPost"
        elif domaine_action == ConstantesForum.TRANSACTION_MODIFIER_POST:
            processus = "millegrilles_domaines_Forum:ProcessusTransactionModifierPost"
        elif domaine_action == ConstantesForum.TRANSACTION_AJOUTER_COMMENTAIRE:
            processus = "millegrilles_domaines_Forum:ProcessusTransactionMAjouterCommentaire"
        elif domaine_action == ConstantesForum.TRANSACTION_MODIFIER_COMMENTAIRE:
            processus = "millegrilles_domaines_Forum:ProcessusTransactionModifierCommentaire"
        else:
            # Type de transaction inconnue, on lance une exception
            processus = super().identifier_processus(domaine_transaction)

        return processus

    def get_handler_requetes(self) -> dict:
        return self.__handler_requetes

    def get_handler_commandes(self) -> dict:
        return self.__handler_commandes

    def get_nom_collection(self):
        return self.get_nom_collection_forums()

    def get_nom_collection_forums(self):
        return ConstantesForum.COLLECTION_FORUMS_NOM

    def get_nom_collection_posts(self):
        return ConstantesForum.COLLECTION_POSTS_NOM

    def get_nom_collection_forum_posts(self):
        return ConstantesForum.COLLECTION_FORUMS_POSTS_NOM

    def get_nom_collection_forum_commentaires(self):
        return ConstantesForum.COLLECTION_COMMENTAIRES_NOM

    def get_nom_collection_forum_votes(self):
        return ConstantesForum.COLLECTION_VOTES_NOM

    def get_nom_queue(self):
        return ConstantesForum.QUEUE_NOM

    def get_collection_transaction_nom(self):
        return ConstantesForum.COLLECTION_TRANSACTIONS_NOM

    def get_collection_processus_nom(self):
        return ConstantesForum.COLLECTION_PROCESSUS_NOM

    def get_nom_domaine(self):
        return ConstantesForum.DOMAINE_NOM

    def get_forums(self, params: dict):
        niveaux_securite = ConstantesSecurite.cascade_public(params['securite']) or Constantes.SECURITE_PUBLIC
        filtre = {
            Constantes.DOCUMENT_INFODOC_SECURITE: {'$in': niveaux_securite}
        }
        collection_site = self.document_dao.get_collection(ConstantesForum.COLLECTION_FORUMS_NOM)
        curseur = collection_site.find(filtre)

        forums = list()
        for forum in curseur:
            for key in list(forum.keys()):
                if key.startswith('_'):
                    del forum[key]
            forums.append(forum)

        return forums

    def creer_forum(self, params: dict):
        uuid_transaction = params['en-tete']['uuid_transaction']
        date_courante = pytz.utc.localize(datetime.datetime.utcnow())
        forum = {
            Constantes.DOCUMENT_INFODOC_LIBELLE: ConstantesForum.LIBVAL_FORUM,
            Constantes.DOCUMENT_INFODOC_DATE_CREATION: date_courante,
            Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: date_courante,

            'ref_id': uuid_transaction,
            'securite': Constantes.SECURITE_PROTEGE,
        }
        collection_site = self.document_dao.get_collection(ConstantesForum.COLLECTION_FORUMS_NOM)

        resultat = collection_site.insert_one(forum)
        if resultat.acknowledged is not True:
            return {'ok': False, 'err': 'Echec ajout document de forum'}

        return {'ok': True}

    def maj_forum(self, params: dict):
        ref_id = params[ConstantesForum.CHAMP_REF_ID]

        champs_supportes = [
            ConstantesForum.CHAMP_NOM_FORUM,
            ConstantesForum.CHAMP_LANGUE_FORUM,
            ConstantesForum.CHAMP_DESCRIPTION_FORUM,
        ]

        # Transferer les valeurs a modifier en fonction de la liste de champs supportes
        set_ops = dict()
        for key in params:
            if key in champs_supportes:
                set_ops[key] = params[key]

        ops = {
            '$set': set_ops,
            '$currentDate': {Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: True}
        }

        filtre = {
            ConstantesForum.CHAMP_REF_ID: ref_id,
        }

        collection_site = self.document_dao.get_collection(ConstantesForum.COLLECTION_FORUMS_NOM)
        resultats = collection_site.update_one(filtre, ops)

        if resultats.modified_count != 1:
            return {'ok': False, 'err': "Echec mise a jour, document non trouve"}

        return {'ok': True}


class ProcessusTransactionCreationForum(MGProcessusTransaction):

    def __init__(self, controleur, evenement):
        super().__init__(controleur, evenement)
        self.__logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

    def initiale(self):
        """
        :return:
        """
        transaction = self.transaction
        reponse = self.controleur.gestionnaire.creer_forum(transaction)

        self.set_etape_suivante()  # Termine

        return reponse


class ProcessusTransactionModifierForum(MGProcessusTransaction):

    def __init__(self, controleur, evenement):
        super().__init__(controleur, evenement)
        self.__logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

    def initiale(self):
        """
        :return:
        """
        transaction = self.transaction
        reponse = self.controleur.gestionnaire.maj_forum(transaction)

        self.set_etape_suivante()  # Termine

        return reponse