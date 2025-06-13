from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# =======================
# ORTAK YARDIMCI FONKSİYONLAR
# =======================

def setup_driver(mobile=False):
    options = webdriver.ChromeOptions()
    if mobile:
        options.add_argument("--window-size=480,800")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def open_website(driver, url, wait_time=2):
    driver.get(url)
    time.sleep(wait_time)

def scroll_half_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)

def quit_driver(driver):
    driver.quit()

# =======================
# TEST 1: Sayfa Başlığı Kontrolü
# =======================

def test_title_check():
    print("\n[Test 1] Sayfa başlığı kontrolü")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/")
        actual_title = driver.title
        expected_title = "Restful-booker-platform demo"
        if actual_title == expected_title:
            print("TEST PASS — Sayfa başlığı beklenenle eşleşiyor.")
        else:
            print("TEST FAIL — Sayfa başlığı beklenenle eşleşmiyor.")
            print(f"Beklenen: '{expected_title}' — Gerçekleşen: '{actual_title}'")
    finally:
        quit_driver(driver)

# =======================
# TEST 2: Geçersiz Telefon Numarası ile Form Hata Kontrolü
# =======================

def test_invalid_phone_input():
    print("\n[Test 2] Geçersiz telefon numarası kontrolü")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/")
        scroll_half_page(driver)
        driver.find_element(By.ID, "name").send_keys("Ali")
        driver.find_element(By.ID, "email").send_keys("ali@example.com")
        driver.find_element(By.ID, "phone").send_keys("abc123")
        driver.find_element(By.ID, "subject").send_keys("Geçersiz Telefon Testi")
        driver.find_element(By.ID, "description").send_keys("Bu test geçersiz telefon numarası içindir.")
        submit_btn = driver.find_element(By.XPATH, '//button[text()="Submit"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        submit_btn.click()
        time.sleep(1)
        error_elements = driver.find_elements(By.CLASS_NAME, "alert-danger")
        if any("phone" in e.text.lower() for e in error_elements):
            print("TEST PASS — Telefon hatası başarılı şekilde algılandı.")
        else:
            print("TEST FAIL — Geçersiz telefon için uyarı mesajı görünmedi.")
    finally:
        quit_driver(driver)

# =======================
# TEST 3: E-posta Boş Bırakıldığında Uyarı
# =======================

def test_empty_email_field_warning():
    print("\n[Test 3] E-posta boş bırakıldığında uyarı kontrolü")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/")
        scroll_half_page(driver)
        driver.find_element(By.ID, "name").send_keys("Özgür")
        driver.find_element(By.ID, "phone").send_keys("55512345678")
        driver.find_element(By.ID, "subject").send_keys("Zorunlu Alan Testi")
        driver.find_element(By.ID, "description").send_keys("E-posta boş bırakılacak.")
        submit_btn = driver.find_element(By.XPATH, '//button[text()="Submit"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        submit_btn.click()
        time.sleep(1)
        error_elements = driver.find_elements(By.CLASS_NAME, "alert-danger")
        if any("email may not be blank" in e.text.lower() for e in error_elements):
            print("TEST PASS — E-posta boş bırakıldığında uyarı gösterildi.")
        else:
            print("TEST FAIL — Uyarı mesajı bulunamadı.")
    finally:
        quit_driver(driver)

# =======================
# TEST 4: Çok Uzun Mesaj Uyarısı
# =======================

def test_very_long_message_warning():
    print("\n[Test 4] Çok uzun mesaj gönderildiğinde uyarı kontrolü")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/")
        scroll_half_page(driver)
        long_msg = "a" * 2100
        driver.find_element(By.ID, "name").send_keys("Özgür")
        driver.find_element(By.ID, "email").send_keys("ozgur@example.com")
        driver.find_element(By.ID, "phone").send_keys("55512345678")
        driver.find_element(By.ID, "subject").send_keys("Uzun Mesaj")
        driver.find_element(By.ID, "description").send_keys(long_msg)
        submit_btn = driver.find_element(By.XPATH, '//button[text()="Submit"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        submit_btn.click()
        time.sleep(1)
        error_elements = driver.find_elements(By.CLASS_NAME, "alert-danger")
        if any("message must be between 20 and 2000 characters" in e.text.lower() for e in error_elements):
            print("TEST PASS — Uzun mesaj için doğru uyarı verildi.")
        else:
            print("TEST FAIL — Uzun mesaj gönderildi ama uyarı çıkmadı.")
    finally:
        quit_driver(driver)

# =======================
# TEST 5: Admin Paneli Giriş Formu Görünürlük
# =======================

def test_admin_login_form_visibility():
    print("\n[Test 5] Admin login formu görünürlük testi")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/admin", wait_time=0)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))
        driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[name='username']")
        driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        print("TEST PASS — Login formu görünür.")
    except Exception as e:
        print("TEST FAIL — Admin panel login formu görünmedi.")
        print(f"Hata Detayı: {e}")
    finally:
        quit_driver(driver)

# =======================
# TEST 6: Yanlış Admin Giriş Bilgileri
# =======================

def test_invalid_admin_login():
    print("\n[Test 6] Yanlış admin bilgileriyle giriş denemesi")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/admin", wait_time=0)
        wait = WebDriverWait(driver, 10)
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[name='username']")))
        password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        username.send_keys("wronguser")
        password.send_keys("wrongpass")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        time.sleep(2)
        error_elements = driver.find_elements(By.CLASS_NAME, "alert-danger")
        if error_elements:
            print("TEST PASS — Hatalı bilgilerle giriş reddedildi.")
            print("Hata Mesajı:", error_elements[0].text.strip())
        else:
            print("TEST FAIL — Hatalı girişte uyarı mesajı çıkmadı.")
    finally:
        quit_driver(driver)

# =======================
# TEST 7: Doğru Admin Bilgileriyle Giriş
# =======================

def test_valid_admin_login():
    print("\n[Test 7] Geçerli admin girişi testi")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/admin", wait_time=0)
        wait = WebDriverWait(driver, 10)
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[name='username']")))
        password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        username.send_keys("admin")
        password.send_keys("password")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        time.sleep(3)
        page_source = driver.page_source
        keywords = ["Rooms", "Logout", "Add Room", "roomName"]
        if any(kw in page_source for kw in keywords):
            print("TEST PASS — Admin olarak giriş yapıldı, panel erişimi başarılı.")
        else:
            print("TEST FAIL — Panel içerikleri görünmedi.")
    except Exception as e:
        print(f"TEST ERROR — Giriş sırasında hata oluştu: {e}")
    finally:
        quit_driver(driver)

# =======================
# TEST 8: Formu Tamamen Boş Gönderme
# =======================

def test_empty_form_submission():
    print("\n[Part 2] Form tamamen boş gönderildiğinde hata mesajı kontrolü")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get("https://automationintesting.online/")
        wait = WebDriverWait(driver, 10)

        # Sayfayı aşağı kaydır
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)

        # Formu boş gönderiyoruz
        submit_btn = driver.find_element(By.XPATH, '//button[text()="Submit"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        submit_btn.click()

        # Hata mesajlarını al
        time.sleep(1)
        error_elements = driver.find_elements(By.CLASS_NAME, "alert-danger")

        # Hata mesajlarını yazdır
        if error_elements:
            print("TEST PASS — Form boş gönderildi, hata mesajları başarıyla alındı:")
            for i, error in enumerate(error_elements, 1):
                print(f"{i}. {error.text}")
        else:
            print("TEST FAIL — Form boş gönderildi ama hata mesajı gösterilmedi!")
    finally:
        driver.quit()

# =======================
# TEST 9: Rooms ve Contact Linkleri
# =======================

def test_rooms_and_contact():
    print("\n[Test 9] Rooms ve Contact linkleri testi")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/")
        wait = WebDriverWait(driver, 10)
        rooms_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Rooms")))
        rooms_link.click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.ID, "rooms")))
        print("TEST PASS — 'Rooms' bağlantısı çalıştı, 'Rooms' bölümü göründü.")

        contact_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Contact")))
        driver.execute_script("arguments[0].scrollIntoView(true);", contact_link)
        time.sleep(3)
        contact_link.click()
        time.sleep(3)
        inputs = ["name", "email", "phone", "subject", "description"]
        all_found = all(wait.until(EC.visibility_of_element_located((By.ID, i))) for i in inputs)
        if all_found:
            print("TEST PASS — 'Contact' bağlantısı çalıştı, iletişim formu bulundu.")
        else:
            print("TEST FAIL — 'Contact' bağlantısı çalıştı ama iletişim formu eksik.")
    except Exception as e:
        print("TEST FAIL — Rooms veya Contact testi sırasında hata oluştu.")
        print(f"Hata Detayı: {e}")
    finally:
        quit_driver(driver)

