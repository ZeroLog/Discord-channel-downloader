import discord
import asyncio
import os

TOKEN = '' #Токен бота
CHANNEL_ID =  #id канала

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Бот подключен как {client.user}')
    channel = client.get_channel(CHANNEL_ID)

    channel_name = channel.name if channel.name else str(CHANNEL_ID)
    folder_name = f'chat_{channel_name}'
    os.makedirs(folder_name, exist_ok=True)

    attachments_folder = os.path.join(folder_name, 'downloaded_files')
    os.makedirs(attachments_folder, exist_ok=True)

    file_counter = 1  

    html_content = f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>История чата {channel_name}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .chat-container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .message {{
                margin-bottom: 20px;
            }}
            .message p {{
                margin: 5px 0;
                white-space: pre-wrap;
            }}
            .timestamp {{
                font-size: 0.8em;
                color: #888;
            }}
            .username {{
                font-weight: bold;
            }}
            .file-link {{
                color: #007BFF;
                text-decoration: none;
                font-size: 0.9em;
            }}
            .file-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
    <div class="chat-container">
    <h1>История чата: {channel_name}</h1>
    '''

    async for message in channel.history(limit=None): 
        timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')  
        content = message.content.replace('\n', '<br>')  

        html_content += f'''
        <div class="message">
            <div class="timestamp">{timestamp}</div>
            <p class="username">{message.author.name}:</p>
            <p>{content}</p>
        </div>
        '''

        for attachment in message.attachments:
            file_name = attachment.filename
            base_name, ext = os.path.splitext(file_name)
            unique_file_name = f"{file_counter}{ext}"  
            file_path = os.path.join(attachments_folder, unique_file_name) 

            await attachment.save(file_path) 

   
            html_content += f'''
            <div class="message">
                <div class="timestamp">{timestamp}</div>
                <p class="username">{message.author.name}:</p>
                <p>ФАЙЛ {file_counter}: <a href="downloaded_files/{unique_file_name}" class="file-link">{unique_file_name}</a></p>
            </div>
            '''

            file_counter += 1 

        await asyncio.sleep(0.05) 


    html_content += '''
    </div>
    </body>
    </html>
    '''
    
    html_file_path = os.path.join(folder_name, 'chat_history.html')
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Сообщения и вложения сохранены в папку {folder_name}.")
    await client.close()

client.run(TOKEN)
