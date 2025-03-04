from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus
from TelegramBot.config import SUDO_USERID, OWNER_USERID 


async def isAdmin(message: Message) -> bool:
    """
    Return True if the message is from owner or admin of the group or sudo of the bot.
    """

    if not message.from_user:
        return False
    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return False

    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id
    check_status = await client.get_chat_member(chat_id, user_id)

    if user_id in SUDO_USERID:
        return True
    elif check_status.status in [
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR]:
        return True
    else: return False


def get_readable_time(seconds: int) -> str:
    """
    Return a human-readable time format seconds.
    """

    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)

    if days != 0:
        result += f"{days}d "
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)

    if hours != 0:
        result += f"{hours}h "
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)

    if minutes != 0:
        result += f"{minutes}m "

    seconds = int(seconds)
    result += f"{seconds}s "
    return result
    
    
def get_readable_bytes(size: str) -> str:
	"""
	Return a human readable file size from bytes.
	"""
	
	dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
	
	if not size: return ""
	power = 2**10
	raised_to_pow = 0
	
	while size > power:
	    size /= power
	    raised_to_pow += 1
	    
	return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"
