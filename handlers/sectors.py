import content

from aiogram import Router, F, Bot
from aiogram.types import Message

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from cfg import SUPER_GROUP, sectors_to_ids, sectors_list
from keyboards import get_cancelkb, get_seckb
from filters import ChatTypeFilter, ReplyToSelf

        
router = Router()
router.message.filter(
    ChatTypeFilter(chat_type='private')
)


class Writeto(StatesGroup):
    writing = State()


@router.message(F.text.in_(sectors_list))
async def writeto(message: Message, state: FSMContext):
    await message.answer(content.write_msg, reply_markup=await get_cancelkb())
    await state.update_data(writing=message.text)
    await state.set_state(Writeto.writing)


@router.message(Writeto.writing)
async def writing(message: Message, state: FSMContext, bot: Bot):
    sector = await state.get_value("writing")
    forwarded = await message.forward(SUPER_GROUP, sectors_to_ids[sector])

    await bot.send_message(
        SUPER_GROUP, 
        f">_{message.from_user.id}_{message.message_id}",
        message_thread_id=sectors_to_ids[sector], 
        reply_to_message_id=forwarded.message_id
    )

    await message.answer(content.sent_msg, reply_markup=await get_seckb())
    await state.clear()


@router.message(F.reply_to_message, ReplyToSelf())
async def sendfromuser(message: Message, bot: Bot):
    sector = message.reply_to_message.text.split()[-1]
    if not (sector in sectors_list):
        await warnuser(message)
        return
    
    forwarded = await message.forward(SUPER_GROUP, sectors_to_ids[sector])

    await bot.send_message(
        SUPER_GROUP, 
        f">_{message.from_user.id}_{message.message_id}",
        message_thread_id=sectors_to_ids[sector], 
        reply_to_message_id=forwarded.message_id
    )
    await message.answer(content.replied_msg, reply_markup=await get_seckb())


@router.message()
async def warnuser(message: Message):
    await message.reply(content.error_msg)
