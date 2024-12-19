import telebot
from telebot.types import InputMediaPhoto, InputMediaVideo
from telebot.apihelper import ApiTelegramException
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from database import User ,UserSubscription ,SubscriptionPlan
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import lzma
import json
import instaloader
from instaloader import TwoFactorAuthRequiredException
import validators
import re
from datetime import timedelta
from divar import request_to_api , get_data_by_token
import subprocess
import urllib.parse

curent_dir = os.getcwd()
with open('/mnt/txt.txt' , 'r') as d:
    dicti = json.load(d)
CHANNEL_USERNAME = "@INSTACURL"
BOT_TOKEN =dicti['bot_token']
PASS = dicti['mysql']
MYSQL = f"mysql+pymysql://root:{PASS}@localhost:3306/abzar_database"
ADMIN_ID = '6040165079'
DATA_MAX_SIZA = 30 #Megabytes

engine = create_engine(MYSQL, echo=True)
Session = sessionmaker(bind=engine)

loader = instaloader.Instaloader(download_pictures=False, download_videos=False, download_video_thumbnails=False, download_geotags=False, save_metadata=True)

# Telegram Bot setup
bot = telebot.TeleBot(BOT_TOKEN)
logging.basicConfig(filename='Radepa.log', level=logging.INFO, format='%(asctime)s - %(message)s')

""" Block fo User signup"""
#menu reply

def get_user_name_by_id(user_id):
    try:
        user_info = bot.get_chat(user_id)
        full_name = f"{user_info.first_name} {user_info.last_name or ''}".strip()
        return full_name
    
    except Exception as e:
        logging.error(f"name and username not fonud , because : {e}")
        return 'Unknown'
def create_main_menu_reply(tg_id):
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if str(tg_id) == ADMIN_ID:
        #markup.add(KeyboardButton("Instagram"))
        markup.add(KeyboardButton("Register"))
        #markup.add(KeyboardButton("Youtube"))
        markup.add(KeyboardButton("Linkedin"))
        markup.add(KeyboardButton("Divar"))
        #markup.add(KeyboardButton("divar VS digikala"))
        markup.add(KeyboardButton("Crypto Charts"))
        
    else:
        markup.add(KeyboardButton("Divar"))
        markup.add(KeyboardButton("Register"))
        
        
    return markup
#start
def is_user_member(user_id):
    try:
        # بررسی وضعیت کاربر در کانال
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"خطا در بررسی عضویت: {e}")
        return False
@bot.callback_query_handler(func=lambda call:call.data == 'khonsa')
def khonsa(call):
    pass
@bot.message_handler(commands=['start','help'])
def start_handling(message):
    user_tgid = message.from_user.id
    session = Session()
    Uzer = session.query(User).filter_by(telegram_id = str(user_tgid)).first()
    name = get_user_name_by_id(user_tgid)
    if Uzer == None:
        if is_user_member(user_tgid):
            new_user = User(telegram_id = user_tgid ,
                            created_at = datetime.now(),
                            )
            session.add(new_user)
            session.commit()
            default_plan = session.query(SubscriptionPlan).filter_by(name="Free").first()
            days = int(default_plan.duration_days)
            new_user_plan = UserSubscription(
                user_id=new_user.id,
                plan_id=default_plan.id,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(hours=24),  # پلن رایگان بدون تاریخ انقضا
                status="active"                
            )
            session.add(new_user_plan)
            session.commit()
            bot.send_message(user_tgid , f"{name} عزیز ;\nخوش آمدید." , reply_markup = create_main_menu_reply(user_tgid))  
        else:
            bot.send_message(user_tgid , f'You have to join channel to countinue.\n{CHANNEL_USERNAME}') 
    else:
        if is_user_member(user_tgid):
            bot.send_message(user_tgid , f"'{name}' عزیز ;\nمجددا خوش آمدید." , reply_markup = create_main_menu_reply(user_tgid))
        else:
            bot.send_message(user_tgid , f'You have to join channel to countinue.\n{CHANNEL_USERNAME}')

