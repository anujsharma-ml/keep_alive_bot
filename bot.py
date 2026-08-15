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
    
    # Streamlit cold start ke liye lamba wait (45 seconds)
    print("App ke fully load hone ka wait kiya ja raha hai (45s max)...")
    wait = WebDriverWait(driver, 45)
    
    # Step 1: Pehle check karein ki kya koi 'Wake up' button hai
    try:
        wake_up_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'back up') or contains(., 'Wake up') or contains(., 'Yes')]"))
        )
        print("Wake-up button mil gaya, click kiya ja raha hai...")
        wake_up_button.click()
        time.sleep(15) # Wake up hone ke baad extra wait
    except Exception:
        print("Koi wake-up button nahi mila, aage badh rahe hain.")

    # Step 2: Chat input box ke render hone ka wait karein
    print("Chat input box ko dhoonda ja raha hai...")
    input_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="stChatInput"] textarea'))
    )

    print("Message type kiya ja raha hai...")
    input_box.click()
    input_box.send_keys("Hello")
    input_box.send_keys(Keys.RETURN)

    # Response process hone ke liye wait
    time.sleep(10)
    print("Activity successful! App active ho gaya hai.")

except Exception as e:
    print(f"Error aa gaya: {e}")
    # Debugging ke liye screenshot save kar lein taaki GitHub Actions me dikh sake
    driver.save_screenshot("streamlit_error.png")
    print("Screenshot 'streamlit_error.png' save kar diya gaya hai.")
    raise e

finally:
    driver.quit()
