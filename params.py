import configparser
import os.path

from flask import Blueprint

import pgpy
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

routes = Blueprint("routes", __name__)

config = configparser.ConfigParser()
config.read('sierra.ini')

version = "0.1"

def make_key():
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
    uid = pgpy.PGPUID.new(pn=config['SIERRA']['repository_name'], comment=f"Sieloader Repository, {config['SIERRA']['hostname']}",
                          email=config['SIERRA']['email'])
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
if pgpkey.userids[0].name != config['SIERRA']['repository_name'] or pgpkey.userids[0].email != config['SIERRA']['email'] or pgpkey.userids[0].comment != f"Sieloader Repository, {config['SIERRA']['hostname']}":
    make_key()
    pgpkey = pgpy.PGPKey.from_file('key.pgp')[0]

