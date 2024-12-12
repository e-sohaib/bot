import telebot
from telebot.types import InputMediaPhoto, InputMediaVideo
from telebot.apihelper import ApiTelegramException
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from database import User
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import lzma
import json
import instaloader
from instaloader import TwoFactorAuthRequiredException
import validators
import re
from divar import request_to_api 

curent_dir = os.getcwd()
with open('/mnt/txt.txt' , 'r') as d:
    dicti = json.load(d)
CHANNEL_USERNAME = "@INSTACURL"
BOT_TOKEN = dicti['bot_token']
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
def create_main_menu_reply(tg_id):
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if str(tg_id) == ADMIN_ID:
        markup.add(KeyboardButton("Instagram"))
        markup.add(KeyboardButton("Register"))
        markup.add(KeyboardButton("Youtube"))
        markup.add(KeyboardButton("Linkedin"))
        markup.add(KeyboardButton("Divar"))
        markup.add(KeyboardButton("Register"))
        
    else:
        markup.add(KeyboardButton("Instagram"))
        
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
    session.commit()
    if Uzer == None:
        if is_user_member(user_tgid):
            new_user = User(telegram_id = user_tgid ,
                            created_at = datetime.now(),
                            )
            session.add(new_user)
            session.commit()
            bot.send_message(user_tgid , "Welcom!" , reply_markup = create_main_menu_reply(user_tgid))  
        else:
            bot.send_message(user_tgid , f'You have to join channel to countinue.\n{CHANNEL_USERNAME}') 
    else:
        if is_user_member(user_tgid):
            bot.send_message(user_tgid , "Welcom Back!" , reply_markup = create_main_menu_reply(user_tgid))
        else:
            bot.send_message(user_tgid , f'You have to join channel to countinue.\n{CHANNEL_USERNAME}')

"""End Signup Block """


"""registering block"""
@bot.message_handler(func = lambda message:message.text == "Register")
def user_register(message):
    tg_id = message.from_user.id
    session = Session()
    user = session.query(User).filter_by (telegram_id= tg_id).first()
    if user.subscriptions :
        print("youre current plan is available still")
    

"""end register block """
"""Divar block"""
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
    
@bot.callback_query_handler(lambda call : call.data.startswith('category_'))
def prepare_request(call):
    city = call.message.text.split('\n')[0].split(':')[1].strip()
    text = call.message.text.split('\n')[0]
    category = call.data.split('_')[1]
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.edit_message_text(f"{text}\nدسته بندی انتخاب شده : {category}",call.message.chat.id,call.message.message_id)
    city_number = find_city_number(city)
    category_slug = find_slug_cat(category)
    bot.send_message(ADMIN_ID , f"check:\n{city}\n{city_number}\n{category_slug}")
    response = request_to_api(city_number , category_slug)
    with open(curent_dir + '/hichi.txt' , 'w' ,encoding='utf-8') as respo:
        respo.write(str(response))
    with open(curent_dir + '/hichi.txt' , 'r' ,encoding='utf-8') as r:
        bot.send_document(ADMIN_ID ,r)    

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
    tg_id = message.from_user.id
    bot.send_message(tg_id ,"شهر را انتخاب کنید",reply_markup=divar_markup_citys())


"""END Divar"""
""" Instagram Block """



def is_valid_instagram_link(link):
    """
    بررسی صحت لینک اینستاگرام
    """
    if validators.url(link) and "instagram.com" in link:
        return True
    return False

def detect_content_type(link):
    """
    تشخیص نوع محتوا از لینک
    """
    if "/p/" in link:
        return "post"
    elif "/reel/" in link:
        return "reel"
    elif "/stories/" in link:
        return "story"
    elif "/tv/" in link:
        return "igtv"
    else:
        return None

