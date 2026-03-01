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

# Hàm tạo dữ liệu ngẫu nhiên
def random_data():
    letters = string.ascii_lowercase
    name = "User " + ''.join(random.choices(letters, k=5))
    email = ''.join(random.choices(letters, k=10)) + "@gmail.com"
    password = "Pass" + ''.join(random.choices(string.digits, k=6)) + "!"
    return name, email, password

file_name = "tai_khoan_da_tao.txt"
# Khởi tạo Service 1 lần để chạy nhanh hơn
service = Service(ChromeDriverManager().install())

# Cấu hình trình duyệt chạy ngầm
chrome_options = Options()
chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

print("=== BẮT ĐẦU ĐĂNG KÝ 100 TÀI KHOẢN ===")

for i in range(1, 101):
    print(f"[{i}/100] Đang xử lý...", end=" ", flush=True)
    
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(20)
        
        # Truy cập trang web từ video bạn gửi
        driver.get("https://clickmoney.online/register?ref=ref_621")
        
        # Đợi các ô nhập liệu xuất hiện
        wait = WebDriverWait(driver, 10)
        inputs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
        
        if len(inputs) >= 3:
            name, email, pwd = random_data()
            
            # Điền dữ liệu
            inputs[0].send_keys(name)
            inputs[1].send_keys(email)
            inputs[2].send_keys(pwd)
            
            # Click nút Đăng ký
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit'] | //button[contains(text(), 'Đăng Ký')]")
            submit_btn.click()

            # Chờ 1 giây để hệ thống nhận dữ liệu
            time.sleep(1)
            
            # Ghi kết quả vào file
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(f"Email: {email} | Pass: {pwd}\n")
            
            print(f"THÀNH CÔNG: {email}")
        else:
            print("LỖI: Không thấy form")
            
    except Exception as e:
        print(f"LỖI: {str(e)[:50]}...")
    finally:
        if driver:
            driver.quit()

print(f"\n=== HOÀN TẤT! Dữ liệu lưu tại {file_name} ===")
