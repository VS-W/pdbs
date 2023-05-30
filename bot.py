import os, json, asyncio, multiprocessing, socket
import discord

TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('DISCORD_TARGET_CHANNEL_ID'))

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

async def handle_client(reader, writer):
	request = None
	while True:
		request = (await reader.read(1024)).decode('utf8')
		response = str(request)
		writer.write(response.encode('utf8'))
		await writer.drain()
		await send_message(f'Server: {request}')
	writer.close()

async def run_server():
	server = await asyncio.start_server(handle_client, 'localhost', 5999)
	async with server:
		await server.serve_forever()

async def main():
	loop = asyncio.get_event_loop()
	socketserver = loop.create_task(run_server())
	discordbot = loop.create_task(client.start(TOKEN))
	await asyncio.wait([socketserver, discordbot])

asyncio.run(main())
