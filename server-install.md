# Project Progress: 🟢 Environment Ready, 🟡 Bot Automation in Progress

## Way of Working
- **Teamwork**: User is the "hands and eyes" (executes commands, checks physical screen). Agent is the "brain" (analyzes, plans, writes code).
- **Consent First**: Before the agent changes any code or configuration, it MUST always ask the user for confirmation first.
- **Incremental Progress**: We document every step and current status here in `server-install.md`.

## User Setup & Permissions
- User `hilmi` has been granted `sudo` access.
- Project is located at `/home/hilmi/real-time-translator-ms`.
- **Note**: The environment must be strictly `hilmi`. If `HOME` or `USER` variables point to `/root`, Playwright will fail due to permission issues.

## Daily Startup Procedure (Order is Important)

1. **VMware Console**: Log in as `hilmi` and run `startx`. Keep this screen open. Run `xhost +local:` in the terminal there.
2. **SSH Terminal 1 (Virtual Cam)**:
   ```bash
   cd ~/real-time-translator-ms
   source venv/bin/activate
   sudo modprobe v4l2loopback video_nr=0 card_label="PythonCam"
   python3 ubuntu_virtual_cam.py
   ```
3. **SSH Terminal 2 (Audio Sink & Silence)**:
   ```bash
   # Check if sink already exists, if not, load it
   if ! pactl list short sinks | grep -q "teams_sink"; then
     pactl load-module module-null-sink sink_name=teams_sink sink_properties=device.description=TeamsSink
   fi
   
   # Keep sink alive
   pw-play silence.wav --target=teams_sink &
   
   # Set as default source for Chrome
   pactl set-default-source teams_sink.monitor
   ```
4. **SSH Terminal 3 (The Bot)**:
   ```bash
   cd ~/real-time-translator-ms
   source venv/bin/activate
   # Critical Environment Fixes
   export HOME=/home/hilmi
   export PLAYWRIGHT_BROWSERS_PATH=/home/hilmi/.cache/ms-playwright
   export DISPLAY=:0
   export PULSE_SOURCE=teams_sink.monitor
   
   python3 bot.py
   ```

## Verification & Status

To verify if everything is working correctly without guessing, run the following command in any terminal:
```bash
cd ~/real-time-translator-ms
python3 check_status.py
```

### What to look for in the output:
- **v4l2loopback**: Must be ACTIVE (This is your camera).
- **Teams Audio Sink**: Must be ACTIVE (This is where the bot "hears" and "speaks").
- **Chromium connection**: Should show "correctly routed to TeamsSink".

## Troubleshooting
- **ModuleNotFoundError: No module named 'playwright'**: Ensure `source venv/bin/activate` is run.
- **BrowserType.launch: Executable doesn't exist**: Ensure `PLAYWRIGHT_BROWSERS_PATH` is exported and `playwright install chromium` was run by the `hilmi` user.
- **Permission Denied (mkdir /root/.cache)**: This happens if `HOME` is set to `/root`. Always use `export HOME=/home/hilmi`.
