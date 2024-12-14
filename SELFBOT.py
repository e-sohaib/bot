from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights


api_id = '28812868'
api_hash = '5962d36e4a4ab8108eb4ac1231307669'
session_name = 'clinet_manager'



# لیست کلمات ممنوعه
banned_words = ['kir', 'کیر', 'بی شرف', 'تخم حروم']

# اتصال به تلگرام
client = TelegramClient('session_name', api_id, api_hash)

# تنظیمات محدودیت کاربر
ban_rights = ChatBannedRights(
    until_date=None,  # محدودیت دائمی
    send_messages=True  # جلوگیری از ارسال پیام
)

# تابع برای مدیریت پیام‌ها
@client.on(events.NewMessage(chats='https://t.me/testselft'))
async def handle_new_message(event):
    try:
        # بررسی پیام
        message_text = (event.message.text or "").lower()  # متن پیام به حروف کوچک
        if any(word in message_text for word in banned_words):
            # حذف پیام
            await event.delete()
            print(f"پیام غیرمجاز حذف شد: {event.message.text}")

            # ارسال هشدار به کاربر
            user = await event.get_sender()
            warning_message = (
                f"⚠️ کاربر گرامی @{user.username or user.id}, "
                "پیام شما شامل کلمات غیرمجاز بوده و حذف شد. لطفاً قوانین گروه را رعایت کنید."
            )
            await client.send_message(user.id, warning_message)
            print(f"هشدار به کاربر {user.username or user.id} ارسال شد.")

            # اختیاری: بلاک کردن کاربر
            # group = await client.get_entity(group_username)
            # await client(EditBannedRequest(group, user, ban_rights))
            # print(f"کاربر {user.username or user.id} بلاک شد.")
    except Exception as e:
        print(f"خطا در مدیریت پیام: {e}")

# شروع ربات
async def main():
    print("ربات مدیریت پیام در حال اجرا است...")
    await client.start()
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