# =======================
# TEST 10: Mobil Menü
# =======================

def test_mobile_menu_display():
    print("\n[Test 10] Mobil görünümde hamburger menü testi")
    driver = setup_driver(mobile=True)
    try:
        open_website(driver, "https://automationintesting.online/", wait_time=1)
        wait = WebDriverWait(driver, 10)
        menu_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "navbar-toggler")))
        menu_button.click()
        menu_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "navbar-collapse")))
        if menu_links.is_displayed():
            print("TEST PASS — Mobil görünümde hamburger menü başarıyla açıldı.")
        else:
            print("TEST FAIL — Menü görünmedi, responsive tasarım hatası olabilir.")
    except Exception as e:
        print("TEST ERROR — Menü testi sırasında hata oluştu.")
        print("Hata Detayı:", str(e))
    finally:
        quit_driver(driver)

# =======================
# TEST 11: 404 Sayfası
# =======================

def test_404_page_display():
    print("\n[Test 11] Hatalı URL için 404 sayfa testi")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/nonexistentpage", wait_time=1)
        wait = WebDriverWait(driver, 10)
        error_heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        if "404" in error_heading.text or "not found" in error_heading.text.lower():
            print("TEST PASS — Hatalı URL için 404 sayfası başarıyla görüntülendi.")
        else:
            print("TEST FAIL — 404 sayfası bekleniyordu ama farklı içerik bulundu.")
    except Exception as e:
        print("TEST ERROR — 404 testi sırasında hata oluştu.")
        print("Hata Detayı:", str(e))
    finally:
        quit_driver(driver)

