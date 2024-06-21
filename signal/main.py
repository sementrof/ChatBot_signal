import os
import random
import time
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta

# Список для хранения уже отправленных фотографий
sent_photos = []

# Функция для обработки нажатия на первую кнопку
def send_text_and_photo(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    
    # Вычисляем текущее время
    current_time = datetime.now()
    # Генерируем случайное количество минут от 1 до 5
    minutes_delay = random.randint(1, 5)
    # Вычисляем будущее время как текущее время плюс случайное количество минут
    future_time = current_time + timedelta(minutes=minutes_delay)
    # Преобразуем время в строку формата "ЧЧ:ММ"
    future_time_str = future_time.strftime("%H:%M")
    
    # Отправляем текстовое сообщение с временем
    update.callback_query.message.reply_text(f"❗️ Время следующего результата: {future_time_str} ❗️\n 🔥Смело можешь ставить свою ставку🔥")
    

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"Привет, {user.first_name}! Мы команда специалистов, занимающаяся извлечением прибыли с нашумевшей игры Lucky Jet🚀", reply_markup=create_button())

# Функция для создания первой кнопки
def create_button() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton("💸Для начала заработка, жми на кнопку💸", callback_data='send_text_and_photo')
    return InlineKeyboardMarkup([[button]])

# Функция для создания второй кнопки с гиперссылкой
def create_second_button() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton("💰Ссылка на сайт💰", url='https://1wzlcz.life/casino/list?open=register&p=pcj5')
    return InlineKeyboardMarkup([[button]])

# Функция для создания третьей кнопки
def create_third_button() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton("❗️Новый сигнал❗️", callback_data='send_next_photo')
    return InlineKeyboardMarkup([[button]])

# Функция для обработки нажатия на первую кнопку
def send_text_and_photo(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    
    # Вычисляем текущее время
    current_time = datetime.now()
    # Генерируем случайное количество минут от 1 до 5
    minutes_delay = random.randint(1, 5)
    # Вычисляем будущее время как текущее время плюс случайное количество минут
    future_time = current_time + timedelta(minutes=minutes_delay)
    # Преобразуем время в строку формата "ЧЧ:ММ"
    future_time_str = future_time.strftime("%H:%M")
    
    # Отправляем текстовое сообщение с временем
    update.callback_query.message.reply_text(f"❗️ Время результат [МСК]: {future_time_str} ❗️\n 🔥Смело можешь ставить свою ставку🔥")
    update.callback_query.answer()
    # Отправляем текстовое сообщение
    time.sleep(2)
    # Получаем список фотографий в папке
    photo_files = [file for file in os.listdir("photos") if file.endswith(('jpg', 'jpeg', 'png'))]
    # Убираем из списка уже отправленные фотографии
    available_photos = [file for file in photo_files if file not in sent_photos]
    if available_photos:
        # Выбираем случайную фотографию из доступных
        photo_filename = random.choice(available_photos)
        # Отправляем фотографию
        with open(os.path.join('photos', photo_filename), 'rb') as photo_file:
            update.callback_query.message.reply_photo(photo=photo_file)
        # Добавляем выбранную фотографию в список отправленных
        sent_photos.append(photo_filename)
    else:
        update.callback_query.message.reply_text("Больше сигналов нет.")
    # После выполнения всех действий, отправляем вторую кнопку с гиперссылкой
    second_button_markup = create_second_button()
    third_button_markup = create_third_button()
    reply_markup = InlineKeyboardMarkup([[second_button_markup.inline_keyboard[0][0], third_button_markup.inline_keyboard[0][0]]])
    update.callback_query.message.reply_text("Выбери действие:", reply_markup=reply_markup)

# Функция для обработки нажатия на вторую кнопку
def handle_second_button(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()

# Функция для обработки нажатия на третью кнопку
def handle_third_button(update: Update, context: CallbackContext) -> None:
    send_text_and_photo(update, context)

def main() -> None:
    # Создание объекта Updater и передача токена Telegram бота
    updater = Updater("6992522888:AAHHybdX1X89U3hwTsJ4ZNPrHDyfWq1VW-0")

    # Получение диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Регистрация обработчика нажатия на первую кнопку
    dispatcher.add_handler(CallbackQueryHandler(send_text_and_photo, pattern='send_text_and_photo'))

    # Регистрация обработчика нажатия на вторую кнопку
    dispatcher.add_handler(CallbackQueryHandler(handle_second_button, pattern='second_button'))

    # Регистрация обработчика нажатия на третью кнопку
    dispatcher.add_handler(CallbackQueryHandler(handle_third_button, pattern='send_next_photo'))

    # Запуск бота
    updater.start_polling()

    # Остановка бота при нажатии Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
