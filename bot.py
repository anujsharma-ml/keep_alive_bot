import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Dono apps ke URLs
RAG_URL = "https://diabetesbpairagpipeline-egnh5crjjtbher5eczhmwx.streamlit.app/"
CAR_URL = (
    "https://endtoendcarpricepredictionpipeline-rb8enhmfsdb352bflp3n7r.streamlit.app/"  # <-- Yahan apni car price app ka link daal dena
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
        f"[{app_name}] App sleep mode me tha! Wake-up button click kiya ja"
        " raha hai..."
    )
    wake_btn.click()
    print(f"[{app_name}] App wake up hone ka 20 seconds wait ho raha hai...")
    time.sleep(20)
  except Exception:
    print(
        f"[{app_name}] Koi wake-up button nahi mila, app shayad pehle se active"
        " hai."
    )

  # Check if wrapped in iframe
  try:
    iframe = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)
    print(f"[{app_name}] Iframe ke andar switch ho gaye.")
  except Exception:
    driver.switch_to.default_content()
    print(f"[{app_name}] Koi iframe nahi hai, direct page par hain.")


# ==========================================
# PART 1: RAG BOT AUTOMATION
# ==========================================
try:
  wake_up_app_if_needed(RAG_URL, "RAG Bot")

  print("[RAG Bot] Chat input box ko dhoonda ja raha hai...")
  input_box = wait.until(
      EC.presence_of_element_located(
          (By.CSS_SELECTOR, 'div[data-testid="stChatInput"] textarea, textarea')
      )
  )

  print("[RAG Bot] Message type kiya ja raha hai...")
  input_box.click()
  input_box.send_keys("Hello")
  input_box.send_keys(Keys.RETURN)

  time.sleep(10)
  print(
      "[RAG Bot] SUCCESS: Message successfully bhej diya gaya hai aur app active"
      " ho gaya hai."
  )

except Exception as e:
  print(f"[RAG Bot] ERROR: RAG Bot mein error aa gaya -> {e}")
  driver.save_screenshot("rag_error.png")
  print("Screenshot 'rag_error.png' save kar diya gaya hai.")

# ==========================================
# PART 2: CAR PRICE PREDICTOR AUTOMATION
# ==========================================
try:
  wake_up_app_if_needed(CAR_URL, "Car Price App")

  print("[Car Price App] Page load hone ka wait kiya ja raha hai...")
  time.sleep(
      5
  )  # Extra pause taaki car app ke saare widgets/dropdowns properly render ho jayein

  print(
      "[Car Price App] 'Calculate Predicted Price' button ko dhoonda ja raha"
      " hai..."
  )
  # Streamlit ke primary button ya text ke through button dhoondhna
  calc_btn = wait.until(
      EC.element_to_be_clickable((
          By.XPATH,
          "//button[contains(., 'Calculate Predicted Price') or contains(.,'"
          " Price')]",
      ))
  )

  print(
      "[Car Price App] Calculate button mil gaya, click kiya ja raha hai..."
  )
  driver.execute_script(
      "arguments[0].scrollIntoView(true);", calc_btn
  )  # Scroll to button
  calc_btn.click()

  time.sleep(10)
  print(
      "[Car Price App] SUCCESS: Prediction button successfully click ho gaya"
      " hai aur app active ho gaya hai."
  )

except Exception as e:
  print(f"[Car Price App] ERROR: Car Price App mein error aa gaya -> {e}")
  driver.save_screenshot("car_error.png")
  print("Screenshot 'car_error.png' save kar diya gaya hai.")

finally:
  driver.quit()
  print("\n--- Automation Script Finished ---")
