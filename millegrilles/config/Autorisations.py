# Contients des configurations sous forme de constantes

class ConstantesAutorisation:
    REGLE_DOMAINEACTIONS_PERMIS = 'domaineactions_permis'  # Domaine-actions toujours permis (date = message)


_autorisations_idmg = {
    "version:": 1,
    "QME8SjhaCFySD9qBt1AikQ1U7WxieJY2xDg2JCMczJST": {
        "description": "Signature pour les catalogues officiels MilleGrille",
        ConstantesAutorisation.REGLE_DOMAINEACTIONS_PERMIS: frozenset([
            "CatalogueApplications.majDomaine",
            "CatalogueApplications.catalogueDomaines",
            "CatalogueApplications.catalogueApplication"
        ])
    }
}


def autorisations_idmg():
    return _autorisations_idmg.copy()


class Constantes:
    REGLE_CERTIFICAT_DATE_MESSAGE = 'certificat_date_message'
