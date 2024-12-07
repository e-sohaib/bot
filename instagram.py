import instaloader
import validators
import re

# لاگین به حساب کاربری

loader = instaloader.Instaloader()



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
    """
    دانلود محتوا از اینستاگرام
    """
    if not is_valid_instagram_link(link):
        return ("Incorrect Link.")
    content_type = detect_content_type(link)
    if not content_type:
        return("The type of link entered is not recognized.")
    try:
        if content_type == "post":
            shortcode = re.search(r"/p/([^/]+)/", link).group(1)
        elif content_type == "reel":
            shortcode = re.search(r"/reel/([^/]+)/", link).group(1)
        elif content_type == "story":
            return("Download story is login required.")
            
        elif content_type == "igtv":
            shortcode = re.search(r"/tv/([^/]+)/", link).group(1)
        else:
            return("File format not suported.")
            
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.filename_pattern = tg_id
        loader.dirname_pattern = f'instadownloads-{tg_id}'
        # دانلود محتوا
        print(f"در حال دانلود {content_type} با شناسه {shortcode}...")
        loader.download_post(post, target=content_type)
        return("The download was done successfully." , )

    except Exception as e:
        
        return (f"Error downloading link.")

#if __name__ == "__main__":
#    link = input("لینک اینستاگرام را وارد کنید: ")
#    download_instagram_content(link)
