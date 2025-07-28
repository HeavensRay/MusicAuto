from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import time
import os

driver = None

# === Config ===
base_dir = os.path.dirname("..\\MusicAuto")

# Paths to Chrome for Testing and ChromeDriver in your project folder
chrome_binary_path = os.path.join(base_dir, "chrome-win64", "chrome.exe")
driver_path = os.path.join(base_dir, "chromedriver-win64", "chromedriver.exe") 



# === Chrome Options (Stealth + Incognito) ===
options = Options()
options.binary_location = chrome_binary_path
options.add_argument("--incognito")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-background-networking")
options.add_argument("--disable-client-side-phishing-detection")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-sync")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-extensions")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-sync")
options.add_argument("--disable-translate")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# === URL Cleanup ===
def clean_youtube_url(url):
    parsed = urlparse(url)
    v = parse_qs(parsed.query).get('v', [''])[0]
    return f"https://www.youtube.com/watch?v={v}" if v else None

def simplify_url(url):
    v = parse_qs(urlparse(url).query).get("v", [""])[0]
    return v
# === Stealth Script ===
stealth_script = """
  Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  window.navigator.chrome = { runtime: {} };
  Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3] });
  Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] });
"""

def create_driver():
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth_script})
    return driver

def is_driver_alive(driver):
    try:
        _ = driver.current_url
        return True
    except:
        return False

# === Ad Skipping & Muting ===
def handle_ads(driver):
    try:
        driver.execute_script("""
            const player = document.getElementById('movie_player');
            if (player && player.classList.contains('ad-showing')) {
                const video = document.querySelector('video');
                if (video && !video.muted) video.muted = true;
            }
        """)
        skipped = driver.execute_script("""
            const btn = document.querySelector('.ytp-ad-skip-button, .ytp-ad-overlay-close-button');
            if (btn) { btn.click(); return true; }
            return false;
        """)
        if skipped:
            print("⏩ Skipped an ad.")
    except:
        pass

# === Watch Until End or Change ===
def wait_for_video_end_or_change(driver):
    

    while True:
        try:
            handle_ads(driver)
            state = driver.execute_script("""
                const player = document.getElementById('movie_player');
                return player ? player.getPlayerState() : null;
            """)
            # 0 = ended
            if state == 0:
                print("✅ Video ended.")
                return "ended"
        except Exception:
            print("💻🔧 Browser manually manipulated")
            return

        time.sleep(1)

from selenium.webdriver.common.action_chains import ActionChains

def hover_over_video(driver):
    video_element = driver.find_element(By.CSS_SELECTOR, "video")
    actions = ActionChains(driver)
    actions.move_to_element(video_element).perform()

# === Main Runner ===
def run_video_watcher(url):
    clean_url = clean_youtube_url(url)
    global driver

    if driver is None or not is_driver_alive(driver):
        print("🚀 Launching new browser...")
        driver = create_driver()
    else:
        print("🟢 Reusing browser session.")

    if not clean_url:
        print("❌ Invalid URL")
        return "error"

    print(f"▶️ Loading video: {clean_url}")
    driver.get(clean_url)

    wait_for_video_end_or_change(driver)

    print("✅ Song ended")
    return 200
