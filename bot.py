import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Yahan apne live Streamlit app ka URL daal de bhai
STREAMLIT_URL = "https://diabetesbpairagpipeline-egnh5crjjtbher5eczhmwx.streamlit.app/"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Headless mode me kabhi-kabhi screen resolution issue se bhi element chup jata hai, isliye size fix kar sakte hain:
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    print("App khul raha hai...")
    driver.get(STREAMLIT_URL)
    
    # Streamlit load hone ke liye WebDriverWait ka use karein (upto 25 seconds)
    print("Chat input box ke load hone ka wait kiya ja raha hai...")
    wait = WebDriverWait(driver, 25)
    
    # Streamlit ka standard chat input textarea selector
    input_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="stChatInput"] textarea'))
    )

    print("Message type kiya ja raha hai...")
    input_box.click()
    input_box.send_keys("Hello")
    input_box.send_keys(Keys.RETURN)

    # Response aane aur request process hone ke liye thoda wait
    time.sleep(8)
    print("Activity successful! App active rahega aur message bhej diya gaya hai.")

except Exception as e:
    print(f"Error aa gaya: {e}")

finally:
    driver.quit()
