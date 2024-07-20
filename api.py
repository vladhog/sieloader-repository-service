import ast
import base64
import json
import os

from flask import jsonify

from params import *


@routes.route("/repo/info")
def info():
    data = {"name": config['SIERRA']['repository_name'],
            "version": version,
            "email": config['SIERRA']['email'],
            "repositories": len(next(os.walk("data"))[1])}
    return jsonify(data), 200

@routes.route("/repo/metadata")
def metadata():
    dirs = next(os.walk("data"))[1]
    data = {}
    for i in dirs:
        with open(f"data/{i}/metadata.json") as file:
            meta = json.load(file)
            if ast.literal_eval(config['SIERRA']['secure']):
                meta.update({"source": f"https://{config['SIERRA']['hostname']}/repo/{i}"})
            else:
                meta.update({"source": f"http://{config['SIERRA']['hostname']}/repo/{i}"})
            meta.update({"size": len(base64.b64encode(bytes(pgpy.PGPMessage.new(f"data/{i}/data.tar.xz", file=True))))})
            data[i] = meta
    return jsonify(data), 200

@routes.route("/repo/public_key")
def public_key():
    return base64.b64encode(bytes(pgpkey.pubkey))

@routes.route("/repo/<repo>")
def repo_download(repo):
    return base64.b64encode(bytes(pgpy.PGPMessage.new(f"data/{repo}/data.tar.xz", file=True)))

@routes.route("/repo/<repo>/signature")
def repo_cert(repo):
    file = pgpy.PGPMessage.new(f"data/{repo}/data.tar.xz", file=True)
    signature = pgpkey.sign(file)
    return base64.b64encode(bytes(signature))
