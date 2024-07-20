# Sieloader Repository Service
Sieloader (SIERRA tool addons loader) Repository Service made for simple share of addons used with sieloader tool and sierepo command line tool.

# Settings up server
All settings of Sieloader Repository Service stored in sierra.ini file, there you can find:
- repository name
- repository contact email 
- repository hostname, should be external hostname/ip via which people will be able to communicate with service
- secure option, made for servers who using HTTPS connection, switch it to True if using HTTPS and leave it False if HTTP

# Endpoints
All endpoints stored in api.py file, here i will tell about some of them:
- /repo/info (json)
	- Endpoint made for getting information about repository, such as repository name, version, contact email and amount of addons hosted by service.
	
- /repo/metadata (json)
	- Providing metadata about all addons stored, such as addon name, author, author contact email, description, size of addon, source url for downloading addon and addon version.

- /repo/public_key (base64 bytes)
	- For safety reasons, we using PGP keys system for verifying that you talking to right server, with this endpoint you can get server's public key.
	
- /repo/"repo name"	(base64 bytes)
	- Download url for addons, for example /repo/invoker-starter-pack will download invoker-starter-pack
	
- /repo/"repo name"/signature (base64 bytes)
	- With this endpoint you can get addon's signature, signed by server. Its made for making sure that you getting right information and that no one modified it while transfer.

# Official servers
https://sierra.vladhog.ru/ - Vladhog Security SIERRA Repository

# License
Sieloader Repository Service © 2024 by Vladhog Security is licensed under Attribution-NonCommercial-ShareAlike 4.0 International.