# Script de test pour transmettre message de transaction
import datetime
import time
import json
import requests
import tarfile
import logging
import sys

from io import BufferedReader, RawIOBase

from millegrilles.dao.Configuration import ContexteRessourcesMilleGrilles
from millegrilles.dao.MessageDAO import BaseCallback
from millegrilles.transaction.GenerateurTransaction import GenerateurTransaction
from millegrilles import Constantes
from millegrilles.Constantes import ConstantesDomaines, ConstantesBackup
from millegrilles.domaines.Principale import ConstantesPrincipale
from threading import Thread, Event
from millegrilles.util.BackupModule import ArchivesBackupParser

contexte = ContexteRessourcesMilleGrilles()
contexte.initialiser()


class MessagesSample(BaseCallback):

    def __init__(self):
        super().__init__(contexte)
        self.contexte.message_dao.register_channel_listener(self)
        self.generateur = GenerateurTransaction(self.contexte)

        self.channel = None
        self.event_recu = Event()

    def on_channel_open(self, channel):
        # Enregistrer la reply-to queue
        self.channel = channel
        channel.queue_declare(durable=True, exclusive=True, callback=self.queue_open_local)

    def queue_open_local(self, queue):
        self.queue_name = queue.method.queue
        print("Queue: %s" % str(self.queue_name))

        self.channel.basic_consume(self.callbackAvecAck, queue=self.queue_name, no_ack=False)
        self.executer()

    def run_ioloop(self):
        self.contexte.message_dao.run_ioloop()

    def deconnecter(self):
        self.contexte.message_dao.deconnecter()

    def traiter_message(self, ch, method, properties, body):
        print("Message recu, correlationId: %s" % properties.correlation_id)
        print(json.dumps(json.loads(body.decode('utf-8')), indent=4))
        print("Channel : " + str(ch))
        print("Method : " + str(method))
        print("Properties : " + str(properties))
        print("Channel virtual host : " + str(ch.connection.params.virtual_host))

    def commande_restaurerGrosFichiers(self):
        params = {
        }
        domaine = 'commande.backup.restaurerGrosFichiers'
        self.generateur.transmettre_commande(
            params, domaine, reply_to=self.queue_name, correlation_id='reply_regenerer')

    def executer(self):
        sample.commande_restaurerGrosFichiers()


# --- MAIN ---
logging.basicConfig()
logging.getLogger('millegrilles').setLevel(logging.DEBUG)
sample = MessagesSample()

# TEST

# FIN TEST
sample.event_recu.wait(240)
sample.deconnecter()