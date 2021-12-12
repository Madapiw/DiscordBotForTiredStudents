from logging import currentframe
import os
import discord
from discord.ext import commands, tasks
from discord.embeds import Embed
from dotenv import load_dotenv
import datetime
import requests
import json

load_dotenv()


global currentAssignments # future with mongo database cuz quick and lightweight

# Setting Classes for Discord Bot

class AssignmentClass:
    def __init__(self,subjectToDo,whatToDo,deadLine,*args, **kwargs):
        self.subjectToDo = subjectToDo
        self.whatToDo = whatToDo
        self.deadLine = deadLine
        self.whenAlert = kwargs.get('whenAlert', deadLine) #subtract 2 hours by default
        
    @classmethod 
    def addReminder(self):
        assignmentRmider = json.dumps({
            'Subject': self.subjectToDo,
            'WhatToDo': self.whatToDo,
            'Deadline': self.deadLine,
            'WhenAlert':self.whenAlert
        })
        pass


class TableOfAssinments():
    pass
# Commands of Discord Bot



# Start of the Bot

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description="Discord bot for tired students, tired of remembering all the deadlines, assignments and tests.")        
        
@bot.event
async def on_ready():
    print("Bot is online and ready!")
    print(f"BOT NAME: {bot.user.name}")
    print(f"BOT ID: {bot.user.id}")
    print("------------------------------")
    await bot.change_presence(activity=discord.Game(name="!help")) 
    
bot.run(os.getenv("DOTENV.TOKEN"))