from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from cfg import sectors_list
import content

async def get_readkb() -> InlineKeyboardMarkup:
    readkb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=content.readykb, callback_data="read_rules")]
    ])
    return readkb

async def get_seckb() -> ReplyKeyboardMarkup:
    distrkb = ReplyKeyboardBuilder()
    for _ in sectors_list:
        distrkb.add(KeyboardButton(text=_))
    return distrkb.adjust(2).as_markup(input_field_placeholder=content.chooseseckb, is_persistent=True)


async def get_cancelkb() -> ReplyKeyboardMarkup:
    cancelkb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=content.cancelkb)]
    ], resize_keyboard=True)
    return cancelkb