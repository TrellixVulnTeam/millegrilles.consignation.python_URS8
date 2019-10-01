# Module du domaine des taches.

from millegrilles import Constantes
from millegrilles.Domaines import GestionnaireDomaineStandard
from millegrilles.MGProcessus import MGProcessus, MGProcessusTransaction
from millegrilles.dao.EmailDAO import SmtpDAO
from millegrilles.transaction.GenerateurTransaction import GenerateurTransaction

from bson import ObjectId

import datetime
import json
import uuid


class TachesConstantes:

    DOMAINE_NOM = 'millegrilles.domaines.Taches'
    QUEUE_SUFFIXE = DOMAINE_NOM
    COLLECTION_TRANSACTIONS_NOM = QUEUE_SUFFIXE
    COLLECTION_DOCUMENTS_NOM = '%s/documents' % COLLECTION_TRANSACTIONS_NOM
    COLLECTION_PROCESSUS_NOM = '%s/processus' % COLLECTION_TRANSACTIONS_NOM

    TRANSACTION_NOUVELLE_TACHE = 'millegrilles.domaines.Taches.nouvelle'
    TRANSACTION_NOTIFICATION_TACHE = 'millegrilles.domaines.Taches.notification'
    TRANSACTION_ACTION_TACHE = 'millegrilles.domaines.Taches.actionUsager'

    # Niveaux d'une notification de tache
    NIVEAU_SUIVI = 'suivi'                  # Niveau bas avec limite de temps
    NIVEAU_INFORMATION = 'information'      # Plus bas niveau sans limite de temps
    NIVEAU_AVERTISSEMENT = 'avertissement'  # Niveau par defaut / grave
    NIVEAU_ALERTE = 'alerte'                # Plus haut niveau / critique

    LIBVAL_NOTIFICATIONS = 'notifications'
    LIBVAL_TACHES_TABLEAU = 'taches_tableau'

    # Action posee par l'usager sur la notification
    LIBELLE_ID_NOTIFICATION = 'id_notification'  # _id de la notification
    LIBELLE_NIVEAU_NOTIFICATION = 'niveau'  # Niveau d'urgence de la notification
    LIBELLE_COMPTEUR = 'compteur'  # Compte le nombre de fois que la notification est survenue
    LIBELLE_ACTION = 'action'  # Libelle (etiquette) de l'action a faire
    ACTION_VUE = 'vue'         # La notification a ete vue, pas d'autres action requise
    ACTION_RAPPEL = 'rappel'   # L'usager demande un rappel apres une periode de temps. Cachee en attendant.

    LIBELLE_DOMAINE = 'domaine'
    LIBELLE_SOURCE = 'source'
    LIBELLE_COLLATEUR = 'collateur'
    LIBELLE_VALEURS = 'valeurs'
    LIBELLE_DATE = 'date'
    LIBELLE_ACTIVITE = 'activite'
    LIBELLE_ETAT = 'etat_notification'
    LIBELLE_NOTIFICATIONS = 'notifications'
    LIBELLE_DERNIERE_ACTION = 'derniere_action'
    LIBELLE_PERIODE_ATTENTE = 'periode_attente'
    LIBELLE_DATE_ACTION = 'date_action'  # Date de prise d'action
    LIBELLE_DATE_ATTENTE_ACTION = 'date_attente_action'  # Date a partir de laquelle on fait un rappel, de-snooze, etc.
    LIBELLE_TACHES_ACTIVES = 'taches_actives'
    LIBELLE_UUID_TACHE = 'tache_uuid'
    LIBELLE_TITRE = 'titre'
    LIBELLE_ACTIONS_NOTIFICATION = 'actions_notifications'
    LIBELLE_ACTIONS_VISUALISER_DOC = 'inclure_visualiser_document'
    LIBELLE_ACTIONS_DOMAINES = 'actions_domaine'
    LIBELLE_ACTION_DOMAINE = 'action'
    LIBELLE_ACTION_LIBELLE = 'libelle'

    ETAT_NOUVELLE = 'nouvelle'    # Nouvelle tache, notification non generee
    ETAT_ACTIVE = 'active'        # Notification active, pas encore actionee par l'usager
    ETAT_COMPLETEE = 'completee'  # La notification a ete actionnee par l'usager, plus rien a faire.
    ETAT_RAPPEL = 'rappel'        # En attente de rappel aupres de l'usager. Cachee en attendant.

    DOC_NOTIFICATIONS = {
        Constantes.DOCUMENT_INFODOC_LIBELLE: LIBVAL_NOTIFICATIONS,
        LIBELLE_NOTIFICATIONS: list(),
    }

    DOC_SUMMARY_NOTIFICATION = {
        LIBELLE_TITRE: None,
        LIBELLE_DATE: None,
        LIBELLE_UUID_TACHE: None,
        LIBELLE_NIVEAU_NOTIFICATION: None,
        LIBELLE_ACTIONS_NOTIFICATION: True,
    }

    DOC_TACHES_TABLEAU = {
        Constantes.DOCUMENT_INFODOC_LIBELLE: LIBVAL_TACHES_TABLEAU,
        LIBELLE_TACHES_ACTIVES: dict(),  # Docs type DOC_TACHE_TABLEAU_TEMPLATE
    }

    DOC_TACHE_TABLEAU_TEMPLATE = {
        LIBELLE_NIVEAU_NOTIFICATION: NIVEAU_INFORMATION,
        LIBELLE_DATE: None,  # Date plus recente activite
        LIBELLE_TITRE: None,  # Courte description de la tache (64 chars)
        LIBELLE_DOMAINE: None,
        LIBELLE_COLLATEUR: dict(),
        LIBELLE_UUID_TACHE: None,
        LIBELLE_ACTIONS_NOTIFICATION: True,    # Boutons: Vue, Rappel, Suivre
        LIBELLE_ACTIONS_VISUALISER_DOC: True,  # Bouton, redirige vers domaine doc d'origine

        # Ajoute au domaine, envoye en transaction (domaine.action). Notification est vue.
        # Objet DOC_ACTION_DOMAINE
        LIBELLE_ACTIONS_DOMAINES: list(),
    }

    DOC_ACTION_DOMAINE = {
        LIBELLE_ACTION_DOMAINE: None,
        LIBELLE_ACTION_LIBELLE: None,
    }


