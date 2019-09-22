from millegrilles.SecuritePKI import EnveloppeCertificat

import binascii
from cryptography.x509.oid import NameOID, ObjectIdentifier
from cryptography.x509 import NameAttribute


class CertificatSubjectTest:

    def __init__(self):
        self.cert_pem = None
        self.enveloppe = None

    def charger(self, cert_path):
        with open(cert_path, 'rb') as fichier:
            pem_file = fichier.read()

        enveloppe = EnveloppeCertificat(certificat_pem=pem_file)
        self.enveloppe = enveloppe

    def afficher_info(self):
        print("Certificat %s" % self.enveloppe.subject_rfc4514_string())


test = CertificatSubjectTest()
test.charger('/opt/millegrilles/dev2/pki/certs/dev2_maitredescles.cert.pem')
test.afficher_info()
