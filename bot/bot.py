import os
import telebot
from dotenv import load_dotenv
from telebot.apihelper import ApiTelegramException
from telebot import types
from database.models import OfferCityOlx


load_dotenv()

CHAT_ID = os.environ.get("CHAT_ID")


def sender_message_wrapper(bot_method):
    def wrapper(text, *args, **kwargs):
        try:
            return bot_method(CHAT_ID, text, *args, **kwargs)
        except ApiTelegramException as exp:
            print(exp)
            return False

    return wrapper


bot = telebot.TeleBot(os.environ.get("BOT_TOKEN_KEY"))
bot.send_message = sender_message_wrapper(bot.send_message)


def city_olx_markup():
    markup = types.ReplyKeyboardMarkup()
    all_offers = OfferCityOlx.get_all()
    for offer in all_offers:
        command = f"/set_olx_city {offer.city}"
        if offer.enabled:
            command += " disable"
        else:
            command += " enable"

        markup.add(command)

    return markup


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    # Class will check whether the user is admin or creator in group or not
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']


# To register filter, you need to use method add_custom_filter.
bot.add_custom_filter(IsAdmin())


@bot.message_handler(commands=['setting'], is_admin=True)
def setting(message):
    markup = types.ReplyKeyboardMarkup()
    get_cities_olx = types.KeyboardButton('/get_olx')
    add_city_olx = types.KeyboardButton('/add_city_olx')

    markup.add(get_cities_olx, add_city_olx)

    bot.send_message(
        text="settings",
        reply_to_message_id=message.message_id,
        reply_markup=markup,
    )


@bot.message_handler(commands=["get_olx"], is_admin=True)
def get_olx_cities(message):
    bot.send_message(
        "set olx city",
        reply_to_message_id=message.message_id,
        reply_markup=city_olx_markup(),
    )


@bot.message_handler(commands=["set_olx_city"], is_admin=True)
def set_olx_city(message):
    city_data = message.text.split(" ")
    if len(city_data) != 3:
        return

    city = OfferCityOlx.get_by_city(city=city_data[1])
    if city:
        if city_data[2] == "enable":
            OfferCityOlx.enable(id=city.id)
        else:
            OfferCityOlx.disable(id=city.id)

    bot.send_message(
        "set olx city",
        reply_to_message_id=message.message_id,
        reply_markup=city_olx_markup(),
    )


@bot.message_handler(commands=["add_city_olx"], is_admin=True)
def add_olx_city(message):
    print(message.text)
    markup = types.ForceReply(selective=False)
    bot.send_message("city:", reply_markup=markup)


@bot.message_handler(is_admin=True)
def echo(message):
    if message.reply_to_message:
        msg_data = message.reply_to_message.text.split()
        if len(msg_data) == 1:
            if message.reply_to_message.text == "city:":
                markup = types.ForceReply(selective=False)
                bot.send_message(f"{message.text} url:", reply_markup=markup)
        elif msg_data[1] == "url:":
            city = msg_data[0]
            url = message.text
            OfferCityOlx.create(city=city, url=url)

            bot.send_message(
                "set olx city",
                reply_to_message_id=message.message_id,
                reply_markup=city_olx_markup(),
            )
