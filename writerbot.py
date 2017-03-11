import discord
import asyncio

client = discord.Client()
help_message = '**Commands:**\n`.writer help` - displays this information. This can also be used for detailed information about each command: `.writer command`\n`.writer delete messageID1 messageID2` - deletes all messages between messageID1 and messageID2.\n`.writer delay seconds` - forces users to wait a certain number of seconds after each message.\n**Examples:**\nGet information about the delete command: `.writer help delete`\nDelete: `.writer delete 289900281297371136 289900570058162176`\ndelay to 1 minute: `.writer delay 60`'
help_messages = {
    'help' : 'You are using this command right now!',
    'delete' : 'Deletes a batch of commands. Make sure \'Developer Mode\' is enabled in your discord settings. You can then right click on a message and click \'Copy ID\'. Get two IDs and use them in the delete command to delete all messages between the two IDs. For example: `.writer delete 289900281297371136 289900570058162176`.',
    'delay' : 'Sets a delay between messages to stop a user from sending lots of messages at once. To enable this on a channel with a delay of 10 seconds do the following: `.writer delay 10`.'
    }
delay_channels = []
delay_time = {}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for server in client.servers:
        await client.send_message(server.get_channel(server.id), 'WriterBot has been restarted. Remember to reset your delays as they will have been deleted.')

@client.event
async def on_message(message):
    if message.channel.id in delay_channels and message.author != client.user and not message.channel.permissions_for(message.author).administrator:
        await delay(message.author, message.channel)
    elif message.content.startswith('.writer') and message.author.server_permissions.administrator:
        command = message.content[8:]
        if command == 'help':
            await client.send_message(message.channel, help_message)
        elif command.startswith('help'):
            help_command = command[5:]
            if help_command in help_messages:
                await client.send_message(message.channel, help_messages[help_command])
        elif command.startswith('delete'):
            command_delete = command[6:].split()
            try:
                start_message = await client.get_message(message.channel, command_delete[0])
                end_message = await client.get_message(message.channel, command_delete[1])
                await client.delete_message(start_message)
                if command_delete[0] != command_delete[1]:
                    await client.delete_message(end_message)
                await client.purge_from(message.channel, limit = 100, before = end_message, after = start_message)
                await client.delete_message(message)
                message_sent = await client.send_message(message.channel, 'Messages deleted 3')
                await asyncio.sleep(1)
                await client.edit_message(message_sent, new_content = 'Messages deleted 2')
                await asyncio.sleep(1)
                await client.edit_message(message_sent, new_content = 'Messages deleted 1')
                await asyncio.sleep(1)
                await client.delete_message(message_sent)
            except:
                await client.send_message(message.channel, '**You did something wrong! The delete command works like this:**\n' + help_messages['delete'])
        elif command.startswith('delay'):
            try:
                command_delay = command[5:].strip()
                if command_delay == '0':
                    try:
                        delay_channels.remove(message.channel.id)
                        del delay_time[message.channel.id]
                        await client.send_message(message.channel, 'Delay removed')
                    except:
                        await client.send_message(message.channel, 'The delay is already set to 0.')
                elif message.channel.id in delay_channels:
                    delay_time[message.channel.id] = int(command_delay)
                    await client.send_message(message.channel, 'Delay changed')
                else:
                    delay_channels.append(message.channel.id)
                    delay_time[message.channel.id] = int(command_delay)
                    await client.send_message(message.channel, 'Delay set')
            except:
                await client.send_message(message.channel, '**You did something wrong! The delay command works like this:**\n' + help_messages['delay'])
        else:
            await client.send_message(message.channel, '**You did something wrong! The bot usage is as follows:**\n' + help_message)

async def delay(user, channel):
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await client.edit_channel_permissions(channel, user, overwrite)
    await asyncio.sleep(delay_time[channel.id])
    overwrite.send_messages = True
    await client.edit_channel_permissions(channel, user, overwrite)

client.run('Mjg5NDEzNTUxMjc2Mjk0MTQ0.C6VXhQ.LI3Vc816XmR5hbAZPzZ2iaYJZV4')
