import os
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def random_data():
    letters = string.ascii_lowercase
    name = "User " + ''.join(random.choices(letters, k=5))
    email = ''.join(random.choices(letters, k=12)) + "@gmail.com"
    password = "Pass" + ''.join(random.choices(string.digits, k=6)) + "!"
    return name, email, password

file_name = "tai_khoan_2000.txt"
service = Service(ChromeDriverManager().install())

chrome_options = Options()
chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# Khởi tạo trình duyệt 1 lần duy nhất để dùng cho nhiều lượt
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)

success_count = 0
for i in range(1, 2001):
    print(f"[{i}/2000] Đang xử lý...", end=" ", flush=True)
    
    try:
        # Truy cập trang
        driver.get("https://clickmoney.online/register?ref=ref_621")
        
        # Đợi form
        inputs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
        
        name, email, pwd = random_data()
        inputs[0].send_keys(name)
        inputs[1].send_keys(email)
        inputs[2].send_keys(pwd)
        
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit'] | //button[contains(text(), 'Đăng Ký')]")
        submit_btn.click()

        # Đợi phản hồi ngắn
        time.sleep(1.2)
        
        # Ghi file
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(f"{email} | {pwd}\n")
        
        success_count += 1
        print(f"OK!")

        # Cứ sau 50 lần thì khởi động lại trình duyệt để giải phóng bộ nhớ
        if i % 50 == 0:
            driver.quit()
            driver = webdriver.Chrome(service=service, options=chrome_options)
            wait = WebDriverWait(driver, 15)
            print(">>> Đã reset trình duyệt để giải phóng RAM")

    except Exception:
        print("LỖI (Đang thử lại lượt sau)")
        # Nếu lỗi quá nặng, khởi động lại driver
        try:
            driver.quit()
            driver = webdriver.Chrome(service=service, options=chrome_options)
            wait = WebDriverWait(driver, 15)
        except:
            pass

print(f"\n=== HOÀN TẤT! Thành công {success_count}/2000 tài khoản ===")
driver.quit()
