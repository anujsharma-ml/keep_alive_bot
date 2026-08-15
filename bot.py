import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Yahan apne live Streamlit app ka URL daal de bhai
STREAMLIT_URL = "https://diabetesbpairagpipeline-egnh5crjjtbher5eczhmwx.streamlit.app/"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
  print("App khul raha hai...")
  driver.get(STREAMLIT_URL)
  time.sleep(12)  # Page load hone ka wait karein

  # Streamlit chat input box ko target karne ke liye
  input_box = driver.find_element(
      By.CSS_SELECTOR, 'textarea[aria-label="Consult MediPulse AI..."]'
  )

  print("Message type kiya ja raha hai...")
  input_box.send_keys("Hello")
  input_box.send_keys(Keys.RETURN)

  time.sleep(5)
  print("Activity successful! App active rahega.")

except Exception as e:
  print(f"Error aa gaya: {e}")

finally:
  driver.quit()
