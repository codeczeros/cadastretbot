from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from cfg import SUPER_GROUP, sectors_to_ids
from filters import SuperGroupFilter

        
router = Router()
router.message.filter(
    SuperGroupFilter(SUPER_GROUP)
)

@router.message(F.text)
async def reply(message: Message, bot: Bot):
    if not (message.reply_to_message or message.reply_to_message.text):
        return 
    
    atr = message.reply_to_message.text.split("_")
    
    if not (atr and atr[0] == ">"):
        return
    
    try:
        await bot.send_message(
            atr[1],
            f"{message.text}\n\n{get_sectid(message.message_thread_id)}",
            reply_to_message_id=atr[2]
        )
        # await message.copy_to(atr[0], reply_to_message_id=atr[1], caption="___herer___")
    except TelegramForbiddenError as e:
        await message.reply("Yuborilmadi, bot foydalanuvchi tomonidan blocklangan.")
    except Exception as e:
        print("Error in supergroup.py:34 :", e)
        pass


# @router.message(F.animation)
# async def replymedia(message: Message, bot: Bot):
#     print("animation?")


# @router.message(F.photo)
# async def replymedia(message: Message, bot: Bot):
#     print("photo?")


# @router.message(F.document)
# async def replymedia(message: Message, bot: Bot):
#     print("document?")


def get_sectid(id):
    for k, v in sectors_to_ids.items():
        if v == id:
            return k