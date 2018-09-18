# Module de processus pour MilleGrilles
from millegrilles import Constantes
from millegrilles.dao.Configuration import TransactionConfiguration
from millegrilles.dao.DocumentDAO import MongoDAO
from millegrilles.dao.MessageDAO import PikaDAO, BaseCallback

'''
Controleur des processus MilleGrilles. Identifie et execute les processus.

MGPProcessus = MilleGrilles Python Processus. D'autres controleurs de processus peuvent etre disponibles.

'''


class MGPProcessusControleur(BaseCallback):

    def __init__(self):
        super().__init__()

        self._configuration = TransactionConfiguration()
        self._document_dao = None
        self._message_dao = None

    def initialiser(self):
        self._configuration.loadEnvironment()
        self._document_dao = MongoDAO(self._configuration)
        self._message_dao = PikaDAO(self._configuration)

    """
    Identifie le processus a executer, retourne une instance si le processus est trouve.
    
    :returns: Instance MGPProcessus si le processus est trouve. 
    :raises ErreurProcessusInconnu: Si le processus est inconnu.  
    """
    def identifier_processus(self, evenement):
        nom_processus = evenement.get(Constantes.PROCESSUS_DOCUMENT_LIBELLE_PROCESSUS)
        nom_module, nom_classe = nom_processus.split('.')
        print('Importer %s, %s' % (nom_module, nom_classe))
        module_processus = __import__('millegrilles.processus.%s' % nom_module, fromlist=nom_classe)
        classe_processus = getattr(module_processus, nom_classe)
        return classe_processus

    def charger_document_processus(self, id_document_processus):
        return self._document_dao.charger_processus_par_id(id_document_processus)

    def sauvegarder_etape_processus(self, id_document_processus, dict_etape):
        self._document_dao.sauvegarder_etape_processus(id_document_processus, dict_etape)

    """ 
    Lance une erreur fatale pour ce message. Met l'information sur la Q d'erreurs. 
    
    :param message: Le message pour lequel l'erreur a ete generee.
    :param nom_etape: Nom complet de l'etape qui a genere l'erreur.
    :param detail_erreur: Optionnel, objet ErreurExecutionEtape.
    """
    def erreur_fatale(self, id_document_processus, erreur):
        self._message_dao.transmettre_erreur_processus(
            id_document_processus=id_document_processus, detail=erreur)


class MGProcessus:

    """
    Classe de processus MilleGrilles. Continent des methodes qui representes les etapes du processus.

    :param controleur: Controleur de processus qui appelle l'etape
    :param message: Message recu qui a declenche l'execution de cette etape
    """
    def __init__(self, controleur, evenement):
        self._controleur = controleur
        self._evenement = evenement

        self._document_processus = None
        self._etape_suivante = None
        self._etape_complete = False
        self._methode_etape_courante = None
        self._processus_complete = False

    '''
    Utilise le message pour identifier l'etape courante qui doit etre executee. 
    
    :returns: Methode executable.
    :raises ErreurEtapeInconnue: Si l'evenement ne contient pas l'information sur quelle etape executer
    :raises AttributeError: Si le nom de l'etape ne correspond a aucune methode de la classe.
    '''
    def _identifier_etape_courante(self):
        # Retourner le contenu de l'element etape-suivante du message. L'etape a executer
        # est determinee par l'etape precedente d'un processus.
        nom_methode = self._evenement.get(Constantes.PROCESSUS_MESSAGE_LIBELLE_ETAPESUIVANTE)
        if nom_methode is None:
            raise ErreurEtapeInconnue("etape-suivante est manquante sur evenement pour classe %s: %s" % (self.__class__.__name__, self._evenement))
        methode_a_executer = getattr(self, nom_methode)

        return methode_a_executer

    '''
    Prepare un message qui peut etre mis sur la Q de MGPProcessus pour declencher l'execution de l'etape suivante.
    
    :returns: Libelle identifiant l'etape suivante a executer.
    '''
    def transmettre_message_etape_suivante(self, parametres=None):
        # Verifier que l'etape a ete executee avec succes.
        if not self._etape_complete and self._etape_suivante is not None:
            raise ErreurEtapePasEncoreExecutee("L'etape n'a pas encore ete executee ou l'etape suivante est inconnue")

        message = {
            Constantes.PROCESSUS_MESSAGE_LIBELLE_PROCESSUS: self.__class__.__name__,
            Constantes.PROCESSUS_MESSAGE_LIBELLE_ETAPESUIVANTE: self._etape_suivante,
            Constantes.PROCESSUS_MESSAGE_LIBELLE_ID_DOC_PROCESSUS: str(self._document_processus[Constantes.MONGO_DOC_ID])
        }
        if parametres is not None:
            message[Constantes.PROCESSUS_MESSAGE_LIBELLE_PARAMETRES] = parametres

        return message

    '''
    Execute l'etape identifiee dans le message.

    :raises ErreurExecutionEtape: Erreur fatale encontree lors de l'execution de l'etape
    '''
    def traitement_etape(self):

        id_document_processus=None
        try:
            # Charger le document du processus
            id_document_processus = self._evenement[Constantes.PROCESSUS_MESSAGE_LIBELLE_ID_DOC_PROCESSUS]
            self._document_processus = self._controleur.charger_document_processus(id_document_processus)

            # Executer l'etape
            etape_execution = self._identifier_etape_courante()
            resultat = etape_execution(self)
            self._etape_complete = True

            # Verifier s'il faut transmettre un message pour continuer le processus ou s'il est complete.
            if not self._processus_complete:
                self.transmettre_message_etape_suivante(resultat)

        except Exception as erreur:
            # Erreur inconnue. On va assumer qu'elle est fatale.
            self._controleur.erreur_fatale(id_document_processus=id_document_processus, erreur=erreur)


    '''
    Implementation de reference pour l'etape finale. 
    '''
    def finale(self):
        pass

'''
Exception lancee lorsqu'une etape ne peut plus continuer (erreur fatale).
'''


class ErreurProcessusInconnu(Exception):

    def __init__(self, message=None):
        super().__init__(self, message=message)


class ErreurEtapeInconnue(Exception):

    def __init__(self, message=None):
        super().__init__(self, message)


class ErreurEtapePasEncoreExecutee(Exception):

    def __init__(self, message=None):
        super().__init__(self, message=message)
