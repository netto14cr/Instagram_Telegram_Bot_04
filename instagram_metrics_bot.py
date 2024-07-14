import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import instaloader
from instaloader.exceptions import TwoFactorAuthRequiredException, BadCredentialsException
from message_manager import MessageManager  # Import the MessageManager class

# Load environment variables from .env file
load_dotenv()

# Install and configure Instaloader
L = instaloader.Instaloader()

# Global variables for handling 2FA state
requires_2fa = False
two_factor_code = None
username = None
password = None

# Create an instance of MessageManager
message_manager = MessageManager()
current_language = "en"

# Supported languages
LANGUAGES = {
    "en": "en-US",
    "es": "es-ES",
    "de": "de-DE",
    "ja": "ja-JP"
}

# Function to set the language
def set_language(language):
    global current_language
    if language in LANGUAGES:
        current_language = language
        message_manager.set_language(LANGUAGES[language], language)

# Function to log in to Instagram
def login_instagram():
    global requires_2fa, username, password
    print(f"Attempting to log in with username: {username}")  # Add this for debugging
    try:
        L.login(username, password)
    except TwoFactorAuthRequiredException:
        requires_2fa = True
    except BadCredentialsException as e:
        print(f"Credential error: {e}")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e

# Function to complete 2FA authentication
def complete_two_factor_auth(code):
    L.two_factor_login(code)

# Functions to get follower information
def get_followers():
    profile = instaloader.Profile.from_username(L.context, username)
    return list(profile.get_followers())

def get_not_following_back():
    profile = instaloader.Profile.from_username(L.context, username)
    followers = set(profile.get_followers())
    followees = set(profile.get_followees())
    return list(followees - followers)

def get_following_not_followed():
    profile = instaloader.Profile.from_username(L.context, username)
    followers = set(profile.get_followers())
    followees = set(profile.get_followees())
    return list(followers - followees)


def get_UnderscoredText():
    return "--------------------------------------------------------------\n"

# Create and configure the Telegram bot
class InstagramFollowersBot:
    def __init__(self, telegram_token):
        self.telegram_token = telegram_token
        self.application = Application.builder().token(telegram_token).build()
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.language_menu_message = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(message_manager.get_text("start"))
        await self.show_main_menu(update)

    async def show_main_menu(self, update: Update):
        keyboard = [
            [InlineKeyboardButton("Login to Instagram", callback_data='login')],
            [InlineKeyboardButton("Change Language", callback_data='change_language')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            message_manager.get_text("options"),
            reply_markup=reply_markup
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        global requires_2fa, two_factor_code, username, password

        text = update.message.text

        if requires_2fa:
            two_factor_code = text
            try:
                complete_two_factor_auth(two_factor_code)
                requires_2fa = False
                await update.message.reply_text(message_manager.get_text("auth_success"))
                await self.show_options(update)
            except Exception as e:
                await update.message.reply_text(f"{message_manager.get_text('auth_failed')} {e}")
        else:
            try:
                if username is None:
                    username = text
                    await update.message.reply_text("Please enter your password.")
                else:
                    password = text
                    login_instagram()
                    await update.message.reply_text(message_manager.get_text("auth_success"))
                    await self.show_options(update)
            except Exception as e:
                await update.message.reply_text(f"{message_manager.get_text('auth_failed')} {e}")

    async def show_options(self, update: Update):
        keyboard = [
            [InlineKeyboardButton(message_manager.get_text("followers"), callback_data='followers')],
            [InlineKeyboardButton(message_manager.get_text("not_following_back"), callback_data='not_following_back')],
            [InlineKeyboardButton(message_manager.get_text("following_not_followed"), callback_data='following_not_followed')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            message_manager.get_text("options"),
            reply_markup=reply_markup
        )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data

        if data == 'login':
            await query.message.reply_text(message_manager.get_text("login_prompt"))
            await query.answer()
            return

        if data == 'change_language':
            keyboard = [
                [InlineKeyboardButton("English", callback_data='set_language_en')],
                [InlineKeyboardButton("Español", callback_data='set_language_es')],
                [InlineKeyboardButton("Deutsch", callback_data='set_language_de')],
                [InlineKeyboardButton("日本語", callback_data='set_language_ja')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if self.language_menu_message:
                await self.language_menu_message.delete()
            self.language_menu_message = await query.message.reply_text("Select Language:", reply_markup=reply_markup)
            await query.answer()
            return

        if data.startswith('set_language'):
            if data == 'set_language_en':
                set_language("en")
                await query.message.reply_text("Language set to English.")
            elif data == 'set_language_es':
                set_language("es")
                await query.message.reply_text("Idioma establecido a Español.")
            elif data == 'set_language_de':
                set_language("de")
                await query.message.reply_text("Sprache auf Deutsch eingestellt.")
            elif data == 'set_language_ja':
                set_language("ja")
                await query.message.reply_text("言語が日本語に設定されました。")

            # Hide language menu after selection
            if self.language_menu_message:
                await self.language_menu_message.delete()
                self.language_menu_message = None

            await query.answer()
            return

        try:
            if data == 'followers':
                followers = get_followers()
                message = f"{message_manager.get_text('followers').upper()}\n" + \
                          f"{get_UnderscoredText()}\n" + \
                          "\n".join([follower.username for follower in followers])
            elif data == 'not_following_back':
                not_following_back_users = get_not_following_back()
                message = f"{message_manager.get_text('not_following_back').upper()}\n" + \
                          f"{get_UnderscoredText()}\n" + \
                          "\n".join([user.username for user in not_following_back_users])
            elif data == 'following_not_followed':
                following_not_followed_users = get_following_not_followed()
                message = f"{message_manager.get_text('following_not_followed').upper()}\n" + \
                          f"{get_UnderscoredText()}\n" + \
                          "\n".join([user.username for user in following_not_followed_users])
            else:
                message = message_manager.get_text("error")

            await query.message.reply_text(message)
            await query.answer()
        except Exception as e:
            await query.message.reply_text(f"{message_manager.get_text('error')} {e}")

    def run(self):
        self.application.run_polling()

if __name__ == '__main__':
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    bot = InstagramFollowersBot(TELEGRAM_TOKEN)
    bot.run()