# Script de test pour transmettre message de transaction

from millegrilles import Constantes
from millegrilles.util.BaseSendMessage import BaseEnvoyerMessageEcouter
from millegrilles.domaines.Taches import FormatteurEvenementNotification, TachesConstantes

import datetime

class MessagesSample(BaseEnvoyerMessageEcouter):

    def __init__(self, uuid):
        super().__init__()
        self.uuid = uuid
        self.transmettre_certificat()

    def deconnecter(self):
        self.contexte.message_dao.deconnecter()

    def traiter_message(self, ch, method, properties, body):
        print("Message recu, correlationId: %s" % properties.correlation_id)
        print(body)

    def notification_tache(self):
        formatteur = FormatteurEvenementNotification(
            TachesConstantes.DOMAINE_NOM,
            TachesConstantes.COLLECTION_DOCUMENTS_NOM,
            self.contexte.generateur_transactions,
        )

        source = {
            Constantes.DOCUMENT_INFODOC_LIBELLE: 'configuration',
        }
        collateur = {
            Constantes.DOCUMENT_INFODOC_LIBELLE: 'configuration_13',
        }
        valeurs = {
            'version': 2
        }

        formatteur.emettre_notification_tache(source, collateur, valeurs)
        print("Sent")

    def marquer_tache_completee(self):
        transaction = {
            TachesConstantes.LIBELLE_UUID_TACHE: self.uuid,
            TachesConstantes.LIBELLE_ACTION: TachesConstantes.ACTION_VUE,
        }
        domaine = TachesConstantes.TRANSACTION_ACTION_TACHE_COMPLETEE

        generateur = self.contexte.generateur_transactions
        generateur.soumettre_transaction(transaction, domaine)

    def marquer_tache_rappel(self):
        current_time = datetime.datetime.utcnow()
        time_delta = datetime.timedelta(minutes=1)
        rappel_time = current_time + time_delta

        transaction = {
            TachesConstantes.LIBELLE_UUID_TACHE: self.uuid,
            TachesConstantes.LIBELLE_RAPPEL_TIMESTAMP: int(rappel_time.timestamp()),
            TachesConstantes.LIBELLE_ACTION: TachesConstantes.ACTION_RAPPEL,
        }
        domaine = TachesConstantes.TRANSACTION_ACTION_TACHE_RAPPEL

        generateur = self.contexte.generateur_transactions
        generateur.soumettre_transaction(transaction, domaine)

# --- MAIN ---
sample = MessagesSample(uuid='cb21763c-fcb6-49ef-b035-13044b96eb5b')

# TEST
# enveloppe = sample.maj_email_smtp_sanspassword()
# enveloppe = sample.notification_tache()
# enveloppe = sample.marquer_tache_completee()
enveloppe = sample.marquer_tache_rappel()


sample.recu.wait(10)

# FIN TEST
sample.deconnecter()
