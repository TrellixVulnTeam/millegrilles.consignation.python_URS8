import logging
import os

from uuid import uuid4

from millegrilles.util.BaseTestMessages import DomaineTest
from millegrilles.Constantes import ConstantesPublication
from millegrilles.util.Chiffrage import ChiffrerChampDict


class TestPublication(DomaineTest):

    def __init__(self):
        super().__init__()
        self.__logger = logging.getLogger(self.__class__.__name__)

        self.site_id = '09906262-206c-11eb-88cc-af560af5618f'
        self.noeud_id = '639e1d3b-fa5b-4a13-86b2-d3e6148c9d99'

    def requete_liste_sites(self):
        requete = dict()
        domaine_action = 'requete.Publication.' + ConstantesPublication.REQUETE_LISTE_SITES
        correlation_id = 'test'
        self.generateur.transmettre_requete(
            requete, domaine_action, correlation_id=correlation_id, reply_to=self.queue_name)

    def requete_liste_posts(self):
        requete = {'post_ids': ['bf20add7-0355-40e7-86d4-5b0ab1fee873', 'a5e34904-ffdb-4f50-a092-86e3058f9716', '5fce6672-a644-4f1b-94e0-3fa265b4affc']}
        domaine_action = 'requete.Publication.' + ConstantesPublication.REQUETE_POSTS
        correlation_id = 'test'
        self.generateur.transmettre_requete(
            requete, domaine_action, correlation_id=correlation_id, reply_to=self.queue_name)

    def requete_config_site(self):
        requete = {'site_id': self.site_id}
        domaine_action = 'requete.Publication.' + ConstantesPublication.REQUETE_CONFIGURATION_SITE
        correlation_id = 'test'
        self.generateur.transmettre_requete(
            requete, domaine_action, correlation_id=correlation_id, reply_to=self.queue_name)

    def requete_sites_pour_noeud(self):
        requete = {'noeud_id': self.noeud_id}
        domaine_action = 'requete.Publication.' + ConstantesPublication.REQUETE_SITES_POUR_NOEUD
        correlation_id = 'test'
        self.generateur.transmettre_requete(
            requete, domaine_action, correlation_id=correlation_id, reply_to=self.queue_name)

    def requete_cdns(self):
        requete = {}
        domaine_action = 'requete.Publication.' + ConstantesPublication.REQUETE_LISTE_CDN
        correlation_id = 'test'
        self.generateur.transmettre_requete(
            requete, domaine_action, correlation_id=correlation_id, reply_to=self.queue_name)

    def maj_site(self):
        info_site = {
            ConstantesPublication.CHAMP_SITE_ID: '09906262-206c-11eb-88cc-af560af5618f',
            ConstantesPublication.CHAMP_NOM_SITE: 'Mon site',
            ConstantesPublication.CHAMP_LANGUAGES: ['fr', 'en'],
            ConstantesPublication.CHAMP_NOEUDS_URLS: {
                self.site_id: ["mg-dev3.maple.maceroc.com"]
            },
            ConstantesPublication.CHAMP_FICHIERS: {
                ConstantesPublication.CHAMP_TOUTES_COLLECTIONS: True
            },
            ConstantesPublication.CHAMP_ALBUMS: {
                ConstantesPublication.CHAMP_TOUTES_COLLECTIONS: True
            }
        }
        domaine_action = 'Publication.' + ConstantesPublication.TRANSACTION_MAJ_SITE
        self.generateur.soumettre_transaction(info_site, domaine_action, reply_to=self.queue_name)

    def maj_section(self):
        info_site = {
            # ConstantesPublication.CHAMP_SITE_ID: '2aba74c9-9273-4ba6-828f-7571149e0633',
            # ConstantesPublication.CHAMP_TYPE_SECTION: 'fichiers',
            ConstantesPublication.CHAMP_SECTION_ID: '15732780-a777-11eb-822b-afa6e29b1852',

            ConstantesPublication.CHAMP_ENTETE: {'fr': 'Fichiers'},
            ConstantesPublication.CHAMP_COLLECTIONS: ['abcd-1234', 'abcd-1235'],
        }
        domaine_action = 'Publication.' + ConstantesPublication.TRANSACTION_MAJ_SECTION
        self.generateur.soumettre_transaction(info_site, domaine_action, reply_to=self.queue_name, correlation_id='maj_section')

    def maj_partie_page(self):
        info_site = {
            # ConstantesPublication.CHAMP_SECTION_ID: '15732780-a777-11eb-822b-afa6e29b1852',
            ConstantesPublication.CHAMP_PARTIEPAGE_ID: '6b336f28-a77b-11eb-822b-afa6e29b1852',

            ConstantesPublication.CHAMP_TYPE_PARTIE_PAGE: 'texte',

            ConstantesPublication.CHAMP_TITRE: {'fr': 'Titre de ma page 2'},
            ConstantesPublication.CHAMP_HTML: {'fr': '<p>Ma page mise a jour</p>'},
            # ConstantesPublication.CHAMP_DATE_POST: '',
            # ConstantesPublication.CHAMP_CSS_PAGE: '',
            # ConstantesPublication.CHAMP_MEDIA_UUID: '',
        }
        domaine_action = 'Publication.' + ConstantesPublication.TRANSACTION_MAJ_PARTIEPAGE
        self.generateur.soumettre_transaction(info_site, domaine_action, reply_to=self.queue_name, correlation_id='maj_section')

    def maj_post(self):
        info_post = {
            "post_id": "17b2430e-c6bc-4d0b-8dd1-9787e0b5bf2a",
            # "post_id": str(uuid4()),
            "html": {
                "fr": "<h1>Mon post, en francais</h1><p>Un nouveau post</p>",
                "en": "<h1>My post, in English</h1><p>A new post</p>",
            }
        }
        domaine_action = 'Publication.' + ConstantesPublication.TRANSACTION_MAJ_POST
        self.generateur.soumettre_transaction(info_post, domaine_action, reply_to=self.queue_name, correlation_id='maj_post')

    def maj_cdn(self):

        motdepasse = None
        # motdepasse = os.environ.get('AWSS3_SECRET')
        # if motdepasse is not None:
        #     certificat = self.get_cert_maitrecles()
        #     cipher = ChiffrerChampDict(self.contexte)
        #     info_motdepasse = cipher.chiffrer(certificat, 'Publication', {'type': 'cdn', 'champ': 'awss3.secretAccessKey'}, motdepasse)
        #     motdepasse = info_motdepasse['secret_chiffre']
        #
        #     commande_maitrecles = info_motdepasse['maitrecles']
        #     domaine_maitrecles = "commande.MaitreDesCles." + commande_maitrecles['en-tete']['domaine']
        #     self.generateur.transmettre_commande(commande_maitrecles, domaine_maitrecles)

        cdn = {
            'active': True,
            'description': 'Mon CDN AWS S3',

            # 'cdn_id': '20ce2512-a506-11eb-be86-071692588846',
            # 'type_cdn': 'sftp',
            # 'configuration': {
            #     'host': '192.168.2.131',
            #     'port': 22,
            #     'username': 'sftptest',
            #     'repertoireRemote': '/home/sftptest/consignation',
            # },

            # 'cdn_id': '157b58dc-a511-11eb-be86-071692588846',
            # 'type_cdn': 'ipfs',

            'cdn_id': 'ff9bcfab-a522-11eb-be86-071692588846',
            'type_cdn': 'awss3',
            'configuration': {
                # 'bucketRegion': 'us-east-1',
                # 'credentialsAccessKeyId': 'AKIA2JHYIVE5E3HWIH7K',
                # 'secretAccessKey_chiffre': motdepasse,
                # 'bucketName': 'millegrilles',
                'bucketDirfichier': 'mg-dev4/fichiers',
            },

        }
        domaine_action = 'Publication.' + ConstantesPublication.TRANSACTION_MAJ_CDN
        self.generateur.soumettre_transaction(cdn, domaine_action, reply_to=self.queue_name, correlation_id='maj_cdn')

    def supprimer_cdn(self):
        transaction = {
            'cdn_id': 'a5b77eea-a510-11eb-be86-071692588846',
        }
        domaine_action = 'Publication.' + ConstantesPublication.TRANSACTION_SUPPRIMER_CDN
        self.generateur.soumettre_transaction(transaction, domaine_action, reply_to=self.queue_name, correlation_id='supprimer_cdn')

    def executer(self):
        self.__logger.debug("Executer")

        # self.requete_liste_sites()
        # self.requete_liste_posts()
        # self.requete_config_site()
        # self.requete_sites_pour_noeud()
        # self.requete_cdns()
        # self.maj_site()
        # self.maj_post()
        # self.maj_cdn()
        # self.maj_section()
        self.maj_partie_page()
        # self.supprimer_cdn()


# --- MAIN ---
if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('millegrilles').setLevel(logging.DEBUG)
    logging.getLogger('TestPublication').setLevel(logging.DEBUG)
    test = TestPublication()
    # TEST

    # FIN TEST
    test.event_recu.wait(10)
    test.deconnecter()
