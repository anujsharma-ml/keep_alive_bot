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
    print("App URL khola ja raha hai...")
    driver.get(STREAMLIT_URL)
    
    wait = WebDriverWait(driver, 30)
    
    # STEP 1: Check for Streamlit "Wake up" / "Get this app back up" button
    try:
        print("Checking if app is sleeping / looking for wake-up button...")
        # Streamlit ka specific wake-up button text ya xpath
        wake_btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'back up') or contains(., 'Wake up') or contains(., 'Yes')]"))
        )
        print("App sleep mode me tha! Wake-up button click kiya ja raha hai...")
        wake_btn.click()
        
        # App ke uthne ke liye thoda lamba wait dena zaroori hai
        print("App wake up hone ka 20 seconds wait ho raha hai...")
        time.sleep(20)
    except Exception:
        print("Koi wake-up button nahi mila, app shayad pehle se active hai.")

    # STEP 2: Streamlit Cloud ke main container ya iframe me switch karna
    print("Streamlit container load hone ka wait kiya ja raha hai...")
    try:
        # Check if wrapped in iframe
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        print("Iframe ke andar switch ho gaye.")
    except Exception:
        print("Koi iframe nahi hai, direct page par hain.")

    # STEP 3: Chat input box ko dhoondhna aur message type karna
    print("Chat input box ko dhoonda ja raha hai...")
    input_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="stChatInput"] textarea, textarea'))
    )

    print("Message type kiya ja raha hai...")
    input_box.click()
    input_box.send_keys("Hello")
    input_box.send_keys(Keys.RETURN)

    # Response process hone ke liye wait
    time.sleep(10)
    print("Activity successful! Message successfully bhej diya gaya hai aur app active ho gaya hai.")

except Exception as e:
    print(f"Error aa gaya: {e}")
    driver.save_screenshot("streamlit_error.png")
    print("Screenshot 'streamlit_error.png' save kar diya gaya hai.")
    raise e

finally:
    driver.quit()
