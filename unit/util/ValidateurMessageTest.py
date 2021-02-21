import json

from cryptography.exceptions import InvalidSignature

from unit.helpers.TestBaseContexte import TestCaseContexte
from millegrilles.util.ValidateursMessages import ValidateurMessage
from millegrilles.util.Hachage import ErreurHachage
from millegrilles.dao.MessageDAO import CertificatInconnu


IDMG = 'z2RACWHAFSqghq8EaTg5HSGKNPBr3uBfpcpLmBTJa9SEK9MmbD6cA2'

MESSAGE_1 = {
    "allo": True,
    "en-tete": {
        "idmg": "DUMMY",
        "uuid_transaction": "86cdc7a0-7464-11eb-b661-8d9c3f81d76e",
        "estampille": 1613926067,
        "version": 6,
        "domaine": "Domaine.test",
        "hachage_contenu": "mEiAcD18IXkmUeneUYOVwRvGBKt+foKqzudR0qdN/QNT7YQ",
        "fingerprint_certificat": "zQme3bKbUD9WMbRZqv7qAoxybERFvAjymDixCiqhrfjwDHD"
    },
    "_signature": "mAZTPlNXHyUtIxqJFKNywomL4tuBFz5JyTZNdKdvD8yR2ogIrpk7ofI4xr8+FEH40FvRZ+fB++EEZ4dkgKR7i6FyrHvOn0T+RHxwLBkSUXGevwVjGRWQniA9F+vylWwujFgiDSzIh5GyqaGszVHIXsSSUfAbWIZSZ3KtH2j3dx7e5ImvFYIOPTcxke8JPYAnhyYj4LnhVq0E3O0ZmtIEYc3LOkzD+r7rAmiXnEeGiNTvd1FWamPacxDJ0AloTBLdnFadxIENh15o2u9YV2e+JJ02+CmNAy+NfGWnWQnhBGp03MZ0tzNKDIv56sYJUMobAwQHHXhIXfSn/PUla7ss7G8I",
    "_certificat": [
    "-----BEGIN CERTIFICATE-----\nMIIEEzCCAvugAwIBAgIUTKhREB7RyahKoBIHZMqAQ+amvPMwDQYJKoZIhvcNAQEL\nBQAwgZoxPzA9BgNVBAoMNnoyUkFDV0hBRlNxZ2hxOEVhVGc1SFNHS05QQnIzdUJm\ncGNwTG1CVEphOVNFSzlNbWJENmNBMjEWMBQGA1UECwwNSW50ZXJtZWRpYWlyZTE/\nMD0GA1UEAww2ejJSQUNXSEFGU3FnaHE4RWFUZzVIU0dLTlBCcjN1QmZwY3BMbUJU\nSmE5U0VLOU1tYkQ2Y0EyMB4XDTIxMDIyMTE2NDU0N1oXDTIxMDMyNDE2NDc0N1ow\naDE/MD0GA1UECgw2ejJSQUNXSEFGU3FnaHE4RWFUZzVIU0dLTlBCcjN1QmZwY3BM\nbUJUSmE5U0VLOU1tYkQ2Y0EyMREwDwYDVQQLDAhkb21haW5lczESMBAGA1UEAwwJ\ndW5pdF90ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA/m889tUZ\n9FQ4W6IU1zqi+W7mLHD5u94SbJn1dNovrFAqqiVc7T7Ektm8WcpmuF5i3js8D0ai\nQv5pqAhTrXCOGP6ufXoBO0FW8NVj+GPcvooZBl93s6L9H1S+R0BDGAaNDk/3BNzn\nz9+kAjKq8kmZ8jbV2DWVS6JByzkEoe8xK6jjTLifEL9WWkuZuTDOIeNe/lRfz58u\nhcmyktrzFbRKaFtIh8NbrPSqxLUPPD0XbIwnDC9e5u5JOhWXXnfiMV2hJGDSB9LH\nqCx93Pj51R1Q2JqdYpIjvruXph6vXeQ5uuauCgepdSjyOUancFmatPdi9tOeZpVE\nxl+H+owSSiZKQQIDAQABo4GBMH8wHQYDVR0OBBYEFHkzhaVv+2qM7xEkUYsAyMS8\n5yadMB8GA1UdIwQYMBaAFG+t/BHETxLNF6O617zZ7063GYjEMAwGA1UdEwEB/wQC\nMAAwCwYDVR0PBAQDAgTwMBAGBCoDBAAECDQuc2VjdXJlMBAGBCoDBAEECGRvbWFp\nbmVzMA0GCSqGSIb3DQEBCwUAA4IBAQCAc9ggkqZt1Nhj9z46uFWCge7e362zCIxv\ndT+ptRoqdw2DaYS1Ssca6ASkjjdqFNu3xSyf3kYD0SjUWnZ083o1GZL9n3c2L+Mw\ntoiHpiSbEhQG4FhLqPlZBHmQHAKf7dIODdyCqTm6aoUBbjyNM0+RRFw7siHjz8s1\nDa2Zbtj21V9/lPEqMQNOjS0wCzmW7bs7+tCY6LDaAfalGedOL+tqJCAR4k4yDbJ7\nBbkjRF1+MW2FvX0BKpJaOoNriRFr+U6VjpUqXbtIuuNAcu9mxEO9vnj28GqcA8jL\ntU03KSbdHtLsoejkhSs514mV1nvoVJ2ltMHVrPUsePhTIFgY3PMN\n-----END CERTIFICATE-----\n",
    "-----BEGIN CERTIFICATE-----\nMIIEszCCApugAwIBAgIUBB0GVlURk+vwX8BjIX6jAURrKRgwDQYJKoZIhvcNAQEL\nBQAwJzEUMBIGA1UECgwLTWlsbGVHcmlsbGUxDzANBgNVBAMMBlJhY2luZTAeFw0y\nMTAyMjExNjQ1NDdaFw0yMTAzMjQxNjQ3NDdaMIGaMT8wPQYDVQQKDDZ6MlJBQ1dI\nQUZTcWdocThFYVRnNUhTR0tOUEJyM3VCZnBjcExtQlRKYTlTRUs5TW1iRDZjQTIx\nFjAUBgNVBAsMDUludGVybWVkaWFpcmUxPzA9BgNVBAMMNnoyUkFDV0hBRlNxZ2hx\nOEVhVGc1SFNHS05QQnIzdUJmcGNwTG1CVEphOVNFSzlNbWJENmNBMjCCASIwDQYJ\nKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKxrIWXJhewPiVcRSyysq817N4/RxpFg\nrtLcdtDnJ/txbtJIdcV7X+y714HgVYHPvZO4mc1Rk53CVh9YS4uKL83Az1ksbYYG\n97G2lPJPjkLY/ycAxo0yZaweeVFCJPaQRrJ3qR3qS5nGiSHD/gLxRnSdoYnYw3Ps\n9VIG02WsB5bBDrhwXGe1ZVQ7Um03L6pa4xHQObKgDXVddrZ2kwkV38JpQv1a/1W5\nHAvnQwHvlD/w5j3I4arPJzCvJ7cqaPFl99FpnLT9O3S68MxOyiRvd0eQ8rQohnx1\n7+DkrGJ6nImyFwcZ+pFOr+Aipu5zDDaLqCcYhqE6Oipu4jqqxMgyD1ECAwEAAaNj\nMGEwHQYDVR0OBBYEFG+t/BHETxLNF6O617zZ7063GYjEMB8GA1UdIwQYMBaAFE44\nJLSB/bvYgljhsEwESKiQtYq3MBIGA1UdEwEB/wQIMAYBAf8CAQQwCwYDVR0PBAQD\nAgL8MA0GCSqGSIb3DQEBCwUAA4ICAQA5VE5pnaQz1YoffGc10i+FSw3aUWauy2y9\n4hKUZJFBrUpnvZUy0j98EdPbI2ti192/dAaeJ2QjPiliJ5hAKV6cAGthOQVFhw/i\n5bdixm0PbEdnf1KtHCQPgMlcolw2MVzBHoXU705brKAixiac+6sdFQEzE2KDLmvZ\nqEnrYGPQ692q7E+1IuVJNV75pftTq3ZhBqtpIFhv+Y5oyG487TrgX+v5uNzPwU2r\naalDhejjLeLGhT/QbwiW006B0ONi25P4fmd3aGA49RAVKEucF/p/piyVigpjhrzu\nALlcnK4TiLQ8ByT5WNumnddBu0Q4zdt/dj7IgPHjfJVT8TwydGl8QM5aigCdZwSK\nYtCKqfp4cW5K4q6ygDunr68qGqwlF/tLD+Pez9RP1LLfg/yHlkSvkVOACOue3Arp\nRWyK0X5ojyIIKpmsKY7zECWLKvSw/vV2cdAdAi4/ZSB7Fk+HYqwDP/fHsAjcoxe+\nM6iBTO2vxnSCtoYS7sNW4vIFgeBUtkQjcsjZh84EpUMEDFBaQunSiZxNvvWzeOnh\n2Q4/z3ZpZ4zl6tMHS0ThC2rvQ0kmgDf8kP7E+/3I6mQmTSUeaDsWGwrfcj0FZm0H\nPf8nbkPNVhpC9SX1sVxKCrKNVGWoMLLhoh1yxVoOZ6n9svna4YQSpY3Fxaunr7aY\nZWVJbvl0mQ==\n-----END CERTIFICATE-----\n",
    "-----BEGIN CERTIFICATE-----\nMIIFMjCCAxqgAwIBAgIUZt8j6LG+nsSb1wsrxjmWmSn5lzUwDQYJKoZIhvcNAQEN\nBQAwJzEUMBIGA1UECgwLTWlsbGVHcmlsbGUxDzANBgNVBAMMBlJhY2luZTAeFw0y\nMTAxMTQxODU3NTZaFw0zMTAxMTcxODU5NTZaMCcxFDASBgNVBAoMC01pbGxlR3Jp\nbGxlMQ8wDQYDVQQDDAZSYWNpbmUwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIK\nAoICAQDu4dTDbd9Wz3elIVisJdBedhmhtxdmgxefKEg5uu415TfICVI4c8ay7Qav\nn22S1C6LyVgB0aK1VD5NS+0fPp2sFmDQ7kP+s7QIjHkNCT6CL/n3SdLRN5gexyc1\ntDd52sDAmVuXqBReQ6xDaHWc94QTbMC3eqrAhtMUjG9XMcoyW0u9LT9d7w3AElYT\nzlkAcTSMmshqg893PQPzbOxjnSiLzsAUWuBrYYXx83jmMKaj6WPJ7tTFRZgZnfId\nuso7rl3UpnjoFBLN9AdhKWFPmt7jnVxxaN0JwG+7elxhR007lJD2RylLtHhcPSCx\nWiMZlFLTG+U+tFZgXRh5DeO1v5/vEj97JU6GX7tZG+0K0UdUa8MDvsToooFq33DV\nG5Al6odx+KLATGhBm/l1HIr9LVrj+5tVklXZpaB0P8SAlic8sEF+YpLjRQLueND3\nsi+TpKCg6S83fMJRdp0bTXNe3oeukB8DQxaH7OqksHzMvYZnLpqjSrTrg2kmtS3z\nwm6KOLXxHzE7r85m5o60SOO++C5gDxAAzwKFABZ0UhhzycMekEMTcqB+h23OQYJK\nFVtdhK95A0nMQGeQqthOyIeAAmEzmCZX2SrDhF3mK1N5PDaHdv6bGPJNHzm5wMQc\nnJcVTJCK9+jmFAVnEZfzphjOHcWtd95XqOYb6kkUAWxca6zGOwIDAQABo1YwVDAd\nBgNVHQ4EFgQUTjgktIH9u9iCWOGwTARIqJC1ircwEgYDVR0TAQH/BAgwBgEB/wIB\nBTAfBgNVHSMEGDAWgBROOCS0gf272IJY4bBMBEiokLWKtzANBgkqhkiG9w0BAQ0F\nAAOCAgEAd/8X18Yt8p6L+ox7Hm23BokcVY6AfZOJajDECuVPlVqUvqu6puP2u+uk\nyg1NPPmPTA981L9EQXGmW8fuwcvlJqiUueIszPqk1Zo2Zg6EvcSHJ93d3SPcDo+W\nzTxrfNFDhVxnlp6RdiaYuhJzAZKICA4EJFi7rogKMdcxrzDk7yNAguoU9pkRM3oP\nnKyCqe34madILHHYTir25wcaV3WsSrY+BmjSTgJkoAUWnuSWKa6fvbcocYmELSIu\nnNcpavckTMPEYwLBA7xxVUppSKdXN4vOCRJVAh6NOx+NW4XhN/rb+ltSFFO87oIG\n3+YihVbIith5Xj0GzUswyOX3gn2SJlXjk+B5UIiOh8cd3U4HarquArnn3cf4P5Ev\n3d6J8i6oq0RQzguu6ER6JcwWkWI9psDag0GTxYUG1oQ99hSsxYavdlonJAao/hS8\ni6vDK150gjFv4+mxanmuGxxgr3f5Kzu+NxwSsCVJGZ3ckyRK/SQlnGHe7K6YncTW\nuEeeBOTeRYnf25D+2lr/MpCtkz5i3DHc3eI9FfeAbmDUI6O5NxYz5pBytb4zQ8Sz\neIdNRGmLNchR/uWo9Wnenvz7DAmqteUWm9Lo+5EStaYesIyHeuirUsKDSJVyS+s6\nZE4ROy5y+dG0q3rgtYWkRh5Jseo1fwtVE2IQ/WhPpi9jdFX4DRw=\n-----END CERTIFICATE-----\n"
    ]
}