class GestionnaireTaches(GestionnaireDomaineStandard):

    def __init__(self, contexte):
        super().__init__(contexte)
        self._traitement_message = None

    def demarrer(self):
        super().demarrer()
        self.initialiser_document(TachesConstantes.LIBVAL_NOTIFICATIONS, TachesConstantes.DOC_NOTIFICATIONS)
        self.initialiser_document(TachesConstantes.LIBVAL_TACHES_TABLEAU, TachesConstantes.DOC_TACHES_TABLEAU)


    def get_nom_queue(self):
        return TachesConstantes.QUEUE_SUFFIXE

    def get_nom_collection(self):
        return TachesConstantes.COLLECTION_DOCUMENTS_NOM

    def get_collection_transaction_nom(self):
        return TachesConstantes.COLLECTION_TRANSACTIONS_NOM

    def get_collection_processus_nom(self):
        return TachesConstantes.COLLECTION_PROCESSUS_NOM

    def get_nom_domaine(self):
        return TachesConstantes.DOMAINE_NOM

    def traiter_cedule(self, message):
        # Declencher la verification des actions sur taches
        self.verifier_taches_actionsdues(message)

    def identifier_processus(self, domaine_transaction):
        if domaine_transaction == TachesConstantes.TRANSACTION_ACTION_TACHE:
            processus = "millegrilles_domaines_Taches:ProcessusActionUsager"
        elif domaine_transaction == TachesConstantes.TRANSACTION_NOTIFICATION_TACHE:
            # Notification recue
            processus = "millegrilles_domaines_Taches:ProcessusNotificationRecue"
        else:
            processus = super().identifier_processus(domaine_transaction)

        return processus

    def verifier_taches_actionsdues(self, message):
        collection_taches = self.document_dao.get_collection(TachesConstantes.COLLECTION_DOCUMENTS_NOM)

        filtre = {
            'date_attente_action': {'$lt': datetime.datetime.utcnow()}
        }
        curseur = collection_taches.find(filtre)

        operations_template = {
            '$currentDate': {
                Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: True
            },
            '$unset': {
                TachesConstantes.LIBELLE_DATE_ATTENTE_ACTION: ''
            }
        }

        for taches in curseur:
            etat_tache = taches['etat_tache']

            if etat_tache == TachesConstantes.ETAT_SURVEILLE:
                # La notification est completee (aucun changement depuis qu'elle est en etat de surveillance)
                operations = operations_template.copy()
                operations['$set'] = {
                    TachesConstantes.LIBELLE_ETAT: TachesConstantes.ETAT_COMPLETEE
                }
                self._logger.debug("Completer tache (surveillee): %s" % str(taches))
                collection_taches.update_one({'_id': taches['_id']}, operations)

            elif etat_tache == TachesConstantes.ETAT_RAPPEL:
                # C'est l'heure du rappel. On remet la notification au mode actif.
                operations = operations_template.copy()
                operations['$set'] = {
                    TachesConstantes.LIBELLE_ETAT: TachesConstantes.ETAT_ACTIVE
                }
                self._logger.debug("Rappeler tache: %s" % str(taches))
                collection_taches.update_one({'_id': taches['_id']}, operations)


