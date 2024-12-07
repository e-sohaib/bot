import requests
l = requests.get('https://www.instagram.com/p/DATmqpxNPe-/')
response = requests.get(l, stream=True)

# بررسی موفقیت درخواست
if response.status_code == 200:
    # ذخیره فایل
    with open("downloaded_file.mp4", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    print("فایل با موفقیت دانلود شد!")
else:
    print(f"خطا در دانلود فایل. کد وضعیت: {response.status_code}")