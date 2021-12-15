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


# Setting Classes and functions for Discord Bot
            
            
class AssignmentClass:
    def __init__(self,subjectToDo,whatToDo,deadLine,whenAlert):
        self.subjectToDo = subjectToDo
        self.whatToDo = whatToDo
        self.deadLine = deadLine
        self.whenAlert = whenAlert #subtract 2 hours by default
        
    async def addReminder(self):
        try:
            assignmentRemider = {
                'subjectToDo': self.subjectToDo,
                'whatToDo': self.whatToDo,
                'deadline' : self.deadLine,
                'whenAlert': self.whenAlert
            }
            print(assignmentRemider)
            StudentReminders = get_database()
            StudentReminders.insert_one(assignmentRemider)
            print("Added to DB")
        except Exception:
            Exception("Adding to DB failed")
            
            
#function for conecting to db       
def get_database():
    try:
        client = MongoClient(os.getenv("DOTENV.CONNECTION_STRING"))
        db = client["DiscordBotForTiredStudentsDatabase"]
        StudentReminders = db["StudentReminders"]
        print('Connected to DB')
        return StudentReminders
    except Exception:
        Exception('Failed to connect to DB')        


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
@bot.command(name='addReminder', help="use !addReminder [Subject] [what to do] [time to do it] [when you want to be alerted about it], please use date format [dd.mm.yyyy:HH:MM] for when and alert")
async def DCaddReminder(ctx,subjectToDo,whatToDo,deadLine,whenAlert,):
    Assignment = AssignmentClass(subjectToDo,whatToDo,deadLine,whenAlert)
    await Assignment.addReminder()
    await ctx.send(f"Reminder Added: {subjectToDo} | {whatToDo} | {deadLine} | {whenAlert}")

bot.run(os.getenv("DOTENV.TOKEN"))