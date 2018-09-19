''' Script de test pour transmettre message de transaction

'''

from millegrilles.dao.Configuration import TransactionConfiguration
from millegrilles.dao.MessageDAO import PikaDAO

#credentials = pika.PlainCredentials('mathieu', 'p1234')
#connection = pika.BlockingConnection(pika.ConnectionParameters('cuisine', 5674, credentials=credentials))

#queuename = "mg.sansnom.nouvelles_transactions"

#connection = pika.BlockingConnection( pika.ConnectionParameters('dev2', 5672) )
#channel = connection.channel()
#channel.queue_declare(queue=queuename)

message = {
    "contenu": "valeur était à alisée",
    "nombre": 23
}

message_test_orienteur = {
    "libelle-transaction": "MGPProcessus.ProcessusTest.TestOrienteur"
}

#message_utf8 = json.dumps(message)

#channel.basic_publish(exchange='',
#                      routing_key=queuename,
#                      body=message_utf8)

#print("Sent: %s" % message)

#connection.close()

configuration = TransactionConfiguration()
configuration.loadEnvironment()
messageDao = PikaDAO(configuration)

messageDao.connecter()

enveloppe = messageDao.transmettre_message_transaction(message_test_orienteur, 'MGPProcessus.ProcessusTest.TestOrienteur')

print("Sent: %s" % enveloppe)

messageDao.deconnecter()