class ProcessusTaches(MGProcessusTransaction):

    def get_collection_transaction_nom(self):
        return TachesConstantes.COLLECTION_TRANSACTIONS_NOM

    def get_collection_processus_nom(self):
        return TachesConstantes.COLLECTION_PROCESSUS_NOM


class ProcessusNotificationRecue(ProcessusTaches):

    def __init__(self, controleur, evenement):
        super().__init__(controleur, evenement)

    def initiale(self):
        transaction = self.transaction
        domaine = transaction[TachesConstantes.LIBELLE_DOMAINE]
        source = transaction[TachesConstantes.LIBELLE_SOURCE]
        collateur = transaction[TachesConstantes.LIBELLE_COLLATEUR]

        self._logger.debug("Traitement notification tache: %s" % str(transaction))
        collection = self.document_dao.get_collection(TachesConstantes.COLLECTION_DOCUMENTS_NOM)

        filtre = {
            Constantes.DOCUMENT_INFODOC_LIBELLE: Constantes.DOCUMENT_TACHE_NOTIFICATION,
            TachesConstantes.LIBELLE_DOMAINE: domaine,
            TachesConstantes.LIBELLE_COLLATEUR: collateur,
        }

        # Trouver document de tache
        taches_cursor = collection.find(filtre)
        taches = list()
        for tache in taches_cursor:
            taches.append(tache['_id'])

        if len(taches) == 0:
            # Tache n'existe pas, on va en creer une nouvelle
            etape_suivante = ProcessusNotificationRecue.creer_tache.__name__
        else:
            # On a plusieurs taches qui correspondent, on va traiter chaque tache individuellement
            etape_suivante = ProcessusNotificationRecue.traiter_plusieurs_taches.__name__

        self.set_etape_suivante(etape_suivante)

        titre = self.__formatter_titre_notification(transaction)

        return {
            'source': source,
            'domaine': domaine,
            'taches': taches,
            'collateur': collateur,
            'titre': titre,
        }

    def creer_tache(self):
        transaction = self.transaction
        domaine = transaction[TachesConstantes.LIBELLE_DOMAINE]
        collateur = transaction[TachesConstantes.LIBELLE_COLLATEUR]
        niveau = transaction[TachesConstantes.LIBELLE_NIVEAU_NOTIFICATION]

        entree_historique = self.__generer_entree_historique(transaction, self.parametres['titre'])

        push_op = {
            TachesConstantes.LIBELLE_ACTIVITE: entree_historique
        }

        on_insert_op = {
            TachesConstantes.LIBELLE_DOMAINE: domaine,
            Constantes.DOCUMENT_INFODOC_LIBELLE: Constantes.DOCUMENT_TACHE_NOTIFICATION,
            Constantes.DOCUMENT_INFODOC_DATE_CREATION: datetime.datetime.utcnow(),
            TachesConstantes.LIBELLE_NIVEAU_NOTIFICATION: niveau,
            TachesConstantes.LIBELLE_COLLATEUR: collateur,
            TachesConstantes.LIBELLE_UUID_TACHE: str(uuid.uuid4()),
            TachesConstantes.LIBELLE_ETAT: TachesConstantes.ETAT_NOUVELLE,
        }

        ops = {
            '$push': push_op,
            '$setOnInsert': on_insert_op,
            '$currentDate': {Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: True}
        }

        # Inserer par upsert
        collection = self.document_dao.get_collection(TachesConstantes.COLLECTION_DOCUMENTS_NOM)
        update_result = collection.update_one(filter=on_insert_op, update=ops, upsert=True)

        self.set_etape_suivante(ProcessusNotificationRecue.maj_dash_notifications.__name__)  # Termine

        return {
            'taches': [update_result.upserted_id],
            'date': entree_historique[TachesConstantes.LIBELLE_DATE],
        }

    def traiter_plusieurs_taches(self):
        transaction = self.transaction
        date_activite = datetime.datetime.utcfromtimestamp(transaction[TachesConstantes.LIBELLE_DATE])

        for tache_id in self.parametres['taches']:
            ops = {
                '$push': {
                    # Ajouter a la liste d'activite
                    # Trier en ordre decroissant, conserver uniquement les 100 dernieres entrees.
                    TachesConstantes.LIBELLE_ACTIVITE: {
                        '$each': [self.__generer_entree_historique(transaction, self.parametres['titre'])],
                        '$sort': {TachesConstantes.LIBELLE_DATE: -1},
                        '$slice': 100,
                    }
                },
                '$currentDate': {Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: True}
            }

            filtre = {
                '_id': tache_id
            }

            # Inserer par upsert
            collection = self.document_dao.get_collection(TachesConstantes.COLLECTION_DOCUMENTS_NOM)
            collection.update_one(filter=filtre, update=ops, upsert=False)

        self.set_etape_suivante(ProcessusNotificationRecue.maj_dash_notifications.__name__)  # Termine

        return {
            'date': date_activite,
        }

    def maj_dash_notifications(self):
        collection = self.document_dao.get_collection(TachesConstantes.COLLECTION_DOCUMENTS_NOM)
        liste_tacheids = self.parametres['taches']
        taches = collection.find({'_id': {'$in': liste_tacheids}})

        liste_avertir_usager = list()
        for tache in taches:
            # Verifier si la tache est en mode suivi (snooze)
            etat = tache[TachesConstantes.LIBELLE_ETAT]
            uuid_tache = tache[TachesConstantes.LIBELLE_UUID_TACHE]

            dashboard_update = TachesConstantes.DOC_TACHE_TABLEAU_TEMPLATE.copy()
            dashboard_update[TachesConstantes.LIBELLE_DATE] = self.parametres['date']  # Date plus recente activite
            dashboard_update[TachesConstantes.LIBELLE_TITRE] = self.parametres['titre']  # Courte description de la tache (64 chars)
            dashboard_update[TachesConstantes.LIBELLE_DOMAINE] = tache[TachesConstantes.LIBELLE_DOMAINE]
            dashboard_update[TachesConstantes.LIBELLE_COLLATEUR] = tache[TachesConstantes.LIBELLE_COLLATEUR]
            dashboard_update[TachesConstantes.LIBELLE_UUID_TACHE] = uuid_tache
            dashboard_update[TachesConstantes.LIBELLE_ACTIONS_NOTIFICATION] = True    # Boutons: Vue, Rappel, Suivre
            dashboard_update[TachesConstantes.LIBELLE_ACTIONS_VISUALISER_DOC] = True  # Bouton, redirige vers domaine doc d'origine

            # Ajoute au domaine, envoye en transaction (domaine.action). Notification est vue.
            # Objet DOC_ACTION_DOMAINE
            dashboard_update[TachesConstantes.LIBELLE_ACTIONS_DOMAINES] = None

            generer_notification = False
            if etat in [TachesConstantes.ETAT_NOUVELLE, TachesConstantes.ETAT_COMPLETEE]:
                # On va faire un toggle de l'etat de la tache a actif, generer notification.
                generer_notification = True

            if generer_notification:
                liste_avertir_usager.append(dashboard_update)

                # Ajouter notification dans mongo
                doc_notification = TachesConstantes.DOC_SUMMARY_NOTIFICATION.copy()
                doc_notification[TachesConstantes.LIBELLE_TITRE] = self.parametres['titre']
                doc_notification[TachesConstantes.LIBELLE_DATE] = self.parametres['date']
                doc_notification[TachesConstantes.LIBELLE_UUID_TACHE] = uuid_tache
                doc_notification[TachesConstantes.LIBELLE_NIVEAU_NOTIFICATION] = tache[TachesConstantes.LIBELLE_NIVEAU_NOTIFICATION]
                doc_notification[TachesConstantes.LIBELLE_ACTIONS_NOTIFICATION] = True

                ops = {
                    '$push': {
                        TachesConstantes.LIBELLE_NOTIFICATIONS: doc_notification
                    },
                    '$currentDate': {Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: True}
                }
                filtre = {
                    Constantes.DOCUMENT_INFODOC_LIBELLE: TachesConstantes.LIBVAL_NOTIFICATIONS
                }
                collection.update_one(filtre, ops)

            # Mettre a jour dashboard
            ops_tableau = {
                '$set': {
                    '%s.%s' % (TachesConstantes.LIBELLE_TACHES_ACTIVES, uuid_tache): dashboard_update,
                },
                '$currentDate': {Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: True}
            }
            filtre_tableau = {
                Constantes.DOCUMENT_INFODOC_LIBELLE: TachesConstantes.LIBVAL_TACHES_TABLEAU
            }
            collection.update_one(filtre_tableau, ops_tableau)

        if len(liste_avertir_usager) > 0:
            self.set_etape_suivante(ProcessusNotificationRecue.avertir_usager.__name__)  # Termine
            return {
                'liste_avertir_usager': liste_avertir_usager
            }
        else:
            self.set_etape_suivante()  # Termine

    def avertir_usager(self):
        configuration = self._controleur.configuration

        sujet = "Notification %s" % configuration.nom_millegrille

        for notification in self.parametres['liste_avertir_usager']:
            contenu = "Nouvelle notification pour la MilleGrille %s\n\n%s" % (configuration.nom_millegrille, str(notification))
            self._logger.info("Transmission notifcation par courriel: %s" % sujet)
            self._logger.debug(contenu)

            # smtp_dao = SmtpDAO(self._controleur.configuration)
            # smtp_dao.envoyer_notification(sujet, contenu)

        self.set_etape_suivante()  # Termine le processus

    def __formatter_titre_notification(self, transaction):
        configuration = self._controleur.configuration
        domaine = transaction[TachesConstantes.LIBELLE_DOMAINE]
        valeurs = transaction[TachesConstantes.LIBELLE_VALEURS]

        niveau = transaction[TachesConstantes.LIBELLE_NIVEAU_NOTIFICATION]
        short_domaine = domaine.split('.')[-1]
        description = ', '.join(['%s=%s' % (key, value) for key, value in valeurs.items()])

        titre = '%s %s %s: %s' % (configuration.nom_millegrille, niveau, short_domaine, description)

        if len(titre) > 64:
            titre = titre[0:64]

        return titre

    def __generer_entree_historique(self, transaction, titre):
        source = transaction[TachesConstantes.LIBELLE_SOURCE]
        valeurs = transaction[TachesConstantes.LIBELLE_VALEURS]
        date_activite = datetime.datetime.utcfromtimestamp(transaction[TachesConstantes.LIBELLE_DATE])
        niveau = transaction[TachesConstantes.LIBELLE_NIVEAU_NOTIFICATION]

        entree_historique = {
            TachesConstantes.LIBELLE_SOURCE: source,
            TachesConstantes.LIBELLE_VALEURS: valeurs,
            TachesConstantes.LIBELLE_DATE: date_activite,
            TachesConstantes.LIBELLE_NIVEAU_NOTIFICATION: niveau,
            TachesConstantes.LIBELLE_TITRE: titre,
        }

        return entree_historique


