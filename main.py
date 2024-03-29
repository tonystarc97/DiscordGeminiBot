 
import discord 
import os

from google import generativeai as genai
# file = input("Enter 1, 2, or 3 for loading the chat:\n ")
file = "1"
match(file):
  case "1":
    file = "chat1.txt"
  case "2":
    file = "chat2.txt"
  case "3": 
    file = "chat3.txt"
  case _:
    print("Invalid choice.")
    exit()
    
with open(file, "r") as f:
  chat = f.read() 

GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
genai.configure(api_key=GEMINI_API_KEY)
token = os.getenv("SECRET_KEY")
DISCORD_MAX_MESSAGE_LENGTH = 2000
class MyClient(discord.Client):
    async def send_message_in_chunks(self,ctx,response):
      message = ""
      for chunk in response:
          message += chunk.text
          if len(message) > DISCORD_MAX_MESSAGE_LENGTH:
              extraMessage = message[DISCORD_MAX_MESSAGE_LENGTH:]
              message = message[:DISCORD_MAX_MESSAGE_LENGTH]
              await ctx.send(message)
              message = extraMessage
      if len(message) > 0:
          while len(message) > DISCORD_MAX_MESSAGE_LENGTH:
              extraMessage = message[DISCORD_MAX_MESSAGE_LENGTH:]
              message = message[:DISCORD_MAX_MESSAGE_LENGTH]
              await ctx.send(message)
              message = extraMessage
          await ctx.send(message)
    async def on_ready(self):
        print(f'Logged on as {self.user}!\nbot is online...')

    async def on_message(self, message):
        global chat
        try:
          chat += f"{message.author}: {message.content}\n"
          print(f'Message from {message.author}: {message.content}')
          print(self.user)
          if self.user!= message.author:
              if self.user in message.mentions:
                model = genai.GenerativeModel('gemini-pro')
                
                response = model.generate_content(f"{chat}\Edith97#9114e: ", stream=True)
                response.resolve()
                messageToSend = response.candidates[0].content.parts[0].text
                print(messageToSend)
                channel = message.channel
                await self.send_message_in_chunks(channel,response)   
        except Exception as e:
          print('Error : ', e)
          chat = ""
            
      

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
