#!/bin/bash

echo "🔧 Resetting audio for user: $(whoami)"

# 1. Stop services gracefully
echo "🛑 Stopping audio services..."
systemctl --user stop pipewire-pulse pipewire wireplumber

# 2. Kill any stragglers
echo "🔪 Killing leftover processes..."
pkill -u $(id -u) -f pipewire
pkill -u $(id -u) -f wireplumber

# 3. Clean up stale sockets
echo "🧹 Cleaning sockets..."
rm -f $XDG_RUNTIME_DIR/pipewire-0
rm -f $XDG_RUNTIME_DIR/pipewire-0.lock
rm -f $XDG_RUNTIME_DIR/pulse/native

# 4. Restart services
echo "🔄 Starting audio services..."
systemctl --user daemon-reload
systemctl --user start pipewire wireplumber pipewire-pulse

# 5. Wait for initialization
echo "⏳ Waiting 3 seconds..."
sleep 3

# 6. Load Sink
echo "🔊 Loading Teams Sink..."
# Ensure XDG_RUNTIME_DIR is correct
export XDG_RUNTIME_DIR=/run/user/$(id -u)

if pactl load-module module-null-sink sink_name=teams_sink sink_properties=device.description=TeamsSink; then
    echo "✅ SUCCESS: Audio sink loaded!"
    echo "Default Source Set To: teams_sink.monitor"
    pactl set-default-source teams_sink.monitor
else
    echo "❌ FAILED: Still cannot connect. A system reboot is recommended."
fi
