# Simple Discord bot with locally hosted socket implementation
On your server, assuming it's Debian based (e.g. Ubuntu, Raspberry Pi, etc.):

	sudo apt install docker.io docker-compose git
	git clone https://github.com/VS-W/pdbs
	cd pdbs

Replace the values for User ID/Group ID/DISCORD_TOKEN in docker-compose.yml with your own.

Run the following to see your IDs:

	echo User ID: $(id -u)
	echo Group ID: $(id -g)

Get your discord token from [here](https://discordapp.com/developers/applications):

+ Create an application. Go to the "Bot" tab.
+ Click "Add Bot" and copy  the token displayed, that's your "DISCORD_TOKEN" to paste into the docker-compose.yml file.
+ Go to the "OAuth2" tab.
+ Click "URL Generator" and check the box for "bot" in the "Scopes" field.
+ Under the "Bot Permissions" field, check "Read Messages/View Channels" and "Send Messages" - that's all this bot requires.
+ Scroll down and click "copy" on the generated URL, and open the URL in your web browser and authorize it.

Back on your server, run the following in the same directory you cloned the repo to:

	sudo docker-compose up -d

# Usage

Simple messages:

	python3 client.py "Your message here."

Files:
+ Pulls from installed directory, e.g. pdbs/filename.txt.

e.g.:

	python3 client.py file:filename.txt


+ My usage usually follows the pattern of uploading the file to the server via scp and calling the client script via ssh, normally aliased or in a bash script. Renaming the file with a recognized extension will normally allow directly previewing the file in Discord.

e.g.:

	scp logfile user@server:/home/user/docker/pdbs/logfile.txt && \
	ssh user@server python3 /home/user/docker/pdbs/client.py file:logfile.txt
