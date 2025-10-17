import ast
import base64
import json
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse, PlainTextResponse

from annotations import repo_info, addon_info
from params import *

app = FastAPI(
    title=repository_name,
    description="Sieloader repository",
    version=version,
    summary="Welcome to sieloader repository API",
    contact={
        "name": repository_name,
        "email": email
    }, docs_url="/"
)

@app.get(
    path="/repo/info",
    summary="Getting information about repository",
    responses={200: {'model': repo_info}}
)
def info():
    return repo_info(
        name=repository_name,
        version=version,
        email=email,
        repositories=len(next(os.walk("data"))[1])
    )

@app.get(
    path="/repo/metadata",
    summary="Getting repository metadata, for sure information about every addon which this repository service host"
)
def metadata():
    dirs = next(os.walk("data"))[1]
    data = {}
    for i in dirs:
        with open(f"data/{i}/metadata.json") as file:
            meta = json.load(file)
            if secure:
                source = f"https://{config['SIERRA']['hostname']}/repo/{i}"
            else:
                source = f"http://{config['SIERRA']['hostname']}/repo/{i}"
            size = len(base64.b64encode(bytes(pgpy.PGPMessage.new(f"data/{i}/data.tar.xz", file=True))))
            meta = addon_info(
                author=meta['author'],
                description=meta['description'],
                email=meta['email'],
                source=source,
                size=size,
                version=meta['version']
            )
            data[i] = json.loads(meta.model_dump_json())
    return JSONResponse(content=data)

@app.get(
    path="/repo/public_key",
    summary="Repository public key for verifying signed addons"
)
def public_key():
    return PlainTextResponse(base64.b64encode(bytes(pgpkey.pubkey)))

@app.get(
    path="/repo/{repo}",
    summary="For downloading addon from repository"
)
def repo_download(repo):
    return PlainTextResponse(base64.b64encode(bytes(pgpy.PGPMessage.new(f"data/{repo}/data.tar.xz", file=True))))

@app.get(
    path="/repo/{repo}/signature",
    summary="For getting addon signature from repository"
)
def repo_cert(repo):
    file = pgpy.PGPMessage.new(f"data/{repo}/data.tar.xz", file=True)
    signature = pgpkey.sign(file)
    return PlainTextResponse(base64.b64encode(bytes(signature)))