def download_instagram_content(link , tg_id):
    session_file = f"{curent_dir}/login-sohaib"
    if os.path.isfile(session_file):
        loader.load_session_from_file(session_file)
        print('loged in seccessfully.')
    """
    دانلود محتوا از اینستاگرام
    """
    if not is_valid_instagram_link(link):
        bot.send_message(tg_id,"Incorrect Link.\nCorrect link sample : \thttps://www.instagram.com/p/abcdefghijk/")
    content_type = detect_content_type(link)
    if not content_type:
        bot.send_message(tg_id,"The type of link entered is not recognized.")
    try:
        if content_type == "post":
            shortcode = re.search(r"/p/([^/]+)/", link).group(1)
        elif content_type == "reel":
            shortcode = re.search(r"/reel/([^/]+)/", link).group(1)
        elif content_type == "story":
            bot.send_message(tg_id,"Download story is login required.")
            
        elif content_type == "igtv":
            shortcode = re.search(r"/tv/([^/]+)/", link).group(1)
        else:
            bot.send_message(tg_id,"File format not suported.")
            
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        post_id = link.split('/')[-2]
        loader.filename_pattern = f"{tg_id}_{post_id}"
        loader.dirname_pattern = f'instadownloads-{tg_id}'
        # دانلود محتوا
        download_started = bot.send_message(tg_id,f"Download started...")
        time.sleep(0.5)
        loader.download_post(post, target=content_type)
        Success = bot.edit_message_text("The download was done successfully.",download_started.chat.id ,download_started.message_id)
        time.sleep(0.5)
        ig_json_dump(tg_id ,post_id)
        #upload too telegram
        bot.edit_message_text('Uploading to telegram' , Success.chat.id ,Success.message_id)
        #all_in_dir = os.listdir(f"{curent_dir}/instadownloads-{tg_id}/")
        #for item in all_in_dir:    
        #    if item.split('.')[-1] != "jpg" :
        #        try:
        #            with open(f"{curent_dir}/instadownloads-{tg_id}/{item}" ,'rb') as ax:
        #                bot.send_photo(tg_id , ax ,caption=ig_caption(tg_id),reply_markup=ig_reply_markup(tg_id,post_id))
        #        except Exception as error :
        #            #bot.forward_message(chat_id=tg_id ,from_chat_id=BOT_TOKEN.split(":")[0], message_id = item)
        #            bot.send_message(tg_id , f'Unsuported Image***\n{error}')
        #        try:        
        #            if item.split('.')[-1] != "mp4" :
        #                with open(f"{curent_dir}/instadownloads-{tg_id}/{item}" ,'rb') as film:
        #                    bot.send_video(tg_id , film ,caption=ig_caption(tg_id),reply_markup=ig_reply_markup(tg_id , post_id))
        #        except Exception as ERR :
        #            bot.send_message(tg_id , f'Unsuported video{ERR}**\n')
        try:
            with open(f"{curent_dir}/instadownloads-{tg_id}/{tg_id}_{post_id}.json" , 'r') as jj:
                dicte = json.load(jj)
            cdn_link = dicte['node']["video_url"] 
            bot.send_message(tg_id , f'Click to Download : \t[Download Link]({cdn_link})' ,reply_markup=ig_reply_markup(tg_id , post_id),parse_mode="Markdown")           
            caption = ig_caption(tg_id)
            bot.send_message(tg_id , f"Caption:\n{caption}")
            comments = 'Some comments:\n'
            i = 1  
            for item in ig_coments(tg_id,post_id):
                comments = ''.join(f"{comments}{i} - {item}\n")
                i+=1
            bot.send_message(tg_id , comments)   
        except Exception as E:
            bot.send_message(tg_id,f"Error Uploading link.{E}")
             
    except Exception as e: 
        bot.send_message(tg_id,f"Error downloading link.{e}")

#uplaod customizig
def ig_caption(tg_id):
    for item in os.listdir(f"{curent_dir}/instadownloads-{tg_id}/"):
        if item.split('.')[-1] == 'txt':
            with open(f"{curent_dir}/instadownloads-{tg_id}/{item}" , 'r' , encoding = 'utf-8') as cap:
                caption = cap.read()
            return str(caption)
