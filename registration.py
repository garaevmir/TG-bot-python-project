from aiogram import Router, types, F, filters, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods.send_message import SendMessage
from aiogram.fsm.context import FSMContext
from db_control import adduser, adduserinfo, getdate, getsign, getusers
from parser_horoscope import request_ru_today_horoscope, request_ru_tomorrow_horoscope


router = Router()

months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

def main_keyboard():
    kb = [
        [types.KeyboardButton(text="Гороскоп на сегодня"),
        types.KeyboardButton(text="Гороскоп на завтра")],
        [types.KeyboardButton(text="Натальная карта")],
        [types.KeyboardButton(text="Проверить совместимость")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def months_keyboard():
    buttons = []
    for row in range(0, 3):
        rw = []
        for i in range(0, 4):
            rw.append(types.InlineKeyboardButton(text=months[row*4+i], callback_data= ("month_" + months[row*4+i])))
        buttons.append(rw)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def days_keyboard():
    buttons = []
    for row in range(0, 4):
        rw = []
        for day in range(1, 9):
            rw.append(types.InlineKeyboardButton(text=str(row*8+day), callback_data="day_" + str(row*8+day)))
        buttons.append(rw)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


class Registration(StatesGroup):
    filling_first_name = State()
    filling_last_name = State()
    filling_birthday_year = State()
    filling_birthday_date = State()

@router.message(filters.Command('start'))
async def start(message: types.Message, state: FSMContext):
    adduser(str(message.from_user.id), 'users.db', 'bot_users')
    adduserinfo(str(message.from_user.id), str(message.from_user.username), 'username', 'users.db', 'bot_users')
    await message.answer("Введите имя")
    await state.set_state(Registration.filling_first_name)

@router.message(Registration.filling_first_name)
async def first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    #profile["first_name"] = first_name
    adduserinfo(str(message.from_user.id), first_name, 'first_name', 'users.db', 'bot_users')
    await message.answer("Введите год рождения")
    await state.set_state(Registration.filling_birthday_year)

@router.message(Registration.filling_last_name)
async def first_name(message: types.Message, state: FSMContext):
    try:
        last_name = message.text
        #profile["first_name"] = first_name
        adduserinfo(str(message.from_user.id), last_name, 'last_name', 'users.db', 'bot_users')
        await message.answer("Введите год рождения")
        await state.set_state(Registration.filling_birthday_year)
    except:
        None

@router.message(Registration.filling_birthday_year)
async def year(message: types.Message, state: FSMContext):
    year = message.text
    #profile["first_name"] = first_name
    adduserinfo(str(message.from_user.id), year, 'birth_year', 'users.db', 'bot_users')
    await message.answer("Теперь выберите месяц", reply_markup=months_keyboard())
    await state.set_state(Registration.filling_birthday_date)

@router.callback_query(F.data.startswith("month_"))
async def month(callback: types.CallbackQuery):
    month = callback.data[6:]
    adduserinfo(str(callback.from_user.id), month, 'birth_month', 'users.db', 'bot_users')
    await callback.message.edit_text("Теперь выберите день", reply_markup=days_keyboard())



@router.callback_query(F.data.startswith("day_"))
async def day(callback: types.CallbackQuery, state: FSMContext):
    day = callback.data[4:]
    adduserinfo(str(callback.from_user.id), day, 'birth_day', 'users.db', 'bot_users')
    adduserinfo(str(callback.from_user.id), str(1), 'finished_reg', 'users.db', 'bot_users')
    date = getdate(str(callback.from_user.id), 'users.db', 'bot_users')
    adduserinfo(str(callback.from_user.id), star_sign(date[0], date[1]), 'sign', 'users.db', 'bot_users')
    keyboard = main_keyboard()
    await callback.message.edit_text(text="Спасибо за регистрацию")
    await callback.message.answer(text="Теперь вы можете посмотреть гороскоп для своего знака зодиака, смотреть свою натальную карту, а также проверять совместимость", reply_markup=main_keyboard())

    await state.clear()

    

    
@router.message(F.text == "Гороскоп на сегодня")
async def hor_today(message: types.Message):
    await message.answer(request_ru_today_horoscope(getsign(message.from_user.id, 'users.db', 'bot_users')))

@router.message(F.text == "Гороскоп на завтра")
async def hor_tomorrow(message: types.Message):
    await message.answer(request_ru_tomorrow_horoscope(getsign(message.from_user.id, 'users.db', 'bot_users')))

@router.message(F.text == "Натальная карта")
async def nat_map(message: types.Message):
    await message.answer("Натальная карта")

@router.message(F.text == "Проверить совместимость")
async def compat(message: types.Message):
    await message.answer("Совместимость")


def star_sign(day, month):  
    if month == 'Декабрь':  
        sun_sign = 'sagittarius' if (day < 22) else 'capricorn'  
    elif month == 'Январь':  
        sun_sign = 'capricorn' if (day < 20) else 'aquarius'  
    elif month == 'Февраль':  
        sun_sign = 'aquarius' if (day < 19) else 'pisces'  
    elif month == 'Март':  
        sun_sign = 'pisces' if (day < 21) else 'aries'  
    elif month == 'Апрель':  
        sun_sign = 'aries' if (day < 20) else 'taurus'  
    elif month == 'Май':  
        sun_sign = 'taurus' if (day < 21) else 'gemini'  
    elif month == 'Июнь':  
        sun_sign = 'gemini' if (day < 21) else 'cancer'  
    elif month == 'Июль':  
        sun_sign = 'cancer' if (day < 23) else 'leo'  
    elif month == 'Август':  
        sun_sign = 'leo' if (day < 23) else 'virgo'  
    elif month == 'Сентябрь':  
        sun_sign = 'virgo' if (day < 23) else 'libra'  
    elif month == 'Октябрь':  
        sun_sign = 'libra' if (day < 23) else 'scorpio'  
    elif month == 'Ноябрь':  
        sun_sign = 'scorpio' if (day < 22) else 'sagittarius'  
    return sun_sign  


async def daily_horoscope(bot : Bot):
    users = getusers("users.db", 'bot_users')
    for id in users:
        await bot.send_message(chat_id=id[0], text="Ваш гороскоп на сегодня:")
        await bot.send_message(chat_id=id[0], text=request_ru_today_horoscope(getsign(id[0], 'users.db', 'bot_users')))