# # =======================
# # TEST 12: Oda Mevcutluğu ve Yönlendirme Testi
# # =======================


def test_room_availability():
    print("\n[Room Availability Test]")
    driver = setup_driver()
    try:
        open_website(driver, "https://automationintesting.online/#booking", wait_time=1)
        wait = WebDriverWait(driver, 10)

        check_availability = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Check Availability']")))

        check_availability.click()

        time.sleep(3)  # Sonuçların yüklenmesi için bekleme
        rooms = driver.find_elements(By.CLASS_NAME, "room-card")
        
        if rooms and len(rooms) > 0:
            print("TEST PASS — Uygun odalar listelendi.")
            # İlk "Book Now" butonuna tıklayın
            book_now = rooms[0].find_element(By.LINK_TEXT, "Book now")
            driver.execute_script("arguments[0].scrollIntoView(true);", book_now)
            book_now.click()

            time.sleep(3)  # Yönlendirme sonrası bekleme
            current_url = driver.current_url
            if "reservation" in current_url:
                print("TEST PASS — Yönlendirme başarılı.")
            else:
                print("TEST FAIL — Yönlendirme yapılamadı.")
        else:
            print("TEST FAIL — Uygun oda bulunamadı.")
    finally:
        quit_driver(driver)







# =======================
# MAIN
# =======================

def main():
    test_title_check() #1
    test_invalid_phone_input() #2
    test_empty_email_field_warning() #3
    test_very_long_message_warning() #4
    test_admin_login_form_visibility() #5
    test_invalid_admin_login() #6
    test_empty_form_submission()  # 8
    test_valid_admin_login() #7
    test_rooms_and_contact() #9
    test_mobile_menu_display() #10
    test_404_page_display() #11
    test_room_availability() #12

if __name__ == "__main__":
    main()
