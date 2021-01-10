import datetime
import pytz
import logging

from os import path
from certvalidator.errors import PathValidationError
from typing import Dict

from millegrilles.Constantes import ConstantesGenerateurCertificat
from millegrilles.util.ValidateursPki import ValidateurCertificat, ValidateurCertificatCache
from millegrilles.util.X509Certificate import RenouvelleurCertificat, EnveloppeCleCert

mgdev_certs = '/home/mathieu/mgdev/certs'
idmg = 'QME8SjhaCFySD9qBt1AikQ1U7WxieJY2xDg2JCMczJST'


cert_millegrille = """
-----BEGIN CERTIFICATE-----
MIIDKDCCAhCgAwIBAgIKAwFHBgZAdyMmADANBgkqhkiG9w0BAQ0FADAnMQ8wDQYD
VQQDEwZSYWNpbmUxFDASBgNVBAoTC01pbGxlR3JpbGxlMB4XDTIwMTAwMTIzMTUz
NFoXDTIxMTAwMTIzMTUzNFowJzEPMA0GA1UEAxMGUmFjaW5lMRQwEgYDVQQKEwtN
aWxsZUdyaWxsZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALN3Oqa0
pme6ckKPaOj9ViWHYbshBZShbr27M4UQbJFuWPGczDuWYRA4o+G2XtYvN7IKix4F
Jk5KAhvaBlX6TERZpqTCbmZDg5okkr7LSUroiH4TSjuPqfAqI2XoeHTKQ4QOEKWd
53eu+nbtJ9NDnCe6HYs0nNhsH4DluiCWeoPp862mFPs77Vi00JM8WuQZxrzv0kMi
1izPv0P0DHQ7PLtoVwi7to0GCgXeun4bWGbA3jYjd52IwVSsN34ICLhwu7NxjTEA
qCmqOoxuwZeF9mtOZpyufMT+9M2yRiQ/M3ORSO0DbiyfnERMSEK1y6cDNIoqSm3E
Kq80fkKUmjeGtwMCAwEAAaNWMFQwEgYDVR0TAQH/BAgwBgEB/wIBBTAdBgNVHQ4E
FgQUz0uNp3laAnmytcjpRPxeffzn4YIwHwYDVR0jBBgwFoAUz0uNp3laAnmytcjp
RPxeffzn4YIwDQYJKoZIhvcNAQENBQADggEBADlSMp60EefJ6RezKMf6WP2VYZsC
iM8/HtGmHBk6Y0EEbX0BZlifufrNB3YH8klfYBrxkwPOhku1vaylAtf5xxB3kD+1
Vmxr2mkO9PSJTw+ehDs7tAfOFC/kOy7MCywB/Ysg1oEiQ/uVT51c3zAXDWn+H84k
Vx/4wYGdLVamGVYFU7NSVhzfFED6zZRDn7S+/ncZwhkxmZXIBOl3moWRUA8dBBZp
kD5whYSBNXy9CnaVaVjMW/AwynM+bBiUlVEXXIUw6wyLdkh76srVpyAGm0kVJ4J/
CH5fQslgzRhcQBInXaaV+vB9ac624tzpUy+Mt4vmEsoVbDMGZewpH8hFvtM=
-----END CERTIFICATE-----
"""

