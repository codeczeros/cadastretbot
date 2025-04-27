from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import content
from keyboards import get_readkb, get_seckb

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(content.greeting_msg, reply_markup=ReplyKeyboardRemove())
    await message.answer(content.start_msg, reply_markup=await get_readkb(), parse_mode="Markdown")


@router.callback_query(F.data == "read_rules")
async def read_rules(callback: types.CallbackQuery):
    await callback.message.delete()

    await callback.message.answer(content.done_msg, reply_markup=await get_seckb())
    await callback.answer()


@router.message(F.text == content.cancelkb)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(content.canceled_msg, reply_markup=await get_seckb())
    await state.clear()



@router.message(Command("yordam"))
async def help(message: types.Message):
    await message.answer(content.help_msg, parse_mode="Markdown")
