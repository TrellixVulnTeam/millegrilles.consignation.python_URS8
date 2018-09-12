''' Script de test pour transmettre message de transaction

'''

import pika
import json, time

from millegrilles.transaction.Configuration import TransactionConfiguration
from millegrilles.transaction.MessageDAO import PikaDAO, BaseCallback


#credentials = pika.PlainCredentials('mathieu', 'p1234')
#connection = pika.BlockingConnection(pika.ConnectionParameters('cuisine', 5674, credentials=credentials))

#queuename = "mg.sansnom.nouvelles_transactions"

#connection = pika.BlockingConnection( pika.ConnectionParameters('dev2', 5672) )
#channel = connection.channel()
#channel.queue_declare(queue=queuename)

message = {
    "contenu": "Valeur"
}

#message_utf8 = json.dumps(message)

#channel.basic_publish(exchange='',
#                      routing_key=queuename,
#                      body=message_utf8)

#print("Sent: %s" % message)

#connection.close()

configuration = TransactionConfiguration()
transactionDAO = PikaDAO(configuration)

transactionDAO.connecter()

enveloppe = transactionDAO.transmettre_message_transaction(message)

print("Sent: %s" % enveloppe)

transactionDAO.deconnecter()