#extract .json.xs to json
def ig_json_dump(tg_id,post_id):
    for item in os.listdir(f"{curent_dir}/instadownloads-{tg_id}/"):
        if item.split('.')[-1] == 'xz':
            path = f'{curent_dir}/instadownloads-{tg_id}/{item}'
            output_file = f'{curent_dir}/instadownloads-{tg_id}/{tg_id}_{post_id}.json'
            with lzma.open(path, "rb") as compressed_file:
                raw_data = compressed_file.read().decode("utf-8")
                json_data = json.loads(raw_data)
            with open(output_file, "w") as extracted_file:
                json.dump(json_data, extracted_file, indent=4)
            return
#read json and prepare markup        
def ig_reply_markup(tg_id,post_id):
    
    with open(f'{curent_dir}/instadownloads-{tg_id}/{tg_id}_{post_id}.json', 'r' ,encoding='utf-8') as m:
        dic = json.load(m)
        
    likes_count = dic['node']["edge_media_preview_like"]['count']
    comments_count = dic['node']["edge_media_preview_comment"]['count']
    likes=InlineKeyboardButton(f"Likes ❤️ {likes_count}", callback_data="khonsa")
    comments = InlineKeyboardButton(f"Comments 💬 {comments_count}", callback_data="khonsa")
    markup = InlineKeyboardMarkup([[likes, comments]])
    return markup
#load comments
def ig_coments(tg_id,post_id):
    with open(f'{curent_dir}/instadownloads-{tg_id}/{tg_id}_{post_id}.json', 'r' ,encoding='utf-8') as m:
        dic = json.load(m)
    listofcomments =[]
    A = dic['node']
    ALL_COMMENTS = A['edge_media_to_parent_comment']['edges']
    for item in ALL_COMMENTS:
        listofcomments.append(item['node']['text'])
    return listofcomments        
#instadownloader
def download_ig(message , session):
    t0 = time.time()
    user = session.query(User).filter_by(telegram_id = message.from_user.id ).first()
    if not user.subscriptions.name:
        bot.send_message(user.telegram_id , f"You reached limit")   
        return
    elif user.subscriptions.name:
        link = message.text
        tg_id = user.telegram_id
        bot.send_message(user.telegram_id , "Wait a moment ...")
        download_instagram_content(link , str(tg_id))
        #user.daily_requests = user.daily_requests + 1 
        Bytes = size_meter(tg_id)
        bot.send_message(user.telegram_id , f'remaing requests {user.subscriptions.duration_days}\nyoure data usage : {Bytes/(1024*1024)} MB')
        t1 = time.time()
        bot.send_message(ADMIN_ID , f'time elapsed: {t1 - t0}')
        clear_user_files(tg_id)
        session.commit()
        return
    
#size meter
def size_meter(tg_id):
    here = os.getcwd()
    targ = f"{here}/instadownloads-{tg_id}"
    listofdir = os.listdir(targ)
    totalsize = 0
    for item in listofdir :
        if not os.path.isdir(f'{targ}/{item}'):
            size_bytes = os.path.getsize(f'{targ}/{item}')
            totalsize += size_bytes     
    return totalsize
#clear directory of user
def clear_user_files(tg_id):
    files = os.listdir(f"{curent_dir}/instadownloads-{tg_id}")
    for file in files:
        os.remove(f"{curent_dir}/instadownloads-{tg_id}/{file}")
    #os.remove(file)
#handle Instagram message       
@bot.message_handler(func=lambda message:message.text == "Instagram")
def start_handling(message):
    if is_user_member(message.from_user.id):
        session = Session()
        mess =bot.reply_to(message, "send an instagram valid link")
        bot.register_next_step_handler(mess, download_ig ,session)
    else:
        bot.send_message(message.from_user.id , f'You have to join channel to countinue.')
#handle Youtube message       
@bot.message_handler(func=lambda message:message.text == "Youtube")
def start_handling(message):
    pass

def main():
    try:
        bot.polling(non_stop=True , timeout= 50)
    except Exception as main:
        logging.error(f"bot start nashod : \n {main}")
if  __name__ == "__main__":
    main()
     