class ProcessusActionUsager(ProcessusTaches):

    def __init__(self, controleur, evenement):
        super().__init__(controleur, evenement)

    def initiale(self):
        parametres = self.parametres
        transaction = self.charger_transaction(TachesConstantes.COLLECTION_TRANSACTIONS_NOM)
        collection_notifications = self.document_dao.get_collection(TachesConstantes.COLLECTION_DOCUMENTS_NOM)

        self._logger.debug("Parametres de l'action usager: %s" % str(parametres))
        self._logger.debug("Message de l'action usager: %s" % str(transaction))
        id_notification = transaction[TachesConstantes.LIBELLE_ID_NOTIFICATION]
        action_usager = transaction[TachesConstantes.LIBELLE_ACTION]

        filtre_notification = {'_id': ObjectId(id_notification)}
        operations_set = {
            TachesConstantes.LIBELLE_DERNIERE_ACTION: action_usager
        }
        operations_unset = dict()
        operations = {
            '$set': operations_set,
            '$currentDate': {
                TachesConstantes.LIBELLE_DATE_ACTION: True,
                Constantes.DOCUMENT_INFODOC_DERNIERE_MODIFICATION: True
            }
        }

        if action_usager == TachesConstantes.ACTION_VUE:
            # Marquer la notification comme vue. A moins qu'une autre notification soit recue,
            # l'usager a fait ce qu'il avait a faire au sujet de cette notification.
            operations_set[TachesConstantes.LIBELLE_ETAT] = TachesConstantes.ETAT_COMPLETEE
            operations_unset[TachesConstantes.LIBELLE_DATE_ATTENTE_ACTION] = ''

        elif action_usager == TachesConstantes.ACTION_RAPPEL:
            # Calculer la date de rappel
            date_prochaine_action = self._calculer_periode_attente(transaction)
            operations_set[TachesConstantes.LIBELLE_DATE_ATTENTE_ACTION] = date_prochaine_action
            operations_set[TachesConstantes.LIBELLE_ETAT] = TachesConstantes.ETAT_RAPPEL

        elif action_usager == TachesConstantes.ACTION_SURVEILLE:
            # Calculer la date d'arret de surveillance
            date_prochaine_action = self._calculer_periode_attente(transaction)
            operations_set[TachesConstantes.LIBELLE_DATE_ATTENTE_ACTION] = date_prochaine_action
            operations_set[TachesConstantes.LIBELLE_ETAT] = TachesConstantes.ETAT_SURVEILLE

        if len(operations_unset) > 0:
            operations['$unset'] = operations_unset
        document_notification = collection_notifications.find_one_and_update(filtre_notification, operations)

        if document_notification is None:
            raise ValueError("Document notification _id:%s n'a pas ete trouve" % id_notification)

        # Selon la valeur precedente ou association a un workflow, il pourrait falloir prendre
        # differentss actions.
        self.set_etape_suivante()  # Termine

        return {"notification_precedente": document_notification}

    def _calculer_periode_attente(self, transaction):
        """ Calcule le delai d'attente pour une action. Utilise l'estampille de la transaction pour calculer
            le delai. """

        estampille = transaction[Constantes.TRANSACTION_MESSAGE_LIBELLE_INFO_TRANSACTION][Constantes.TRANSACTION_MESSAGE_LIBELLE_ESTAMPILLE]

        attente_secondes = transaction.get(TachesConstantes.LIBELLE_DATE_ATTENTE_ACTION)
        if attente_secondes is None:
            # Defaut 24h
            attente_secondes = 24 * 60 * 60

        prochaine_action = estampille + datetime.timedelta(seconds=attente_secondes)

        return prochaine_action


