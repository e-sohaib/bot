from instaloader import Instaloader, TwoFactorAuthRequiredException

# ایجاد یک نمونه از Instaloader
loader = Instaloader()

username = "sohaibfaraji"
password = "Aa*#3823219"

try:
    # تلاش برای ورود
    loader.login(username, password)
    print("Logged in successfully!")
except TwoFactorAuthRequiredException:
    # درخواست کد تأیید از کاربر
    two_factor_code = input("Enter the 2FA code sent to your device: ")
    try:
        # تأیید کد دومرحله‌ای
        loader.two_factor_login(two_factor_code)
        print("Logged in successfully with 2FA!")
    except Exception as e:
        print(f"2FA login failed: {e}")
except Exception as e:
    print(f"Login failed: {e}")
