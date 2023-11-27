import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes,
)


# Required Bot Info

load_dotenv()
TOKEN: Final = os.getenv('TOKEN')
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')


# Available Commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to my world of buffering!!!\nType or click /help to check out available commands")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
        Available Commands are:
        /start -> Welcoming Message
        /help -> Displays Available Commands to Pick From
        /about_bot -> Gives a Description About the Bot
        /about_creator -> Gives a Description About the Developer (NOT GOD)
        /factorial [number] -> Calculates the Factorial for a Given Number (i.e. /factorial 9)
        """
    )
        # /image [title] -> Sends an Image Based on Specified Title

async def about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm the first version of this project with so much potential to evolve into something amazing")


async def about_creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This project was developed and currently maintained by Zyrx, contact email: zyrx99x@gmail.com")


def calculate_factorial(number: int) -> int:
    if number == 1:
        return 1
    else:
        return number * calculate_factorial(number-1)

async def factorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        message: str = "Please type the command /factorial followed by a valid number (i.e /factorial 9)"
    else:
        number: str = context.args[0]
        if number.isdigit():
            result: int = calculate_factorial(int(number))
            message: str = f"The factorial for {number} is {result}"
        else:
            message: str = "Please enter a valid number"
    await update.message.reply_text(message)

# async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """
#     Here functionality must be fetching all images meeting a specific image name
#     and sending them either one by one or three by three, perhaps even add a param for that
#     """
#     if len(context.args) == 0:
#         message: str = "Please type the command /image followed by a valid url (i.e /image link)"
#     else:
#         url: str = context.args[0]
#         # here we need to add conditions to validate the url.
#         await update.message.answer_photo(url)
#     await update.message.reply_text(message)

# End of Commands

# Responses

def handle_response(text: str) -> str:
    processed_text = text.lower()

    if "hello" in processed_text:
        return "Hey there!"

    elif "how are you" in processed_text:
        return "I think I'm under the weather yet in the clouds..."

    elif "what do you know" in processed_text:
        return "I know that my creator is the best"

    else:
        return "I'm not trained for this"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # the line below informs us if it's a private or group chat
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # print(f"User: {update.message.chat.id} in {message_type}: {text}")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)

        else:
            return
    else:
        response: str = handle_response(text)

    # print(f"Bot's Response: {response}")

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == '__main__':
    print("Starting Bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('about_bot', about_bot))
    app.add_handler(CommandHandler('about_creator', about_creator))
    app.add_handler(CommandHandler('factorial', factorial))
    # app.add_handler(CommandHandler('image', image))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Keep track of new messages and updates
    print("Polling...")
    app.run_polling(poll_interval=3)
