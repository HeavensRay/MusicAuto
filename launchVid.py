from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os

from urllib.parse import urlparse, parse_qs
import time


driver = None

# === Config ===
msedgedriver_path = os.path.dirname(__file__) +"\\webDriver\\msedgedriver.exe"

# === URL Cleanup ===
def clean_youtube_url(url):
    parsed = urlparse(url)
    v = parse_qs(parsed.query).get('v', [''])[0]
    return f"https://www.youtube.com/watch?v={v}" if v else None

def simplify_url(url):
    v = parse_qs(urlparse(url).query).get("v", [""])[0]
    return v

# === Edge Options (Stealth + InPrivate) ===
options = Options()
options.add_argument("--inprivate")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-features=EdgeSegmentationPlatform")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-client-side-phishing-detection")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-sync")
options.add_argument('--log-level=3') 


service = Service(msedgedriver_path)


def create_driver():
    driver = webdriver.Edge(service=service, options=options)
    
    return driver

def is_driver_alive(driver):
    try:
        _ = driver.current_url
        return True
    except:
        return False

# === Ad Skipping & Muting ===
def handle_ads(driver):
    
        driver.execute_script("""
            const player = document.getElementById('movie_player');
            if (player && player.classList.contains('ad-showing')) {
                const video = document.querySelector('video');
                if (video && !video.muted) video.muted = true;
            }
        """)
    

# === Watch Until End or Change ===
def wait_for_video_end_or_change(driver, timeout=600):
    end_time = time.time() + timeout

    while time.time() < end_time:   
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

    print("⏰ Timeout waiting for video to end.")
    return "timeout"

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
    return 200

def close_window():
    print("Session ended 🎬")
    if driver is not None:
        driver.close()