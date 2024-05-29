from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from geopy.distance import geodesic

# Введите сюда ваш токен API
TOKEN = '7392948042:AAEd2iztW1fZijI4Y0UD83T7dRNiKvhFEoI'


# Функция, которая вычисляет расстояние между координатами
def calculate_distance(lat1, lon1, lat2, lon2):
    location1 = (lat1, lon1)
    location2 = (lat2, lon2)
    return geodesic(location1, location2).kilometers


# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Отправьте мне две пары координат в формате: lat1,lon1 lat2,lon2')


# Обработчик сообщений с координатами
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    try:
        coords = text.split()
        if len(coords) != 2:
            raise ValueError("Неправильное количество координат")

        lat1, lon1 = map(float, coords[0].split(','))
        lat2, lon2 = map(float, coords[1].split(','))

        distance = calculate_distance(lat1, lon1, lat2, lon2)
        await update.message.reply_text(f'Расстояние: {distance:.2f} км')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}')


# Основная функция для запуска бота
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
