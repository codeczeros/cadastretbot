from aiogram.types import Message
from aiogram.filters import BaseFilter


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type
        

class SuperGroupFilter(BaseFilter):
    def __init__(self, chat_id):
        self.chat_id = chat_id

    async def __call__(self, message: Message) -> bool:
        return message.chat.id == self.chat_id
    

class ReplyToSelf(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.reply_to_message.from_user.id != message.from_user.id