# Metastellum-multiformosa

This is a digital office plant. Run this on a Raspberry Pi hooked up to a monitor and watch it grow. Like a plant, you will never see it move, but it is always changing.

In the first days, you will see a cardioid, a nephroid, and higher-order epicycloids. After many days, you will begin to see more intricate patterns emerge from the very-high-order epicycloids. Periodically, it will "bloom", starting by unfurling its rays, then forming epicycloids of decreasing order until it forms either an annulus or a point. Then the bloom will reverse.

"Metastellum" means "changing star", and "multiformosa" means "many shapes". The name was given by my partner, Evonne.

## Setup

Clone this repo into ~/Metastellum-multiformosa.

Add this to `/etc/fstab`

```
tmpfs           /mnt/ramdisk   tmpfs    nodev,nosuid,noexec,nodiratime,size=32M 0 0
```

Add this to `~/.bashrc`

```bash
export EDITOR='vim'

if ps -e | grep -P "(python3|fbi)" ; then
        echo "The plant is already running"
else
        # Start up Metestellum multiformosa
        pushd ~/Metastellum-multiformosa
        ./metastellum.py -s 2400 &
        sleep 15
        fbi link*.png
        popd
fi
```

Reboot the pi. The first time the plant starts, it will record the date and time. The animation is always performed in reference to that epoch. If it loses power, it will resume where it would have been otherwise.

There are probably more steps required.

1. Install fbi
2. Install python3 and python3-pip, python3-cairo
3. ln -s /mnt/ramdisk/ frames
4. Enable automatic login with raspi-config
5. sudo pip install numpy

