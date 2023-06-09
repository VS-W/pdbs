import os, json, asyncio, multiprocessing, socket
from pathlib import Path
import discord

TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('DISCORD_TARGET_CHANNEL_ID'))
SERVER_HOST = '0.0.0.0'
SERVER_PORT = int(os.getenv('SERVER_PORT'))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} is connected to the following guilds:')
	for guild in client.guilds:
		print(f'\t{guild.name} (id: {guild.id})')

@client.event
async def on_message(message):
	try:
		if message.author == client.user:
			return

		if '!test' in message.content:
			resp_str = f'Test response'
			resp = await message.channel.send(resp_str)
	except Exception as e:
		print(e)
		pass

async def send_message(message):
	channel = client.get_channel(TARGET_CHANNEL_ID)
	await channel.send(message)

async def send_file(file):
	channel = client.get_channel(TARGET_CHANNEL_ID)
	await channel.send(file=discord.File(file))

async def handle_client(reader, writer):
	request = None
	request = (await reader.read(1024)).decode('utf8')
	request = str(request)
	if len(request.strip()) > 0:
		print(request)
		with open("requests.log", "a") as f:
			f.write(f'{request}\n')
		await send_message(f'> {request}')
		if "file:" in request[:5]:
			file = request[5:].strip()
			print(f'Sending contents of file: {file}')
			await send_file(file)

async def run_server():
	server = await asyncio.start_server(handle_client, SERVER_HOST, SERVER_PORT)
	async with server:
		await server.serve_forever()

async def main():
	loop = asyncio.get_event_loop()
	socketserver = loop.create_task(run_server())
	discordbot = loop.create_task(client.start(TOKEN))
	await asyncio.wait([socketserver, discordbot])

print(f'INIT:\n\tCHANNEL_ID: {TARGET_CHANNEL_ID}\n\tSERVER_PORT: {SERVER_PORT}')
asyncio.run(main())
