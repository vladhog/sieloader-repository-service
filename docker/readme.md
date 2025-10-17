# Building the docker image

First of all, before running docker image we recommend running server outside of docker for once to generate pgp key for signing addons.
Make sure to set your values to sierra.ini or change them with environment variable and run the server.

After you ran server for once and get key.pgp, you can build image with provided dockerfile
