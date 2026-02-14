import subprocess
import os

def check_command(cmd, name):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, None
    except:
        return False, None

def main():
    print("\n--- 🔍 TRANSLATOR SYSTEM CHECK ---")
    uid = os.getuid()
    os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{uid}"

    # 1. Check Virtual Cam
    cam_mod, _ = check_command("lsmod | grep v4l2loopback", "")
    cam_dev, _ = check_command("ls /dev/video0", "")
    if cam_mod and cam_dev:
        print("✅ CAMERA: Virtual Cam is LIVE (/dev/video0)")
    else:
        print("❌ CAMERA: Virtual Cam is DOWN")
        print("   👉 Fix: sudo modprobe v4l2loopback video_nr=0 card_label='PythonCam'")

    # 2. Check Audio Sink
    sink, _ = check_command("pactl list short sinks | grep teams_sink", "")
    if sink:
        print("✅ AUDIO: TeamsSink is ACTIVE")
    else:
        print("❌ AUDIO: TeamsSink is MISSING")
        print("   👉 Fix: pactl load-module module-null-sink sink_name=teams_sink sink_properties=device.description=TeamsSink")

    # 3. Check Bot Process
    bot, _ = check_command("pgrep -f bot.py", "")
    if bot:
        print("✅ BOT: bot.py is RUNNING")
    else:
        print("❌ BOT: bot.py is NOT RUNNING")

    # 4. Check Chromium Routing
    if sink:
        inputs, _ = check_command("pactl list sink-inputs", "")
        if inputs and ("chromium" in inputs.lower() or "chrome" in inputs.lower()):
            if "teams_sink" in inputs:
                print("✅ ROUTING: Bot is correctly hearing TeamsSink")
            else:
                print("⚠️  ROUTING: Bot is playing to WRONG sink (not TeamsSink)")
        else:
            print("❓ ROUTING: No audio activity detected from Bot")

    print("\n--- 📦 ACTIVE PROCESSES ---")
    # Clean process list: just show the main ones
    os.system(f"ps -u {uid} -o pid,comm,args | grep -E 'bot.py|ubuntu_virtual_cam.py|ffmpeg' | grep -v grep")
    
    print("-" * 34 + "\n")

if __name__ == "__main__":
    main()
