import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URLs for both apps
RAG_URL = "https://diabetesbpairagpipeline-egnh5crjjtbher5eczhmwx.streamlit.app/"
CAR_URL = (
    "YOUR_CAR_PRICE_STREAMLIT_URL_HERE"  # <-- Replace with your Car Price app link
)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)


# --- FUNCTION TO HANDLE APP WAKE-UP ---
def wake_up_app_if_needed(url, app_name):
  print(f"\n--- Checking {app_name} ---")
  print(f"Opening URL: {url}")
  driver.get(url)

  try:
    print(f"[{app_name}] Checking for sleep / wake-up button...")
    wake_btn = WebDriverWait(driver, 8).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(., 'back up') or contains(., 'Wake up') or"
            " contains(., 'Yes')]",
        ))
    )
    print(
        f"[{app_name}] App was in sleep mode! Clicking wake-up button..."
    )
    wake_btn.click()
    print(f"[{app_name}] Waiting 20 seconds for the app to wake up...")
    time.sleep(20)
  except Exception:
    print(f"[{app_name}] No wake-up button found, app is likely already active.")

  # Check if wrapped in iframe
  try:
    iframe = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)
    print(f"[{app_name}] Switched inside iframe.")
  except Exception:
    driver.switch_to.default_content()
    print(f"[{app_name}] No iframe found, on direct page.")


# ==========================================
# PART 1: RAG BOT AUTOMATION
# ==========================================
try:
  wake_up_app_if_needed(RAG_URL, "RAG Bot")

  print("[RAG Bot] Searching for chat input box...")
  input_box = wait.until(
      EC.presence_of_element_located(
          (By.CSS_SELECTOR, 'div[data-testid="stChatInput"] textarea, textarea')
      )
  )

  print("[RAG Bot] Typing message and sending...")
  input_box.click()
  input_box.send_keys("Hello")
  input_box.send_keys(Keys.RETURN)

  time.sleep(10)
  print(
      "[RAG Bot] SUCCESS: Message sent successfully and app is now active."
  )

except Exception as e:
  print(f"[RAG Bot] ERROR: An error occurred in RAG Bot -> {e}")
  driver.save_screenshot("rag_error.png")
  print("Screenshot 'rag_error.png' saved successfully.")

# ==========================================
# PART 2: CAR PRICE PREDICTOR AUTOMATION
# ==========================================
try:
  wake_up_app_if_needed(CAR_URL, "Car Price App")

  print("[Car Price App] Waiting for page components to load...")
  time.sleep(5)  # Pause to ensure all car app widgets render properly

  print("[Car Price App] Searching for 'Calculate Predicted Price' button...")
  calc_btn = wait.until(
      EC.element_to_be_clickable((
          By.XPATH,
          "//button[contains(., 'Calculate Predicted Price') or contains(.,'"
          " Price')]",
      ))
  )

  print("[Car Price App] Calculate button found, clicking...")
  driver.execute_script("arguments[0].scrollIntoView(true);", calc_btn)
  calc_btn.click()

  time.sleep(10)
  print(
      "[Car Price App] SUCCESS: Prediction button clicked successfully and app"
      " is now active."
  )

except Exception as e:
  print(f"[Car Price App] ERROR: An error occurred in Car Price App -> {e}")
  driver.save_screenshot("car_error.png")
  print("Screenshot 'car_error.png' saved successfully.")

finally:
  driver.quit()
  print("\n--- Automation Script Finished ---")
