from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from TelegramBot.config import prefixes, SUDO_USERID, OWNER_USERID
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.database import MongoDb, database 
from TelegramBot.assets.start_constants import *
from pyrogram import filters, Client 
from TelegramBot import bot


START_BUTTON = [
    [
        InlineKeyboardButton("📖 Commands", callback_data="COMMAND_BUTTON"),
        InlineKeyboardButton("👨‍💻 About me", callback_data="ABOUT_BUTTON"),
    ],
    [InlineKeyboardButton("🔭 Original Repo", url=f"https://github.com/sanjit-sinha/Telegram-Bot-Boilerplate")]]


COMMAND_BUTTON = [
    [
        InlineKeyboardButton("Users", callback_data="USER_BUTTON"),
        InlineKeyboardButton("Sudo", callback_data="SUDO_BUTTON"),
    ],
    [InlineKeyboardButton("Developer", callback_data="DEV_BUTTON")],
    [InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")]]


GOBACK_1_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")]]
GOBACK_2_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="COMMAND_BUTTON")]]



commands = ["start", "help"]
@Client.on_message(filters.command(commands, **prefixes))
@ratelimiter
async def start(_, message: Message):
    await database.saveUser(message.from_user)
    return await message.reply_animation(
        animation=START_ANIMATION,
        caption=START_CAPTION,
        reply_markup=InlineKeyboardMarkup(START_BUTTON),
        quote=True)


@Client.on_callback_query(filters.regex("_BUTTON"))
@ratelimiter
async def botCallbacks(client, CallbackQuery):

    clicker_user_id = CallbackQuery.from_user.id
    user_id = CallbackQuery.message.reply_to_message.from_user.id
    
    if clicker_user_id != user_id:
    	return await CallbackQuery.answer ("This command is not initiated by you.")
    
    if CallbackQuery.data == "ABOUT_BUTTON":
        await CallbackQuery.edit_message_text(ABOUT_CAPTION, reply_markup=InlineKeyboardMarkup(GOBACK_1_BUTTON))

    elif CallbackQuery.data == "START_BUTTON":
        await CallbackQuery.edit_message_text(START_CAPTION, reply_markup=InlineKeyboardMarkup(START_BUTTON))

    elif CallbackQuery.data == "COMMAND_BUTTON":
        await CallbackQuery.edit_message_text(COMMAND_CAPTION, reply_markup=InlineKeyboardMarkup(COMMAND_BUTTON))

    elif CallbackQuery.data == "USER_BUTTON":
        await CallbackQuery.edit_message_text(USER_TEXT, reply_markup=InlineKeyboardMarkup(GOBACK_2_BUTTON))

    elif CallbackQuery.data == "SUDO_BUTTON":
        if clicker_user_id not in SUDO_USERID: return await CallbackQuery.answer("You are not in the sudo user list.", show_alert=True)
        else: await CallbackQuery.edit_message_text(SUDO_TEXT, reply_markup=InlineKeyboardMarkup(GOBACK_2_BUTTON) )

    elif CallbackQuery.data == "DEV_BUTTON":
        if clicker_user_id not in OWNER_USERID: return await CallbackQuery.answer( "This is developer restricted command.", show_alert=True)
        else: await CallbackQuery.edit_message_text(DEV_TEXT, reply_markup=InlineKeyboardMarkup(GOBACK_2_BUTTON))

            
            
@Client.on_message(filters.new_chat_members, group=1)
async def newChat(_, message: Message):
    """
    Get notified when someone add bot in the group, then saves that group chat_id
    in the database. 
    """
 
    chatid = message.chat.id 
    for new_user in message.new_chat_members:
    	if new_user.id == bot.me.id:
    		await database.saveChat(chatid)
 
           