cert_1_intermediaire = """
-----BEGIN CERTIFICATE-----
MIIDfzCCAmegAwIBAgIKBHMSAgGWVkgAADANBgkqhkiG9w0BAQ0FADAnMQ8wDQYD
VQQDEwZSYWNpbmUxFDASBgNVBAoTC01pbGxlR3JpbGxlMB4XDTIxMDEwODIwNTcz
NVoXDTI0MDExMTIwNTczNVowfjEtMCsGA1UEAxMkMmRkYjJiNDktMTZhNS00MmMy
LTg3NzItYzJiZTRhNDdmN2M1MRYwFAYDVQQLEw1pbnRlcm1lZGlhaXJlMTUwMwYD
VQQKEyxRTUU4U2poYUNGeVNEOXFCdDFBaWtRMVU3V3hpZUpZMnhEZzJKQ01jekpT
VDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANQlnhWapHBfWgFxJHkt
uY1kojDMrW1OsN/5Z9xsZzxFd6K7Y6Ezr+fgcIij+2kMPLCSH2cNNcwuclJEnHWT
n4xM/MpmALC08cftiqC92QzbonnLGFUuZvk5dXup+sfLkP7rXlHEqfYVsHCuKr8e
YGBZ0pJesgPAvStAFLHqbv/aKBgSd0gWJvlM0rF7QKIOUueamgZNutvPf49Vv+uT
/sKK1VvlJifvL1CIRMzwYcHzSFz24xey7RIMQMpNOzLfw+gddidAivlFHOOthRPx
1qGHM5oPUOBw0LDFX01CopCzXv2LpXD3gFKguwdW2tcAU15ggWzfy2YPeYLb/A3v
JYsCAwEAAaNWMFQwEgYDVR0TAQH/BAgwBgEB/wIBBDAdBgNVHQ4EFgQUHBhBnTsD
AdlyW/8WGcU4St+LtLowHwYDVR0jBBgwFoAUz0uNp3laAnmytcjpRPxeffzn4YIw
DQYJKoZIhvcNAQENBQADggEBAD578RJjXQppZD4iiG9uyQFIl4vqTjsM/+RdWI20
iDsR1Bi9j07y8+5H5nW/Nqsu541bYx1XkdkG596m1gB2gJcNT0cGJpPG8NNfsDaw
9cvudLCJAIJyU0KYHGhJYnGjcBcSV8isYOEgKfRCxBp5KuPNXrANznvmEe/NOZQb
Z0FzCi7RCVMKQ3b46Nrmd+qpzESTyuEaB5yTTZZlqrb49BePi+KR/5NkIP+kK8QH
Y3zrbUFrVbYftK3BKuaACIOnIqafOpMJ1zi7co26LaWj9syETwRt+EjxoQzgiN08
QHg5RZ88D4WtDr+1jYvT4F3Kb03Ms27jy+F42XI51uoNhIo=
-----END CERTIFICATE-----
"""

cert_1_expire = """
-----BEGIN CERTIFICATE-----
MIIEYTCCA0mgAwIBAgIUcKt2m+TJ/BaUBTK7RoSpwLLOjVMwDQYJKoZIhvcNAQEL
BQAwfjEtMCsGA1UEAxMkMmRkYjJiNDktMTZhNS00MmMyLTg3NzItYzJiZTRhNDdm
N2M1MRYwFAYDVQQLEw1pbnRlcm1lZGlhaXJlMTUwMwYDVQQKEyxRTUU4U2poYUNG
eVNEOXFCdDFBaWtRMVU3V3hpZUpZMnhEZzJKQ01jekpTVDAeFw0yMTAxMDkxOTU2
MzhaFw0yMTAxMDkyMDU4MzhaMHgxNTAzBgNVBAoMLFFNRThTamhhQ0Z5U0Q5cUJ0
MUFpa1ExVTdXeGllSlkyeERnMkpDTWN6SlNUMRAwDgYDVQQLDAdtb25pdG9yMS0w
KwYDVQQDDCQyZGRiMmI0OS0xNmE1LTQyYzItODc3Mi1jMmJlNGE0N2Y3YzUwggEi
MA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCu9BTZ7SC+A0VcoP14a+C0Ij1i
z7s8AhQNTqpMcadMGyJqF9vGkHwesOnPx72ZEimIPwQKguFRR8CV456zRlw91Qa3
P86nGJMFfgWkaT+CQHqXcV2DCM28TbvcT1em+yzNBzsSrI203wmJzHGiI0+so1oe
IysAxXIRWaX5xoWwXs/tOYN2tHpVxDa2vdkrLidgnqPsYBsmBXtl+sqBtDLZ1FuS
iH+Oa8hFIDLRSGAI3F5/uKQ165ZkBvfaSekKNyXhAwUo4AnTUuGuvstN1E4FNSMG
A+fPPYBiTPg7j0b92sla0Yad/jLs9gCDkUNdlT/iPXgBNARne1b+RW0M7d8hAgMB
AAGjgdwwgdkwHQYDVR0OBBYEFBCelZdfmMGrNBbhkj4/BduX/lO5MB8GA1UdIwQY
MBaAFBwYQZ07AwHZclv/FhnFOErfi7S6MAwGA1UdEwEB/wQCMAAwCwYDVR0PBAQD
AgTwMCIGBCoDBAAEGjQuc2VjdXJlLDMucHJvdGVnZSwyLnByaXZlMA8GBCoDBAEE
B21vbml0b3IwRwYDVR0RBEAwPoIkMmRkYjJiNDktMTZhNS00MmMyLTg3NzItYzJi
ZTRhNDdmN2M1hwR/AAABhxAAAAAAAAAAAAAAAAAAAAABMA0GCSqGSIb3DQEBCwUA
A4IBAQAutCBqJvencnOkznhm0CvsZQVZCPaeGMz6ESfkgVlTaiHSiJDu79rmKNdF
9HX8Lzae7pAD4ZIyGeVznq8j+HxG6WXWoHrxahN707jOSmDdVoRDhjcq/Oo9VThv
lDesB0sX4SQpt6cyRcLz8Pw0xT364VwLhitXF/XrS03jgHusCDBtq3ZnXUYhnwnX
U/ho5SogCwjFmuH6u5qM5S+d6m77o2hYqi3jBKeM1dJVJ9RX0lRO2UQ6v49VYYdT
z3E0T3HtHJYXdC+ExxQWGYoQcXRjL01PG0CcOAfRdzAbqimca/fudl2NgkqW7Os3
vtYumyCsL6Qb/m3DW8OmFmiElePC
-----END CERTIFICATE-----
"""

