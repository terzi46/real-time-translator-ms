import os
import subprocess
import sys
import time

def run_command(cmd, env):
    try:
        result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {cmd}")
            return True
        else:
            print(f"❌ Failed: {cmd}")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("--- 🔧 ATTEMPTING AUDIO REPAIR ---")
    
    uid = os.getuid()
    # Potential socket locations for PulseAudio/PipeWire
    candidates = [
        f"/run/user/{uid}/pulse/native",
        f"/run/user/{uid}/pipewire-0",
        f"/tmp/pulse-{uid}/native"
    ]
    
    valid_socket = None
    for socket in candidates:
        if os.path.exists(socket):
            print(f"📍 Found socket: {socket}")
            if "pulse" in socket:
                valid_socket = f"unix:{socket}"
                break
    
    # Prepare environment
    env = os.environ.copy()
    env["XDG_RUNTIME_DIR"] = f"/run/user/{uid}"
    
    if valid_socket:
        print(f"🔌 Connecting to: {valid_socket}")
        env["PULSE_SERVER"] = valid_socket
    else:
        print("⚠️ No standard audio sockets found. Checking if PipeWire is running...")
        subprocess.run("ps -u $(id -u) -f | grep pipewire", shell=True)
        # Try to restart it if missing
        print("🔄 Attempting to restart audio services...")
        subprocess.run("systemctl --user restart pipewire pipewire-pulse wireplumber", shell=True, env=env)
        time.sleep(2)

    # Now try the commands
    print("\n--- 🚀 EXECUTING SETUP COMMANDS ---")
    
    # 1. Check Info first
    if run_command("pactl info", env):
        # 2. Load the Sink
        # Check if it exists first to avoid error
        check = subprocess.run("pactl list short sinks | grep teams_sink", shell=True, env=env, capture_output=True, text=True)
        if "teams_sink" in check.stdout:
             print("✅ teams_sink is ALREADY loaded.")
        else:
             print("➕ Loading teams_sink...")
             run_command("pactl load-module module-null-sink sink_name=teams_sink sink_properties=device.description=TeamsSink", env)
        
        # 3. Set Default Source
        print("🎛️ Setting default source...")
        run_command("pactl set-default-source teams_sink.monitor", env)
    else:
        print("🔥 CRITICAL: Still cannot connect to audio daemon.")
        print("   Please try rebooting the server if this persists.")

if __name__ == "__main__":
    main()