"""End Signup Block """
      
"""registering block"""
@bot.callback_query_handler(func=lambda call :call.data.startswith("transaction_"))
def Payment_rial(call):
    amount = call.data.split('_')[-1]
    pass
    
    
    
@bot.callback_query_handler(func=lambda call :call.data.startswith("subcription_"))
def plan_selection(call):
    session = Session()
    plan_name = call.data.split('_')[1]
    plan = session.query(SubscriptionPlan).filter_by(name=plan_name).first()
    
    
    payment_method = InlineKeyboardMarkup()
    Crypto = payment_method.add(InlineKeyboardButton("پرداخت با کریپتو-در حال فعال سازی",callback_data="khonsa"))
    Rial = payment_method.add(InlineKeyboardButton("پرداخت ریالی-در حال فعال سازی",callback_data=f"transaction_{plan.price}"))
    bot.edit_message_text(f"پلن انتخابی {plan.duration_days} روزه - {plan.price} تومان \nروش پرداخت را انتخاب کنید" ,call.message.chat.id,call.message.message_id,reply_markup=payment_method)
    
@bot.message_handler(func = lambda message:message.text == "Register")
def user_register(message):
    tg_id = message.from_user.id
    session = Session()
    user = session.query(User).filter_by (telegram_id= tg_id).first()
    latest_subscription  = user.subscriptions[0]
    if  latest_subscription.end_date <= datetime.now() :
        payment_markup = InlineKeyboardMarkup()
        payment_markup.add(InlineKeyboardButton("یک ماهه - 30000 تومن",callback_data="subcription_One month"))
        payment_markup.add(InlineKeyboardButton("دو ماهه - 50000 تومن",callback_data="subcription_Two month"))
        payment_markup.add(InlineKeyboardButton("سه ماهه - 70000 تومن",callback_data="subcription_Three month"))
        bot.send_message(message.from_user.id , "لطفا پلنی که قصد خرید را دارید انتخاب کنید.\nلازم به ذکر است که درصورت هرگونه خرابی ربات مبلغ پرداختی بدون شرط به حساب شما عودت داده خواهد شد.",reply_markup=payment_markup)
        
    elif latest_subscription.end_date > datetime.now() :
        
        
        bot.send_message(message.from_user.id , f"شما اشتراک فعال دارید و تا تاریخ:\n{ latest_subscription.end_date} اعتبار دارد.")
        
        print("youre current plan is available still")
    

"""end register block """
"""Divar block"""
def export_device_detailes_from_json(text):
    dictionary = json.loads(text)
    result = {'categry':None ,
              'brand':None,
              'model':None,
              'price':None,
              'ram':None,
              'color':None,
              'hard_space':None
              }
    try:
        categry =dictionary['sections'][4]['widgets'][1]['action_log']['server_side_info']['info']['jli']['category']['value']
        result['categry'] = categry
    except:
        categry =None
    try:
        brand = dictionary['sections'][4]['widgets'][0]['action_log']['server_side_info']['info']['brand']
        result['brand'] = brand
    except:
        brand = None
    try:
        model = dictionary['sections'][4]['widgets'][0]['action_log']['server_side_info']['info']['model']
        result['model'] = model
    except :
        model = None
    for item in dictionary['sections'][4]['widgets']:
        try:
            if item['data']['title'] == 'قیمت':
                price = item['data']['value']
                result['price'] = price
        except:
            price = None
            continue
            
        try:
            if item['data']['title'] ==  'مقدار رم':
                ram = item['data']['value']
                result['ram'] = ram
        except:
            ram = None
            continue
        try:
            if item['data']['title'] ==  'رنگ':
                color = item['data']['value']
                result['color'] = color
        except:
            color = None
            continue
        try:    
            if item['data']['title'] ==  'حافظهٔ داخلی':
                hard_space = item['data']['value']
                result['hard_space']=hard_space
        except:
            hard_space = None
            continue
    return result
    

