from aiogram import Router, types, F, filters, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods.send_message import SendMessage
from aiogram.fsm.context import FSMContext
from db_control import adduser, adduserinfo, getdate, getsign, getusers, getuser
from parser_horoscope import request_ru_today_horoscope, request_ru_tomorrow_horoscope


router = Router()

months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

def main_keyboard():
    kb = [
        [types.KeyboardButton(text="Гороскоп на сегодня"),
        types.KeyboardButton(text="Гороскоп на завтра")],
        [types.KeyboardButton(text="Натальная карта")],
        [types.KeyboardButton(text="Проверить совместимость")],
        [types.KeyboardButton(text="Изменить данные")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

def reg_keyboard():
    kb = [
        [types.KeyboardButton(text="Изменить дату рождения")],
        [types.KeyboardButton(text="Изменить время рождения")],
        [types.KeyboardButton(text="Изменить имя")],
        [types.KeyboardButton(text="Изменить пол")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

def y_n_keyboard_gend():
    kb = [
        [types.InlineKeyboardButton(text="Да", callback_data="gen_yes")],
        [types.InlineKeyboardButton(text="Нет", callback_data="gen_no")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def months_keyboard():
    buttons = []
    for row in range(0, 3):
        rw = []
        for i in range(0, 4):
            rw.append(types.InlineKeyboardButton(text=months[row*4+i], callback_data= ("month_" + str(row*4+i + 1))))
        buttons.append(rw)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def months_keyboard_re():
    buttons = []
    for row in range(0, 3):
        rw = []
        for i in range(0, 4):
            rw.append(types.InlineKeyboardButton(text=months[row*4+i], callback_data= ("remonth_" + str(row*4+i + 1))))
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

def days_keyboard_re():
    buttons = []
    for row in range(0, 4):
        rw = []
        for day in range(1, 9):
            rw.append(types.InlineKeyboardButton(text=str(row*8+day), callback_data="reday_" + str(row*8+day)))
        buttons.append(rw)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def gender_keyboard():
    kb = [
        [types.KeyboardButton(text="Мужской")],
        [types.KeyboardButton(text="Женский")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


class Registration(StatesGroup):
    filling_first_name = State()
    filling_gender = State()
    filling_birthday_year = State()
    filling_birthday_date = State()
    refilling_first_name = State()
    refilling_gender = State()
    refilling_birthday_year = State()
    refilling_birthday_date = State()

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
    await message.answer("Выберите свой пол", reply_markup=gender_keyboard())
    await state.set_state(Registration.filling_gender)

@router.message(Registration.filling_gender)
async def first_name(message: types.Message, state: FSMContext):
    try:
        gender = message.text
        if gender != "Мужской" and gender != "Женский":
            await message.answer("К сожалению я не могу обработать ваш пол, так что выберите что-то из предложенных вариантов")
            return
        #profile["first_name"] = first_name
        if gender == "Мужской":
            gender = "male"
        else:
            gender = "female"
        adduserinfo(str(message.from_user.id), gender, 'gender', 'users.db', 'bot_users')
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

    
@router.message(F.text == "Изменить данные")
async def hor_today(message: types.Message):
    await message.answer(text="Выберите, что вы хотите изменить", reply_markup=reg_keyboard())
    
@router.message(F.text == "Гороскоп на сегодня")
async def hor_today(message: types.Message):
    await message.answer(request_ru_today_horoscope(getsign(message.from_user.id, 'users.db', 'bot_users')))

@router.message(F.text == "Гороскоп на завтра")
async def hor_tomorrow(message: types.Message):
    await message.answer(request_ru_tomorrow_horoscope(getsign(message.from_user.id, 'users.db', 'bot_users')))

@router.message(F.text == "Натальная карта")
async def nat_map(message: types.Message):
    user_data = getuser(message.from_user.id, "users.db", "bot_users")
    fin_reg = user_data[6]
    if fin_reg == 0:
        await SendMessage(chat_id=message.from_user.id, text="Кажется вы не завершили регистрацию, нажмите на кнопку 'Изменить данные' и добавьте недостающую информацию", reply_markup=main_keyboard())
        return
    await message.answer("Натальная карта")

@router.message(F.text == "Проверить совместимость")
async def compat(message: types.Message):
    await message.answer("Совместимость")

@router.message(F.text == "Изменить имя")
async def re_reg_name(message: types.Message, state: FSMContext):
    user_data = getuser(message.from_user.id, "users.db", "bot_users")
    await message.answer("В данный момент у вас указано имя {}. Введите новое имя".format(user_data[2]))
    await state.set_state(Registration.refilling_first_name)

@router.message(Registration.refilling_first_name)
async def f_name(message: types.Message, state: FSMContext):
    first_name = message.text
    #profile["first_name"] = first_name
    adduserinfo(str(message.from_user.id), first_name, 'first_name', 'users.db', 'bot_users')
    await message.answer("Имя успешно изменено", reply_markup=main_keyboard())
    await state.clear()

@router.message(F.text == "Изменить дату рождения")
async def re_reg_date(message: types.Message, state: FSMContext):
    user_data = getuser(message.from_user.id, "users.db", "bot_users")
    await message.answer("В данный момент у вас указана дата {}/{}/{}. Введите новый год рождения".format(user_data[3], user_data[4], user_data[5]))
    await state.set_state(Registration.refilling_birthday_date)

@router.message(F.text == "Изменить пол")
async def re_reg_date(message: types.Message, state: FSMContext):
    user_data = getuser(message.from_user.id, "users.db", "bot_users")
    await message.answer("В данный момент у вас указан {} пол. Выберите ваш пол".format("мужской" if user_data[10] == "male" else "женский"), reply_markup=gender_keyboard())
    await state.set_state(Registration.refilling_gender)

@router.message(Registration.refilling_birthday_date)
async def f_name(message: types.Message, state: FSMContext):
    first_name = message.text
    #profile["first_name"] = first_name
    adduserinfo(str(message.from_user.id), first_name, 'birth_year', 'users.db', 'bot_users')
    await message.answer("Теперь выберите месяц", reply_markup=months_keyboard_re())

@router.callback_query(F.data.startswith("remonth_"))
async def month(callback: types.CallbackQuery):
    month = callback.data[8:]
    adduserinfo(str(callback.from_user.id), month, 'birth_month', 'users.db', 'bot_users')
    await callback.message.edit_text("Теперь выберите день", reply_markup=days_keyboard_re())

@router.message(Registration.refilling_gender)
async def first_name(message: types.Message, state: FSMContext):
    try:
        gender = message.text
        if gender != "Мужской" and gender != "Женский":
            await message.answer("К сожалению я не могу обработать ваш пол, так что выберите что-то из предложенных вариантов")
            return
        #profile["first_name"] = first_name
        if gender == "Мужской":
            gender = "male"
        else:
            gender = "female"
        adduserinfo(str(message.from_user.id), gender, 'gender', 'users.db', 'bot_users')
        await message.answer("Пол успешно обновлен", reply_markup=main_keyboard())
    except:
        None



@router.callback_query(F.data.startswith("reday_"))
async def day(callback: types.CallbackQuery, state: FSMContext):
    day = callback.data[6:]
    adduserinfo(str(callback.from_user.id), day, 'birth_day', 'users.db', 'bot_users')
    adduserinfo(str(callback.from_user.id), str(1), 'finished_reg', 'users.db', 'bot_users')
    date = getdate(str(callback.from_user.id), 'users.db', 'bot_users')
    adduserinfo(str(callback.from_user.id), star_sign(date[0], date[1]), 'sign', 'users.db', 'bot_users')
    await callback.message.edit_text(text="Ваши данные обновлены")
    await callback.message.answer(text="Теперь вы можете посмотреть гороскоп для своего знака зодиака, смотреть свою натальную карту, а также проверять совместимость", reply_markup=main_keyboard())
    await state.clear()


def star_sign(day, month):  
    if month == 12:  
        print(month)
        sun_sign = 'sagittarius' if (day < 22) else 'capricorn'  
    elif month == 1:  
        print(month)
        sun_sign = 'capricorn' if (day < 20) else 'aquarius'  
    elif month == 2: 
        print(month) 
        sun_sign = 'aquarius' if (day < 19) else 'pisces'  
    elif month == 3:
        print(month)  
        sun_sign = 'pisces' if (day < 21) else 'aries'  
    elif month == 4: 
        print(month) 
        sun_sign = 'aries' if (day < 20) else 'taurus'  
    elif month == 5:  
        print(month)
        sun_sign = 'taurus' if (day < 21) else 'gemini'  
    elif month == 6:  
        print(month)
        sun_sign = 'gemini' if (day < 21) else 'cancer'  
    elif month == 7:  
        print(month)
        sun_sign = 'cancer' if (day < 23) else 'leo'  
    elif month == 8:  
        print(month)
        sun_sign = 'leo' if (day < 23) else 'virgo'  
    elif month == 9:  
        print(month)
        sun_sign = 'virgo' if (day < 23) else 'libra'  
    elif month == 10: 
        print(month) 
        sun_sign = 'libra' if (day < 23) else 'scorpio'  
    elif month == 11:  
        print(month)
        sun_sign = 'scorpio' if (day < 22) else 'sagittarius'  
    return sun_sign  


async def daily_horoscope(bot : Bot):
    users = getusers("users.db", 'bot_users')
    for id in users:
        await bot.send_message(chat_id=id[0], text="Ваш гороскоп на сегодня:")
        await bot.send_message(chat_id=id[0], text=request_ru_today_horoscope(getsign(id[0], 'users.db', 'bot_users')))