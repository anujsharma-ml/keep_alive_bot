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
    
    wait = WebDriverWait(driver, 45)
    
    # Step 1: Streamlit Cloud ke iframe me switch karna zaroori hai
    print("Streamlit Cloud iframe ko dhoonda ja raha hai...")
    try:
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
        driver.switch_to.frame(iframe)
        print("Successfully iframe ke andar switch ho gaye!")
    except Exception as e:
        print(f"Iframe nahi mila ya direct page hai: {e}")

    # Step 2: Agar app sleep me hai toh wake-up button click karein
    try:
        wake_up_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'back up') or contains(., 'Wake up') or contains(., 'Yes')]"))
        )
        print("Wake-up button mil gaya, click kiya ja raha hai...")
        wake_up_button.click()
        time.sleep(15)
    except Exception:
        print("Koi wake-up button nahi mila.")

    # Step 3: Chat input box ko dhoondna (Ab ye iframe ke andar asani se mil jayega)
    print("Chat input box ko dhoonda ja raha hai...")
    input_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea'))
    )

    print("Message type kiya ja raha hai...")
    input_box.click()
    input_box.send_keys("Hello")
    input_box.send_keys(Keys.RETURN)

    # Response process hone ke liye wait
    time.sleep(10)
    print("Activity successful! Chat box me message bhej diya gaya hai.")

except Exception as e:
    print(f"Error aa gaya: {e}")
    driver.save_screenshot("streamlit_error.png")
    print("Screenshot 'streamlit_error.png' save ho gaya hai.")
    raise e

finally:
    driver.quit()
