import os
import re
import sys
import json
import time
import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta
from aiohttp import ClientSession
from bot import Bot
from helper_func import subscribed, encode, decode, get_messages
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message



GROUPS = {
    "MASTER PRO 1 HINDI": -1002100102965,  # Replace with your actual group IDs
    "Group 2": -1001814803421,  # Replace with your actual group IDs
    "Group 3": -1009876543210   # Replace with your actual group IDs
}


@Bot.on_message(filters.command('join') & filters.private, group=89897)
async def join_command(bot: Bot, message: Message):
    # Create inline buttons for each group, ensuring callback_data is a string
    buttons = [
        [InlineKeyboardButton(group_name, callback_data=str(group_id))] for group_name, group_id in GROUPS.items()
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await message.reply_text(
        "Choose a group to join:",
        reply_markup=reply_markup
    )

