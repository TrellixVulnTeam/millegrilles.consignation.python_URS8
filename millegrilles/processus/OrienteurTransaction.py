#!/usr/bin/python3

'''
    L'orienteur de transaction est le processus qui prend le relai de toutes les transactions
    apres la persistance initiale.
'''

from millegrilles.dao.MessageDAO import BaseCallback, JSONHelper

class OrienteurTransaction(BaseCallback):

    def __init__(self):

        self.dict_libelle = {}
        self._message_dao = None
        self._document_dao = None
        self._json_helper = JSONHelper()

    def initialiser(self):
        self._message_dao = None
        self._document_dao = None

    '''
    Traitement des nouvelles transactions. Le message est decode et le processus est declenche.
    En cas d'erreur, un message est mis sur la Q d'erreur. Dans tous les cas, le message va etre consomme.
    '''
    def callbackAvecAck(self, ch, method, properties, body):
        # Decoder l'evenement qui contient l'information sur la transaction a traiter
        evenement_dict = self.extraire_evenement(body)

        # Traiter la transaction: cette methode complete toujours avec succes. Les erreurs
        # sont mises sur une Q a cet effet.
        self.traiter_transaction(evenement_dict)

        # Transmettre le ACK pour indiquer que le message a ete traite
        super(OrienteurTransaction, self).callbackAvecAck(ch, method, properties, body)

    def extraire_evenement(self, message_body):
        # Extraire le message qui devrait etre un document JSON
        message_dict = self._json_helper.bin_utf8_json_vers_dict(message_body)
        return message_dict

    def charger_liste_processus(self):

        # Charger le dictionnaire des libelles. Permet une correspondance directe
        # vers un processus.

        # Liste des processus
        # MGPProcessus: MilleGrille Python Processus. C'est un processus qui va correspondre directement
        # a un "module.classe" du package millegrilles.processus.
        self.dict_libelle = {
            "MGPProcessus.Senseur.ConsignerLecture": "Senseur.ConsignerLecture"
        }

    def traiter_transaction(self, dictionnaire_evenement):
        try:
            processus_a_declencher = self.orienter_message(dictionnaire_evenement)
            # On va declencher un nouveau processus


        except ErreurInitialisationProcessus as erreur:
            # Une erreur fatale est survenue - l'erreur est liee au contenu du message (ne peut pas etre ressaye)
            doc_id = dictionnaire_evenement["_id"]
            transaction_id = dictionnaire_evenement.get("id-tramsaction")
            self._message_dao.transmettre_erreur_transaction(doc_id, transaction_id, erreur)
        except Exception as erreur:
            # Erreur inconnue. On va assumer qu'elle est fatale.
            doc_id = dictionnaire_evenement["_id"]
            self._message_dao.transmettre_erreur_transaction(id_document=doc_id, detail=erreur)

    '''
    :param message: Evenement d'initialisation de processus recu de la Q (format dictionnaire).
    
    :raises ErreurInitialisationProcessus: le processus est inconnu
    '''
    def orienter_message(self, dictionnaire_evenement):

        # L'evenement recu dans la Q ne contient que les identifiants.
        # Charger la transaction a partir de Mongo pour identifier le type de processus a declencher.
        mongo_id = dictionnaire_evenement.get("_id")
        if mongo_id is None:
            raise ErreurInitialisationProcessus(dictionnaire_evenement, "L'identifiant _id est vide ou absent")

        transaction = self._document_dao.charger_document_par_id(mongo_id)
        if transaction is None:
            raise ErreurInitialisationProcessus(dictionnaire_evenement, "Aucune transaction ne correspond a _id:%s" % mongo_id)

        # Tenter d'orienter la transaction
        processus_correspondant = None

        # Le message d'evenement doit avoir un element "libelle", c'est la cle pour MGPProcessus.
        charge_utile = transaction.get('charge-utile')
        if charge_utile is not None:

            libelle = charge_utile.get('libelle-transaction')

            if libelle is not None:
                # Determiner le moteur qui va gerer le processus
                moteur = libelle.split('.')[0]
                if moteur == 'MGPProcessus':
                    processus_correspondant = self.orienter_message_mgpprocessus(dictionnaire_evenement, libelle)
                else:
                    raise ErreurInitialisationProcessus(dictionnaire_evenement,
                                                        "Le document _id: %s est associe a un type de processus inconnu, libelle: %s" % (mongo_id, libelle))

        if processus_correspondant is None:
            raise ErreurInitialisationProcessus(dictionnaire_evenement,
                                                "Le document _id: %s n'est pas une transaction reconnue" % mongo_id)

        return processus_correspondant

    def orienter_message_mgpprocessus(self, dictionnaire_evenement, libelle):
        # On utilise le dictionanire de processus pour trouver le nom du module et de la classe
        processus_correspondant = self.dict_libelle.get(libelle)

        return processus_correspondant

'''
Exception lancee lorsque le processus ne peut pas etre initialise (erreur fatale).
'''


class ErreurInitialisationProcessus(Exception):

    def __init__(self, evenement, message=None):
        super().__init__(self, message)
        self._evenement = evenement

    @property
    def evenement(self):
        return self._evenement

