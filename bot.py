import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

RAG_URL = "https://diabetesbpairagpipeline-egnh5crjjtbher5eczhmwx.streamlit.app/"
CAR_URL = "https://endtoendcarpricepredictionpipeline-rb8enhmfsdb352bflp3n7r.streamlit.app/"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
# Crucial: Avoid detection by setting a standard desktop browser User-Agent
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)

def handle_streamlit_iframe():
    """Switches to Streamlit iframe if present, otherwise stays in root."""
    driver.switch_to.default_content()
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        print("Switched inside Streamlit iframe.")
    except Exception:
        print("No iframe detected, working on default content.")

def wake_up_app_if_needed(url, app_name):
    print(f"\n--- Checking {app_name} ---")
    print(f"Opening URL: {url}")
    driver.get(url)
    time.sleep(5)  # Allow initial page bundle to load

    # Handle iframe first if Streamlit wraps the app
    handle_streamlit_iframe()

    # Look for Streamlit's official wake-up button or text selector
    try:
        print(f"[{app_name}] Checking for sleep / wake-up button...")
        wake_btn = WebDriverWait(driver, 12).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'wake') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'back up') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'yes')]"
            ))
        )
        print(f"[{app_name}] App was sleeping! Clicking wake-up button...")
        driver.execute_script("arguments[0].click();", wake_btn)
        print(f"[{app_name}] Waiting 25 seconds for initial app boot...")
        time.sleep(25)
    except Exception:
        print(f"[{app_name}] No wake-up button found or app already awake.")

# ==========================================
# PART 1: RAG BOT AUTOMATION
# ==========================================
try:
    wake_up_app_if_needed(RAG_URL, "RAG Bot")

    # Re-verify iframe state in case page refreshed after wake-up
    handle_streamlit_iframe()

    print("[RAG Bot] Searching for chat input box...")
    input_box = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea[data-testid="stChatInputTextArea"], textarea')
        )
    )

    print("[RAG Bot] Typing message and sending...")
    input_box.click()
    input_box.send_keys("Hello")
    input_box.send_keys(Keys.RETURN)

    time.sleep(10)
    print("[RAG Bot] SUCCESS: Message sent successfully.")

except Exception as e:
    print(f"[RAG Bot] ERROR: {e}")
    driver.save_screenshot("rag_error.png")
    print("Saved 'rag_error.png'")

# ==========================================
# PART 2: CAR PRICE PREDICTOR AUTOMATION
# ==========================================
try:
    wake_up_app_if_needed(CAR_URL, "Car Price App")

    handle_streamlit_iframe()

    print("[Car Price App] Searching for button...")
    calc_btn = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//button[contains(., 'Calculate') or contains(., 'Price') or @data-testid='baseButton-secondary']"
        ))
    )

    print("[Car Price App] Clicking action button...")
    driver.execute_script("arguments[0].scrollIntoView(true);", calc_btn)
    driver.execute_script("arguments[0].click();", calc_btn)

    time.sleep(10)
    print("[Car Price App] SUCCESS: Action triggered.")

except Exception as e:
    print(f"[Car Price App] ERROR: {e}")
    driver.save_screenshot("car_error.png")
    print("Saved 'car_error.png'")

finally:
    driver.quit()
    print("\n--- Automation Script Finished ---")