class ValidateurMessageTest(TestCaseContexte):

    def setUp(self) -> None:
        self.validateur = ValidateurMessage(idmg=IDMG)

    def testValiderMessage1(self):
        self.validateur.verifier(MESSAGE_1)

    def testValiderMessage1_hachage_mismatch(self):
        message = MESSAGE_1.copy()
        message['dummy_valeur'] = 1
        self.assertRaises(ErreurHachage, self.validateur.verifier, message)

    def testValiderMessage1_signature_mismatch(self):
        message = MESSAGE_1.copy()
        message['_signature'] = 'mAU5zlOzqEgpLz1MDQenoDo9D15CwqTUVfZQzWRxuwcd+viV/Ofp/dpuFC8k7YE/RPyb5My2coRrtmNZixxd321FFp6XGmpklSndxxxw3v1alybU22TygKkomh2k5USpMjgnbkXwZ1gOIxzRg3hfq1heuIq+jNhoNr0p6NrebMHlC1glc4O3Q1x6j/V/S3Alh2zzuGPRyHOVnJE6DAmnDqxAnb/Zjc+o4t3YXetZ2tr0ww7ohOMW3RzPGkrUJuIwGrUNdSJtBiLogDRclyAadB5GPt6c0q8rRprj1bbECKrd1r8OAoc/HWmsLMLFNeE5RVUCLkzmG19WmIy6dPetJgvg'
        self.assertRaises(InvalidSignature, self.validateur.verifier, message)

    def testValiderMessage1_entete_modifiee(self):
        message = MESSAGE_1.copy()
        message['en-tete'] = message['en-tete'].copy()
        message['en-tete']['dummy'] = 1
        self.assertRaises(InvalidSignature, self.validateur.verifier, message)

    def testValiderMessage1_fingerprint_modifie(self):
        message = MESSAGE_1.copy()
        message['en-tete'] = message['en-tete'].copy()
        message['en-tete']['fingerprint_certificat'] = 'DUMMY'
        self.assertRaises(CertificatInconnu, self.validateur.verifier, message)
