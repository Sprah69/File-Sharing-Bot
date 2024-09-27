import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta
from pyrogram import Client, filters
from datetime import datetime, timedelta
import time
import threading
from bot import Bot
import bot

LOG_ID = '-1001963424186'  
MESSAGE_ID = '55'# Use '@channe

exam_date = datetime(2025, 5, 4)  # May 4, 2025

# Function to send remaining time for the exam
async def send_remaining_time(message: Message):  # Accept the message as a parameter
    now = datetime.now()
    time_left = exam_date - now
    if time_left.days >= 0:  # Only send if the exam is today or in the future
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Beautified message using a single f-string with triple quotes
        lexica = f"""
📅 **Exam Countdown Reminder**

⏳ Time Remaining For NEET 25:
🗓️ **Date:** {exam_date.strftime('%Y-%m-%d')}
📆 **Time Left:** {time_left.days} days, {hours} hours, and {minutes} minutes

Stay focused and keep up the good work! 💪✨
        """
        
        # Send the countdown message to the user who initiated the command
        await message.reply_text(text=lexica)
         await golu.copy(chat_id=LOG_ID) # The actual message content


# Function to handle the countdown
async def countdown_task(message: Message):  # Accept the message as a parameter
    while True:
        await send_remaining_time(message)  # Send the countdown message to the user
        await asyncio.sleep(20)  #  # Wait for 15 minutes (900 seconds)

# Command to start the countdown
@Bot.on_message(filters.command("countdown") , group =8348)
async def start_command(client: Bot, message: Message):
    await message.reply_text("Countdown initiated! I will send the remaining time until the exam every 15 minutes.")
    await send_remaining_time(message)  # Send the remaining time immediately
    # Start the countdown task
    asyncio.create_task(countdown_task(message))  # Create a new task for the countdown


