#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
import subprocess
import os
import sys

class UbuntuVirtualCam:
    def __init__(self):
        self.width, self.height = 1280, 720
        self.fps = 10
        self.device = "/dev/video0"
        self.messages = ["TRANSLATOR LIVE", "Meeting Active", "Ready", "Online"]
        self.msg_idx = 0

    def setup_v4l2loopback(self):
        subprocess.run(['sudo', 'modprobe', '-r', 'v4l2loopback'], check=False)
        subprocess.run([
            'sudo', 'modprobe', 'v4l2loopback',
            f'video_nr=0', 'card_label="PythonCam"',
            'exclusive_caps=1', 'max_buffers=2'
        ], check=True)
        time.sleep(2)
        print(f"✅ Virtual cam ready: {self.device}")

    def create_frame(self):
        frame = np.zeros((self.height, self.width, 3), np.uint8) * 30
        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_frame)

        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        except:
            font = ImageFont.load_default()

        msg = self.messages[self.msg_idx % len(self.messages)]
        self.msg_idx += 1

        bbox = draw.textbbox((0,0), msg, font=font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        y = (self.height - (bbox[3] - bbox[1])) // 2
        draw.text((x, y), msg, fill=(220, 220, 255), font=font)

        return cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)

    def stream_to_v4l2(self):
        print("📹 Streaming to /dev/video0 - Teams ready!")
        print("✅ Test: v4l2-ctl --device=/dev/video0 --all")

        frame_time = 1.0 / self.fps

        while True:
            frame = self.create_frame()

            # Fixed FFmpeg command with sudo
            pipe = subprocess.Popen([
                'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24',
                '-s', f'{self.width}x{self.height}', '-r', str(self.fps), '-i', '-',
                '-c:v', 'rawvideo', '-pix_fmt', 'yuv420p', '-f', 'v4l2', self.device
            ], stdin=subprocess.PIPE)

            try:
                while pipe.poll() is None:
                    pipe.stdin.write(frame.tobytes())
                    pipe.stdin.flush()
                    time.sleep(frame_time)
            except:
                pipe.terminate()

    def run(self):
        self.setup_v4l2loopback()
        self.stream_to_v4l2()

if __name__ == "__main__":
    cam = UbuntuVirtualCam()
    cam.run()
