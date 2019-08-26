# Script de test pour transmettre message de transaction

import datetime, time

from millegrilles.dao.Configuration import ContexteRessourcesMilleGrilles
from millegrilles.dao.MessageDAO import BaseCallback
from millegrilles import Constantes
from millegrilles.domaines.Principale import ConstantesPrincipale
from millegrilles.dao.MessageDAO import JSONHelper

from threading import Thread, Event


class BaseEnvoyerMessageEcouter(BaseCallback):

    def __init__(self):
        super().__init__(ContexteRessourcesMilleGrilles())
        self.contexte.initialiser(init_document=False)
        self.__thread_ioloop = Thread(name="MQ-ioloop", target=self.contexte.message_dao.run_ioloop)
        self.__thread_ioloop.start()
        self.generateur = self.contexte.generateur_transactions
        self.message_dao = self.contexte.message_dao
        self.pret = Event()
        self.recu = Event()

        # Enregistrer la reply-to queue
        print("Attente du channel")
        self.contexte.message_dao.attendre_channel(5)
        self.channel = self.message_dao.channel
        self.channel.queue_declare(durable=True, exclusive=True, callback=self.set_cb_queue)
        self.queue_name = None
        self.pret.wait(5)

    def set_cb_queue(self, queue):
        self.queue_name = queue.method.queue
        print("Queue: %s" % str(self.queue_name))
        self.channel.basic_consume(self.callbackAvecAck, queue=self.queue_name, no_ack=False)
        self.pret.set()

    def deconnecter(self):
        self.contexte.message_dao.deconnecter()

    def lire_message(self, body):
        json_helper = JSONHelper()
        message_dict = json_helper.bin_utf8_json_vers_dict(body)
        print(str(message_dict))

    def traiter_message(self, ch, method, properties, body):
        print("Message recu, correlationId: %s" % properties.correlation_id)
        self.lire_message(body)

        self.recu.set()

    # def requete_profil_usager(self):
    #     requete_profil = {
    #         'filtre': {
    #             Constantes.DOCUMENT_INFODOC_LIBELLE: ConstantesPrincipale.LIBVAL_PROFIL_USAGER,
    #         }
    #     }
    #     requetes = {'requetes': [requete_profil]}
    #     enveloppe_requete = self.generateur.transmettre_requete(
    #         requetes, 'millegrilles.domaines.Principale', 'abcd-1234', self.queue_name)
    #
    #     print("Envoi requete: %s" % enveloppe_requete)
    #     return enveloppe_requete
    #
    # def envoyer_empreinte(self):
    #
    #     empreinte = {
    #         'cle': 'absfoijfdosijfds'
    #     }
    #
    #     enveloppe_val = self.generateur.soumettre_transaction(
    #         empreinte, 'millegrilles.domaines.Principale.creerEmpreinte', reply_to=self.queue_name, correlation_id='efgh')
    #
    #     print("Sent: %s" % enveloppe_val)
    #     return enveloppe_val
    #
    # def ajouter_token(self):
    #
    #     token = {
    #         'cle': 'cle_3'
    #     }
    #
    #     enveloppe_val = self.generateur.soumettre_transaction(
    #         token, 'millegrilles.domaines.Principale.ajouterToken', reply_to=self.queue_name, correlation_id='efgh')
    #
    #     print("Sent: %s" % enveloppe_val)
    #     return enveloppe_val
