import telebot
import os
from dotenv import load_dotenv

load_dotenv()  # Загружает .env файл
# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Типы вопросов и соответствующие типы темпераментов
TEMPERAMENTS = {
    'Холерик': ['активный', 'решительный'],
    'Меланхолик': ['чувствительный', 'замкнутый'],
    'Флегматик': ['спокойный', 'рассудительный'],
    'Сангвиник': ['общительный', 'весёлый']
}

def start(update: Update, context):
    """Обработчик команды /start"""
    reply_keyboard = [
        [KeyboardButton('Активный'), KeyboardButton('Спокойный')],
        [KeyboardButton('Решительный'), KeyboardButton('Рассудительный')]
    ]
    update.message.reply_text(
        text="Привет! Я помогу определить твой тип темперамента.\\n\\nВыбери характеристики, наиболее подходящие твоему поведению:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard)
    )
    return 1  # Переход к следующему этапу разговора

def process_choice(update: Update, context):
    """Обработка выбора пользователя"""
    user_answer = update.message.text.lower()
    temperament_results = {}
    
    for key in TEMPERAMENTS.keys():
        if any(word in user_answer for word in TEMPERAMENTS[key]):
            temperament_results[key] = True
            
    result_message = ''
    if len(temperament_results) > 0:
        result_message += f"Твой тип темперамента склоняется к:\\n"
        for t in temperament_results.keys():
            result_message += f"- {t}\\n"
    else:
        result_message = "Ваш выбор не соответствует ни одному типу темперамента."
        
    update.message.reply_text(result_message)
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_choice)]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    print("Bot is running...")
    application.run_polling()
