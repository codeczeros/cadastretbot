import asyncio

from aiogram.exceptions import TelegramRetryAfter
from aiogram import Dispatcher, Bot

from cfg import BOT_TOKEN, SUPER_GROUP, sectors_to_ids, forum_ids, sectors_list
from handlers import startcmd, sectors, supergroup


dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp.include_routers(
        startcmd.router,
        sectors.router,
        supergroup.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.startup()
async def start(bot: Bot):
    if not forum_ids:
        print("preping Group...")
        i = 0
        while i < len(sectors_list):
            try:
                ForumTopic = await bot.create_forum_topic(SUPER_GROUP, sectors_list[i])
                sectors_to_ids[sectors_list[i]] = ForumTopic.message_thread_id
                await bot.send_message(SUPER_GROUP, "Registered id:  " + str(ForumTopic.message_thread_id), message_thread_id=ForumTopic.message_thread_id)
                i += 1
                await asyncio.sleep(6)
            except TelegramRetryAfter as e:
                print(f"Flood control exceeded, retrying after {e.retry_after} seconds.")
                await asyncio.sleep(e.retry_after)

        await bot.send_message(SUPER_GROUP, str(sectors_to_ids))


    print("Online")


if __name__ == "__main__":
    asyncio.run(main())

