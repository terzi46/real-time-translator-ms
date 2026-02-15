
🔹 Scaling Model

If you want 5 meeting bots:

Create:

bot1

bot2

bot3

bot4

bot5

Each with:

Separate home directory

Separate audio graph

Separate DISPLAY number

Separate Playwright process

They are isolated at OS level.




sudo apt update && sudo apt upgrade -y


sudo apt install -y \
  pipewire \
  pipewire-pulse \
  wireplumber \
  ffmpeg \
  xvfb \
  helvum \
  python3 \
  python3-venv \
  python3-pip \
  wget \
  curl \
  libnss3 \
  libatk-bridge2.0-0t64 \
  libxss1 \
  libasound2t64 \
  libgbm1 \
  libgtk-3-0t64 \
  libdrm2 \
  libxkbcommon0 \
  libatspi2.0-0t64

sudo apt install -y pulseaudio-utils

sudo useradd -m -s /bin/bash bot1
sudo useradd -m -s /bin/bash bot2
sudo passwd bot1
sudo passwd bot2

sudo loginctl enable-linger bot1
sudo loginctl enable-linger bot2

STOP THERE.

Do NOT start pipewire from root.

✅ Phase 2 — Per User Initialization

For each bot you'll have to sign in once so the PAM creates systemd user, dbus, xds runtime dir:

ssh bot1@192.168.184.128


Then inside that shell:

systemctl --user enable pipewire pipewire-pulse wireplumber
systemctl --user start pipewire pipewire-pulse wireplumber


Exit.

Repeat for bot2. (ssh bot2@192.168.184.128)



pactl info | grep "Server Name"

pactl info | grep "Server Name"

RESULT MUST BE:
Server Name: PulseAudio (on PipeWire 1.0.5)


pipewire --version
pw-dump --version
pipewire
Compiled with libpipewire 1.0.5
Linked with libpipewire 1.0.5
pw-dump

pactl load-module module-null-sink sink_name=teams_sink sink_properties=device.description=TeamsSink

Verify:
pactl list short sources | grep teams_sink.monitor


Quick audio test;
# Keep silence flowing
ffmpeg -f lavfi -i anullsrc=r=48000:cl=mono -af "volume=0.01" -t 3600 silence.wav
pw-play silence.wav --target=teams_sink

Set default mic;
pactl set-default-source teams_sink.monitor
echo 'export PULSE_SOURCE=teams_sink.monitor' >> ~/.bashrc
echo 'export PIPEWIRE_RUNTIME_DIR=/run/user/$(id -u)' >> ~/.bashrc
source ~/.bashrc

Install chrome;
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
google-chrome --version

Test Chrome Sees Your Mic

PULSE_SOURCE=teams_sink.monitor xvfb-run -s "-screen 0 1920x1080x24" \
  google-chrome --use-fake-ui-for-media-stream --no-sandbox


git clone https://github.com/terzi46/real-time-translator-ms.git

cd real-time-translator-ms

source venv/bin/activate
pip install playwright
playwright install chromium


ffmpeg -f lavfi -i anullsrc=r=48000:cl=mono \
  -af "volume=0.01" \
  -t 3600 silence.wav

pw-cat -p silence.wav --target=teams_sink

Open a different terminal and see if it runs
pactl list short sinks | grep teams_sink


VIDEO


sudo apt install v4l2loopback-dkms ffmpeg
pip install opencv-python-headless pillow numpy

sudo modprobe v4l2loopback video_nr=0 card_label="PythonCam"

# Terminal 2 - Virtual Cam (ALWAYS RUNNING)
python3 ubuntu_virtual_cam.py

# Terminal 3 - verify if its active

v4l2-ctl --device=/dev/video0 --all | grep -E "Width/Height|Frame rate|Card type"

Expected output:

text
Card type      : PythonCam
Width/Height   : 1280/720
Frame rate     : 10.00 fps


To live check playwright screen

pkill Xvfb
pkill ffmpeg
pkill chrome
rm -f /tmp/.X99-lock
unset DISPLAY


mkdir -p ~/hls
chmod 755 ~/hls




Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

new SSh;

export DISPLAY=:99
xdpyinfo | grep dimensions
You should see 1920x1080.

google-chrome \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --use-fake-ui-for-media-stream \
  --autoplay-policy=no-user-gesture-required \
  --window-size=1920,1080 \
  https://teams.microsoft.com &



mkdir -p ~/hls


ffmpeg \
  -f x11grab \
  -video_size 1920x1080 \
  -framerate 30 \
  -i :99 \
  -c:v libx264 \
  -preset ultrafast \
  -tune zerolatency \
  -g 60 \
  -sc_threshold 0 \
  -pix_fmt yuv420p \
  -f hls \
  -hls_time 2 \
  -hls_list_size 5 \
  -hls_flags delete_segments \
  ~/hls/stream.m3u8

Leave this running.

new ssh
python3 -m http.server 8081

View it at;
http://52.53.208.124:8081/hls/stream.m3u8


Wanna kill the streaming?
pkill Xvfb
pkill ffmpeg
pkill chrome
pkill -f http.server


Activate the SAME venv

Important: don’t create a new one.

source venv/bin/activate


Verify:

which python


Should point to:

.../real-time-translator-ms/venv/bin/python

🥉 STEP 3 — Export runtime env (CRITICAL)

Even though Chrome is already running, Playwright needs these:

export DISPLAY=:99
export PULSE_SOURCE=teams_sink.monitor


Confirm:

echo $DISPLAY
echo $PULSE_SOURCE

🟦 STEP 4 — CLOSE ONLY the old Playwright browser (if any)

If Playwright is already running from an old script:

pkill -f playwright

python your_playwright_file.py

Morgen moet ik weer die neppe recording.wav geluid ook injecteren in die microfoon voordat ik in teams kom. ook die neppe cam openen. Daarna de playwright goed laten navigeren om te joinen in dat link. Zodra ik geluid hoor van mijn windows laptop () wacht wacht wacht, dit stukje moet nog dubbel gecheckt worden.

https://chatgpt.com/share/6989ac51-b4d0-8010-99d6-55b38a5caf67