class FormatteurEvenementNotification:

    TEMPLATE_NOTIFICATION = {
        "domaine": None,

        "niveau": None,

        Constantes.EVENEMENT_MESSAGE_EVENEMENT: Constantes.EVENEMENT_NOTIFICATION,
        "source": {
            "collection": None,
        },

        # Le collateur de tache - permet d'identifier la tache de maniere unique dans le domaine
        "collateur": {
        },

        "valeurs": {
        },
    }

    def __init__(self, domaine: str, nom_collection: str, generateur_transactions: GenerateurTransaction):
        self._domaine = domaine
        self._collection = nom_collection
        self._generateur_transactions = generateur_transactions

        self._template = FormatteurEvenementNotification.TEMPLATE_NOTIFICATION.copy()
        self._template['domaine'] = domaine
        self._template['source']['collection'] = nom_collection

    def __formatter_notification(
            self, source: dict, collateur: dict, valeurs: dict, niveau: str):
        notification = self._template.copy()
        notification['niveau'] = niveau
        notification['source'].update(source)
        notification['collateur'] = collateur
        notification['valeurs'] = valeurs
        notification['date'] = int(datetime.datetime.utcnow().timestamp())

        return notification

    def emettre_notification_tache(
            self, source: dict, collateur: dict, valeurs: dict, niveau: str = TachesConstantes.NIVEAU_INFORMATION):
        """
        Emet une nouvelle notification pour une tache.

        :param source: Business key de la source
        :param collateur: Collateur de tache
        :param valeurs: Regles en cause avec leur valeurs
        :param niveau: Niveau de notification
        """

        notification = self.__formatter_notification(source, collateur, valeurs, niveau)
        routing = TachesConstantes.TRANSACTION_NOTIFICATION_TACHE
        self._generateur_transactions.soumettre_transaction(notification, routing)