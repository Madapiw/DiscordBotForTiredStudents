from logging import currentframe, exception
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

def parseDate(date): #simple, not elegant but works
    split_day_month = date.split(".")
    day = split_day_month[0]
    month = split_day_month[1]
    split_year_and_time = split_day_month[2].split("-")
    year = split_year_and_time[0]
    split_time = split_year_and_time[1].split(":")
    hours = split_time[0]
    minutes = split_time[1]
    return int(day),int(month),int(year),int(hours),int(minutes)
    
# Start of the Bot

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description="Discord bot for tired students, tired of remembering all the deadlines, assignments and tests.")        
        
@bot.event
async def on_ready():
    print("Bot is online and ready!")
    print(f"BOT NAME: {bot.user.name}")
    print(f"BOT ID: {bot.user.id}")
    print("------------------------------")
    await bot.change_presence(activity=discord.Game(name="Gabrys patrzy")) 

# Commands of Discord Bot
@bot.command(name='addReminder', help="use !addReminder [Subject] [what to do] [time to do it] [when you want to be alerted about it], please use date format [dd.mm.yyyy:HH:MM] for when and alert")
async def DCaddReminder(ctx,subjectToDo,whatToDo,deadLine,whenAlert,):
    try:
        DL_day,DL_month,DL_year,DL_hours,DL_minutes = parseDate(deadLine)
        WA_day,WA_month,WA_year,WA_hours,WA_minutes = parseDate(whenAlert)
        if (DL_hours <= 24) and (DL_minutes <= 60) and (WA_hours <= 24) and (WA_minutes <= 60):
            if (DL_day >= WA_day) and (DL_month >= WA_month) and (DL_year == WA_year) and (DL_hours >= WA_hours):
                Assignment = AssignmentClass(subjectToDo,whatToDo,deadLine,whenAlert)
                await Assignment.addReminder()
                await ctx.send(f"Reminder Added: {subjectToDo} | {whatToDo} | {deadLine} | {whenAlert}")
                embedMsg = discord.Embed(title="Assigment TODO !", description="Gabryś będzie smutny, jak sie nie nauczycie")
                embedMsg.set_author(name="Gabriel", url="https://usosweb.usos.pw.edu.pl/kontroler.php?_action=news/default", icon_url="gabrys.png")
                embedMsg.add_field(name="Z jakiego przedmiotu", value=subjectToDo, inline=False)
                embedMsg.add_field(name="Co do roboty", value=whatToDo, inline=False)
                embedMsg.add_field(name="Na kiedy", value=deadLine, inline=True)
                embedMsg.add_field(name="Alert na", value=whenAlert, inline=True)
                await ctx.send(embed=embedMsg)
            else:
                await ctx.send("Wrong format of Dates")
                assert Exception("Wrong format of Dates")     
        else:
            await ctx.send("Incorrect time")
            assert Exception("Incorrect time")       
            
    except Exception:
        Exception("Something went wrong")
        

@tasks.loop(hours=24)
async def AssignemntsAlert():
    pass
    
@AssignemntsAlert.before_loop
async def before():
    await bot.wait_until_ready()

bot.run(os.getenv("DOTENV.TOKEN"))