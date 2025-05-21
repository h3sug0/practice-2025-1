import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# === Настройки ===
BOT_TOKEN = "7696960406:AAEHoRPVJLInEyhlXAXry_L-fDd5o7LE9Vg"

# === Логирование ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n"
        "Я бот к проекту:\n"
        "«Разработка аппаратно-программного комплекса дистанционного управления беспилотной техникой»\n\n"
        "Доступные команды:\n"
        "/about — проблема и название проекта\n"
        "/goal — цель и актуальность\n"
        "/tasks — ключевые задачи\n"
        "/result — ожидаемый результат\n"
        "/test — проверь себя в конце"
    )

# === Команда /about ===
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Название проекта:\n"
        "Разработка аппаратно-программного комплекса дистанционного управления беспилотной техникой и передачи данных посредством сети интернет.\n\n"
        "📌 Проблематика:\n"
        "В настоящее время большинство беспилотной техники, контролируемой человеком-оператором, требует использования специального пульта управления, который представляет собой дополнительное носимое устройство. Таким образом, он занимает определенное количество места и обладает определенной массой, что может вызывать неудобства. Вместе с тем, в наше время стали широко распространены и доступны телефоны с доступом в интернет. Это привело к тому, что у каждого человека всегда имеется смартфон с интернет-браузером."
    )

# === Команда /goal ===
async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 Цель:\n"
        "Обеспечение возможности управления колесной базой и сбора данных с неё без применения специализированного оборудования, используя смартфон.\n\n"
        "📌 Актуальность:\n"
        "В настоящее время активно развивается беспилотная техника, работающая как в автоматическом режиме, так и под управлением оператора. Независимо от способа управления имеет место передача данных между компонентами системы. С учетом современного развития и доступности интернета становится особенно актуальной разработка программно-аппаратного комплекса для дистанционного управления через сеть."
    )

# === Команда /tasks ===
async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Ключевые задачи:\n"
        "1. Разработка back-end части веб-приложения.\n"
        "2. Создание front-end интерфейса приложения.\n"
        "3. Программирование управления драйверами мотор-колес.\n"
        "4. Реализация алгоритмов обработки данных, собираемых беспилотной техникой.\n"
        "5. Обеспечение связи между отдельными компонентами программного комплекса."
    )

# === Команда /result ===
async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Ожидаемый результат:\n"
        "Программно-аппаратный комплекс для дистанционного управления беспилотной техникой и передачи данных через интернет.\n\n"
        "Разработанный прототип будет являться универсальным управляющим устройством, которое может быть встроено с минимальными доработками в широкий ряд разрабатываемых колесных баз, приводимых в движение электромоторами."
    )

# === Команда /test – тестирование знаний ===
QUESTION_INDEX = 0
CORRECT_ANSWERS = 0

QUESTIONS = [
    {
        "text": "Какова основная цель проекта?\nA) Управление светофором\nB) Управление колесной базой через смартфон\nC) Создать игру",
        "correct": "B"
    },
    {
        "text": "Какое устройство используется для управления моторами?\nA) Raspberry Pi\nB) Arduino\nC) Пульт ДУ",
        "correct": "B"
    },
    {
        "text": "Что передается между устройствами?\nA) Музыка\nB) Данные телеметрии и команды\nC) Фильмы",
        "correct": "B"
    },
    {
        "text": "Почему важно использовать интернет для управления?\nA) Он сложен в использовании\nB) Он нужен только для игр\nC) Он всегда доступен у пользователя",
        "correct": "C"
    },
    {
        "text": "Какой интерфейс используется для взаимодействия?\nA) Консоль\nB) Веб-браузер\nC) Только мобильное приложение",
        "correct": "B"
    }
]

# === Обработка ответов на тест ===
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global QUESTION_INDEX, CORRECT_ANSWERS
    QUESTION_INDEX = 0
    CORRECT_ANSWERS = 0
    await ask_question(update)

async def ask_question(update: Update):
    if QUESTION_INDEX < len(QUESTIONS):
        await update.message.reply_text(QUESTIONS[QUESTION_INDEX]["text"])
    else:
        await finish_test(update)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global QUESTION_INDEX, CORRECT_ANSWERS
    user_answer = update.message.text.strip().upper()

    correct_answer = QUESTIONS[QUESTION_INDEX]["correct"]
    if user_answer == correct_answer:
        CORRECT_ANSWERS += 1
    QUESTION_INDEX += 1
    await ask_question(update)

async def finish_test(update: Update):
    total = len(QUESTIONS)
    score = CORRECT_ANSWERS
    await update.message.reply_text(
        f"🏁 Тест завершён!\nВы ответили правильно на {score} из {total} вопросов.\n"
        "Спасибо за прохождение теста!"
    )

# === Основная функция запуска бота ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрация команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("goal", goal))
    app.add_handler(CommandHandler("tasks", tasks))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("test", test))

    # Обработка ответов на тест
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    print("🟢 Бот запущен...")
    app.run_polling()

# === Точка входа ===
if __name__ == '__main__':
    main()