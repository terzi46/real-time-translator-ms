import time
import subprocess
import os
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
TEAMS_URL = "https://teams.live.com/meet/9365513283443?p=CaQ10Tq5rovvmoQ8Ur"
AUDIO_FILE = "response.wav"
SINK_NAME = "teams_sink"

def play_audio_to_teams(file_path):
    try:
        print(f"🔊 Injecting {file_path} into {SINK_NAME}...")
        # Use pw-play to inject audio into the null sink
        subprocess.run(["pw-play", "--target", SINK_NAME, file_path], check=True)
        print("✅ Playback finished.")
    except Exception as e:
        print(f"❌ Audio Injection Error: {e}")

def main():
    print(f"🚀 Starting bot on DISPLAY {os.getenv('DISPLAY', 'NOT SET')}")
    
    with sync_playwright() as p:
        # Launching with headless=False so we can see it on the VMware console
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
            ]
        )
        
        # Grant microphone and camera permissions
        context = browser.new_context(
            permissions=['microphone', 'camera'],
            viewport={'width': 1280, 'height': 720}
        )
        
        page = context.new_page()

        print(f"🔗 Navigating to Teams: {TEAMS_URL}")
        page.goto(TEAMS_URL)

        # Basic wait for the page to load
        time.sleep(10)

        # Try to enter a name and click "Join now"
        try:
            print("🔍 Looking for name input field...")
            # Common selectors for the Teams name input
            name_input = page.locator('input[placeholder="Type your name"], #prejoin-display-name, [data-tid="prejoin-display-name-input"]')
            
            if name_input.is_visible(timeout=15000):
                print("📝 Entering name: translator")
                name_input.fill("translator")
                time.sleep(1) # Small delay to ensure input is registered
            
            print("🔍 Looking for 'Join now' button...")
            join_button = page.locator('button:has-text("Join now"), [data-tid="prejoin-join-button"]')
            if join_button.is_visible(timeout=10000):
                print("✅ Found 'Join now' button. Clicking...")
                join_button.click()
            else:
                print("⚠️ 'Join now' button not found within timeout. Please join manually on the VMware screen.")
        except Exception as e:
            print(f"ℹ️ Auto-join note: {e}")

        print("------------------------------------------------")
        print("🤖 BOT IS LIVE")
        print("1. Ensure 'PythonCam' is selected in Teams Video settings.")
        print("2. Ensure 'TeamsSink' (Monitor) is the system default mic.")
        print("------------------------------------------------")

        print("Waiting for manual interactions or further automation...")
        
        # Keep the script running and allow manual audio injection
        while True:
            try:
                cmd = input("\n🟢 Press ENTER to inject 'response.wav' (or 'exit'): ")
                if cmd.lower() == 'exit':
                    break
                if os.path.exists(AUDIO_FILE):
                    play_audio_to_teams(AUDIO_FILE)
                else:
                    print(f"⚠️ {AUDIO_FILE} not found!")
            except EOFError:
                break

        browser.close()

if __name__ == "__main__":
    main()
