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
    link = message.text
    tg_id = user.telegram_id
    bot.send_message(user.telegram_id , "Wait a moment ...")
    download_instagram_content(link , str(tg_id))
    #user.daily_requests = user.daily_requests + 1 
    Bytes = size_meter(tg_id)
    #bot.send_message(user.telegram_id , f'remaing requests {user.subscriptions.duration_days}\nyoure data usage : {Bytes/(1024*1024)} MB')
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
    bot.send_message(ADMIN_ID ,f"Download director : {files}")
    for file in files:
        try:
            os.remove(f"{curent_dir}/instadownloads-{tg_id}/{file}")
        except Exception as E:
            bot.send_message(ADMIN_ID , f"error : {E}")
    #os.remove(file)
#handle Instagram message       
@bot.message_handler(func=lambda message:message.text == "Instagram")
def start_handling(message):
    if is_user_member(message.from_user.id):
        session = Session()
        tg_id = message.from_user.id
        user = session.query(User).filter_by(telegram_id = tg_id ).first()
        latest_subscription  = user.subscriptions[0] #0 chon hanooz system register ra nayoftade
        if  latest_subscription.end_date < datetime.now() :
            bot.send_message(user.telegram_id , f"You reached limit")   
            return
        mess =bot.reply_to(message, "send an instagram valid link")
        bot.register_next_step_handler(mess, download_ig ,session)
    else:
        bot.send_message(message.from_user.id , f'You have to join channel to countinue.')
#handle Youtube message       
@bot.message_handler(func=lambda message:message.text == "Youtube")
def start_handling(message):
    pass
"""Spotify"""
def dl_spotfy(message , session):
    link = message.text
    command = ["spotdl", link]
    bot.reply_to(message ,'دانلود شروع شد')
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode == 0:
        bot.reply_to(message ,'دانلود تکمیل شد')
        for item in os.listdir(curent_dir):
            if item.split('.')[-1] == 'mp3':
                with open(curent_dir + '/' + item , 'rb') as mp3 :
                    bot.send_audio(message.from_user.id , mp3)
                os.remove(item)
    else:
        bot.reply_to(message , 'خطایی رخ داد')
    
@bot.message_handler(func = lambda message:message.text == "Spotify")
def spotify(message):
    if is_user_member(message.from_user.id):
        session = Session()
        tg_id = message.from_user.id
        user = session.query(User).filter_by(telegram_id = tg_id ).first()
        latest_subscription  = user.subscriptions[0] #0 chon hanooz system register ra nayoftade
        if  latest_subscription.end_date < datetime.now() :
            bot.send_message(user.telegram_id , f"You reached limit")   
            return
        mess =bot.reply_to(message, "send an Spotify valid link")
        bot.register_next_step_handler(mess, dl_spotfy ,session)
    else:
        bot.send_message(message.from_user.id , f'You have to join channel to countinue.')
@bot.callback_query_handler(func=lambda call :call.data.startswith("khonsa"))        
def khonsa(call):
    pass        
"""End spotify"""  