def find_city_number(name):
    with open(curent_dir + '/bigcitys.json' , 'r' , encoding='utf-8') as city:
        citys = json.load(city)
    for item in citys:
        if item[0] == name:
            return str(item[1])
def find_slug_cat(name):
    with open(curent_dir + '/category.json' , 'r' , encoding = 'utf-8') as cats:
        category = json.load(cats)
    for item in category:
        if item['name'] == name:
            return item["slug"]
def Analyze_response(response):
    js = json.loads(response)
    all_posts = js['list_widgets'] #type = list
    TXT = "لیست 24 آگهی اخیر:\n"
    base_url = 'https://divar.ir/v/'
    for post in all_posts:    
        token = post['data']['action']['payload']['token']
        #chizha = get_data_by_token(token)
        #ex = export_device_detailes_from_json(chizha)
        #bot.send_message(ADMIN_ID , f"device details :{ex}")
        title = post['data']['action']['payload']['web_info']['title']
        p = urllib.parse.quote(title.encode('utf-8'), safe='')
        url = base_url +  p + '/' + token  
        try:
            row = post['data']['title']
            Row = f"[{row}]({url}) : {post['data']['middle_description_text']}\n"
            TXT = "".join(TXT + Row)
        except KeyError:
            row_t = post['data']['title']
            Row2 = f"[{row_t}]({url}) : توافقی\n"
            TXT = "".join(TXT + Row2)
    return TXT
        
@bot.callback_query_handler(lambda call : call.data.startswith('category_'))
def prepare_request(call):
    city = call.message.text.split('\n')[0].split(':')[1].strip()
    text = call.message.text.split('\n')[0]
    category = call.data.split('_')[1]
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.edit_message_text(f"{text}\nدسته بندی انتخاب شده : {category}",call.message.chat.id,call.message.message_id)
    city_number = find_city_number(city)
    category_slug = find_slug_cat(category)
    response = request_to_api(city_number , category_slug)
    result = Analyze_response(response)  
    bot.send_message(call.message.chat.id,result , parse_mode="Markdown") 
    time.sleep(3)

def category_mrkup():
    with open(curent_dir + '/category.json' , 'r' , encoding = 'utf-8') as cats:
        category = json.load(cats)  
    markup = InlineKeyboardMarkup()
    for item in category:
        markup.add(InlineKeyboardButton(item['name'], callback_data=f"category_{item['name']}"))
    return markup  
        
@bot.callback_query_handler(func=lambda call : call.data.startswith("city_"))
def change_city_and_chooscategory(call):
    city = call.data.split('_')[1]
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.edit_message_text(f"شهر شما : {city}\nدسته بندی را انتخاب کنید :",call.message.chat.id,call.message.message_id,reply_markup=category_mrkup())
def divar_markup_citys():
    with open(curent_dir + '/bigcitys.json' , 'r' , encoding = 'utf-8') as citys:
        bigcitis = json.load(citys)
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(item[0], callback_data=f"city_{item[0]}") for item in bigcitis]
    markup.add(*buttons)
    return markup
    
@bot.message_handler(func = lambda message:message.text == "Divar")
def user_register(message):
    session = Session()
    tg_id = message.from_user.id
    user = session.query(User).filter_by(telegram_id = tg_id ).first()
    latest_subscription  = user.subscriptions[0] #0 chon hanooz system register ra nayoftade
    if latest_subscription.end_date < datetime.now() :
        bot.send_message(user.telegram_id , f"اعتبار شما به پایان رسید!\nلطفا از طریق منوی 'Register' نسبت به شارژ مجدد حساب خود اقدام فرمایید.")   
        return
    else:
        bot.send_message(tg_id ,"شهر را انتخاب کنید",reply_markup=divar_markup_citys())


"""END Divar"""

def main():
    try:
        bot.polling(non_stop=True , timeout= 50)
    except Exception as main:
        logging.error(f"bot start nashod : \n {main}")
if  __name__ == "__main__":
    main()
     


