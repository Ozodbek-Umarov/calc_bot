from aiogram import  Dispatcher, Bot, Router
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from asyncio import run
from config import API
from background import keep_alive
class Main:

    def __init__(self, token = API) -> None:
        self.dp = Dispatcher()
        self.bt = Bot(token=API)
        self.buttons = ["7","8","9","/",
                        "6","5","4","*",
                        "3","2","1","+",
                        "0",".","=","-"]
    def get_keyboard(self):
        kb = InlineKeyboardBuilder()
        for t in self.buttons:
            kb.add(InlineKeyboardButton(text=t, callback_data="op:"+t))
        kb.adjust(4,4,4,4)
        return kb.as_markup(resize_keyboard=True)
    
    async def start_message(self, msg:Message):
        await msg.answer(text="|",reply_markup=self.get_keyboard())

    async def callback_oper(self, clb:CallbackQuery):
        sym = clb.data.split(":")[1]
        txt = clb.message.text
        if sym == "=":
            try:
                txt = str(eval(txt))
            except:
                txt = "|"
        elif txt != "|":
            txt += sym
        else:
            txt = sym
        await clb.message.edit_text(text=txt,reply_markup=self.get_keyboard())
        await clb.answer(text=f"Add new number {txt}")
    def register(self):
        self.dp.message.register(self.start_message,Command("start"))
        self.dp.callback_query.register(self.callback_oper, F.data.startswith("op:"))

    async def start(self):
        self.register()
        try:
            await self.dp.start_polling(self.bt)
        except:
            await self.bt.session.close()

keep_alive()
if __name__ == "__main__":
    mn = Main()
    run(mn.start())