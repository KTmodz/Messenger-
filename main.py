import subprocess
import sys

# List of required modules
required_modules = ['telebot', 'requests']

# Check if required modules are installed, install if not
def check_install_modules():
    installed = set(module.__name__ for module in sys.modules.values())
    for module in required_modules:
        if module not in installed:
            print(f"Installing {module}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])

# Check and install required modules
check_install_modules()

# Import required modules after installation
import telebot
import requests
import unicodedata
import re

API_TOKEN = '6440604052:AAHb4Yfvvzk45cIUb2otc0bsRUhAqmVn1hg'
bot = telebot.TeleBot(API_TOKEN)

def is_plain_text(text):
    """Check if the text is primarily plain ASCII text."""
    try:
        unicodedata.normalize('NFKD', text).encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def has_text_content(text):
    """Check if the text has any meaningful content (excluding emojis)."""
    for char in text:
        if unicodedata.category(char) != 'So':  # So: Symbol, Other
            return True
    return False

def is_phone_number(text):
    """Check if the text is a phone number."""
    # Simple regex pattern to match Bangladeshi phone numbers
    pattern = r'^\d{11}$'  # Matches exactly 11 digits
    return bool(re.match(pattern, text))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = ("Hey Ami Hocchi Simi, tumi chaile amake jaan boleo dakte paro👉🥺👈")
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_text = message.text
    
    # Check if the message contains any meaningful text content
    if has_text_content(user_text):
        # Check if the message is a phone number
        if is_phone_number(user_text):
            bot.reply_to(message, "Number dite bolsi tai bole diye diba? Tmi ki loyal na? Tmr theke eigula asha kori nai.")
        else:
            try:
                response = requests.get(f"https://ax-tools.team-ax.xyz/AI/?text={user_text}")
                response_data = response.json()
                
                if "success" in response_data:
                    bot.reply_to(message, response_data["success"])
                else:
                    bot.reply_to(message, "Sorry, I couldn't understand your message.")
            except Exception as e:
                bot.reply_to(message, "An error occurred. Please try again later.")
    else:
        bot.reply_to(message, "Eigula bad dao bujhcho ami emoji ba eirokom kichu pochondo kori na.")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot polling failed: {e}")
        time.sleep(15)  # Wait for 15 seconds before restarting polling
