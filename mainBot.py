from logging import currentframe
import os
import discord
from discord.ext import commands, tasks
from discord.embeds import Embed
from dotenv import load_dotenv
import datetime
import requests
import json
from pymongo import MongoClient, mongo_client
import pymongo

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
class MongoDatabase:
    @classmethod
    def get_database():
        client = MongoClient(os.getenv("DOTENV.CONNECTION_STRING"))
        return 
        pass

class TableOfAssinments():
    pass

# Start of the Bot

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description="Discord bot for tired students, tired of remembering all the deadlines, assignments and tests.")        
        
@bot.event
async def on_ready():
    print("Bot is online and ready!")
    print(f"BOT NAME: {bot.user.name}")
    print(f"BOT ID: {bot.user.id}")
    print("------------------------------")
    await bot.change_presence(activity=discord.Game(name="!help")) 

# Commands of Discord Bot
@bot.command()

async def addReminder(ctx,subject,what,deadline,whenAlert):
    AssignmentClass.addReminder(subject,what,deadline,whenAlert)
    await ctx.send(f"Reminder Added: {subject} | {what} | {deadline} | {whenAlert}")
    

bot.run(os.getenv("DOTENV.TOKEN"))