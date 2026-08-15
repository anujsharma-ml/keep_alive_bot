import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

STREAMLIT_URL = "https://diabetesbpairagpipeline-egnh5crjjtbher5eczhmwx.streamlit.app/"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    print("App khul raha hai...")
    driver.get(STREAMLIT_URL)
    
    wait = WebDriverWait(driver, 15)
    
    # Step 1: Check karein ki kya Streamlit ka 'Wake up' / Sleep screen aaya hai
    try:
        print("Checking for Streamlit sleep/wake-up screen...")
        # Streamlit sleep page par 'Yes, get this app back up!' ya similar button hota hai
        wake_up_button = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'back up') or contains(., 'Wake up') or contains(., 'Yes')]"))
        )
        print("App sleep mode me tha, wake-up button click kiya ja raha hai...")
        wake_up_button.click()
        
        # App ke poori tarah uthne ke liye thoda wait karein
        print("App ke wake up hone ka wait ho raha hai...")
        time.sleep(15)
    except Exception:
        print("Koi sleep screen nahi mili, app already active ho sakta hai.")

    # Step 2: Ab chat input box ke load hone ka wait karein
    print("Chat input box ke load hone ka wait kiya ja raha hai...")
    input_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="stChatInput"] textarea'))
    )

    print("Message type kiya ja raha hai...")
    input_box.click()
    input_box.send_keys("Hello")
    input_box.send_keys(Keys.RETURN)

    time.sleep(8)
    print("Activity successful! App active rahega.")

except Exception as e:
    print(f"Error aa gaya: {e}")

finally:
    driver.quit()