dict_ca = dict()


def generer_certificat_valide() -> EnveloppeCleCert:
    ca_autorite = EnveloppeCleCert()
    ca_autorite.cert_from_pem_bytes(cert_millegrille.encode('utf-8'))

    with open(path.join(mgdev_certs, 'pki.intermediaire.key'), 'rb') as fichiers:
        inter_key = fichiers.read()
    with open(path.join(mgdev_certs, 'pki.intermediaire.passwd'), 'rb') as fichiers:
        inter_passwd = fichiers.read()
    with open(path.join(mgdev_certs, 'pki.intermediaire.cert'), 'rb') as fichiers:
        inter_cert = fichiers.read()

    clecert_intermediaire = EnveloppeCleCert()
    clecert_intermediaire.from_pem_bytes(inter_key, inter_cert, inter_passwd)

    renouvelleur = RenouvelleurCertificat(idmg, dict_ca, clecert_intermediaire, ca_autorite)
    cert_enveloppe = renouvelleur.renouveller_par_role(ConstantesGenerateurCertificat.ROLE_DOMAINES, 'test', duree=7)

    return cert_enveloppe


class ValiderCertificat:

    def __init__(self, certs: Dict[str, EnveloppeCleCert]):
        self.validateur = ValidateurCertificat(idmg='QME8SjhaCFySD9qBt1AikQ1U7WxieJY2xDg2JCMczJST')
        self.validateur_cache = ValidateurCertificatCache(idmg='QME8SjhaCFySD9qBt1AikQ1U7WxieJY2xDg2JCMczJST')
        self.certs = certs
        self.__logger = logging.getLogger('__main__.ValiderCertificat')

    def test_valider_1(self):
        enveloppe1 = self.certs['1']
        self.validateur.valider(enveloppe1.chaine)

        date_reference = datetime.datetime(year=2010, month=1, day=1, hour=0, minute=0, tzinfo=pytz.UTC)
        try:
            self.validateur.valider(enveloppe1.chaine, date_reference=date_reference)
        except PathValidationError as pve:
            self.__logger.debug(" ** OK ** -> Message validation avec validateur implicite : %s" % pve)
        else:
            raise Exception("Erreur de validation, date n'a pas ete flaggee comme invalide")

    def test_valider_cache(self):
        # Tester chargement precedent du cert de millegrille (implicitement)
        enveloppe1 = self.certs['1']
        self.validateur_cache.valider(enveloppe1.chaine)

        enveloppe_cache = self.validateur_cache.get_enveloppe(enveloppe1.fingerprint_sha256_b64)
        if enveloppe_cache.fingerprint_sha256_b64 != enveloppe1.fingerprint_sha256_b64 is None:
            raise ValueError("Certificat pas conserve dans le cache")

        self.__logger.debug("Certificat conserve dans le cache et valide : %s" % enveloppe_cache.est_verifie)

        enveloppe_millegrille_cache = self.validateur_cache.get_enveloppe('XE1aGDnW9LmXg9svOFQXy0LSiWojyp0ipHBPlt5SirA=')
        self.__logger.debug("Certificat millegrille conserve dans le cache et valide : %s" % enveloppe_millegrille_cache.est_verifie)

        self.validateur_cache.entretien()


def main():
    logging.basicConfig()
    logging.getLogger('__main__').setLevel(logging.DEBUG)

    cert_valide_1 = generer_certificat_valide()
    certs = {
        '1': cert_valide_1,
    }

    test = ValiderCertificat(certs)
    # test.test_valider_1()
    test.test_valider_cache()


if __name__ == '__main__':
    main()