from playwright.sync_api import sync_playwright
import time
import os

print("=== TEAMS UBUNTU CLICK TEST ===")

# 🔥 REQUIRED ENV FOR UBUNTU
os.environ["DISPLAY"] = ":99"
os.environ["PULSE_SOURCE"] = "teams_sink.monitor"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path="/usr/bin/google-chrome",
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--use-fake-ui-for-media-stream",
            "--autoplay-policy=no-user-gesture-required",
            "--window-size=1920,1080",
        ]
    )

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        permissions=["microphone", "camera"],
        locale="en-US",
    )

    page = context.new_page()

    print("Opening Teams meeting...")
    page.goto(
        "https://teams.live.com/meet/9338034148343?p=c31O7ThP5DfKO00nVc",
        wait_until="domcontentloaded"
    )

    time.sleep(8)  # Teams loads SLOW on Linux

    print("Scanning for buttons...")
    buttons = page.locator(
        'button, [role="button"], input[type="button"], input[type="submit"]'
    ).all()

    print(f"Found {len(buttons)} clickable elements")

    clicked = []

    for i, button in enumerate(buttons):
        try:
            text = (
                button.text_content()
                or button.get_attribute("aria-label")
                or f"Button {i}"
            )

            print(f"Clicking → {text[:60]}")
            button.click(timeout=5000)
            clicked.append(text[:60])
            time.sleep(1)

        except Exception as e:
            print(f"Skipped button {i}: {e}")

    print("\n=== CLICK SUMMARY ===")
    for t in clicked:
        print("-", t)

    print("\nKeeping browser open...")
    time.sleep(300)

    browser.close()
