import ast
import configparser
import os.path

import pgpy
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

config = configparser.ConfigParser()
config.read('sierra.ini')

repository_name = os.getenv("SIERRA_REPOSITORY_NAME", config['SIERRA']['repository_name'])
hostname = os.getenv("SIERRA_HOSTNAME", config['SIERRA']['hostname'])
email = os.getenv("SIERRA_EMAIL", config['SIERRA']['email'])
secure = os.getenv("SIERRA_SECURE", ast.literal_eval(config['SIERRA']['secure']))

version = "0.1.5"

def make_key():
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
    uid = pgpy.PGPUID.new(pn=repository_name, comment=f"Sieloader Repository, {hostname}",
                          email=email)
    key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA512],
                ciphers=[SymmetricKeyAlgorithm.AES256],
                compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP,
                             CompressionAlgorithm.Uncompressed])
    with open("key.pgp", "w") as file:
        file.write(str(key))

# loading pgp key
if not os.path.isfile("key.pgp"):
    make_key()

pgpkey = pgpy.PGPKey.from_file('key.pgp')[0]
if pgpkey.userids[0].name != repository_name or pgpkey.userids[0].email != email or pgpkey.userids[0].comment != f"Sieloader Repository, {hostname}":
    make_key()
    pgpkey = pgpy.PGPKey.from_file('key.pgp')[0]

