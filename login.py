from instaloader import Instaloader, TwoFactorAuthRequiredException
import os
import time


curent_dir = os.getcwd()
loader = Instaloader()
def login():
    username = 'sohaibfaraji'
    password = 'Aa*#3823219'
    session_file = f"{curent_dir}/login-sohaib"
    try:
        if os.path.isfile(session_file):
            timeoflogin = (time.time() - os.path.getmtime(f"{curent_dir}/login-sohaib"))/(60*60)
            if  timeoflogin < 48:
                print("Loading session...")
                with open(session_file, 'rb') as f:
                    content = f.read()
                    if content.strip():
                        loader.load_session_from_file(username, session_file)
                    else:
                        raise ValueError("Session file is empty!")
            else:
                os.remove(session_file)
                try:
                    print("Logging in...")
                    loader.login(username, password)
                except TwoFactorAuthRequiredException:    
                    loader.two_factor_login(two_factor_code)
                    loader.save_session_to_file(session_file)
                    print("Session saved.")               
        else: 
            try:
                print("Logging in...")
                loader.login(username, password)
            except TwoFactorAuthRequiredException:    
                loader.two_factor_login(two_factor_code)
                loader.save_session_to_file(session_file)
                print("Session saved.")   
    except Exception as e:
        print(f"Error during login: {e}")
        if os.path.exists(session_file):
            os.remove(session_file)
username = "sohaibfaraji"
password = "Aa*#3823219"

if __name__ == "__main__":
    login()
