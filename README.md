# Metastellum-multiformosa

This is a digital office plant. Run this on a Raspberry Pi hooked up to a monitor and watch it grow. Like a plant, you will never see it move, but it is always changing.

It will start as a circle. In the first days, you will see a cardioid, a nephroid, and higher-order epicycloids. After many days, you will begin to see more intricate patterns emerge from the intersecting lines of the very-high-order epicycloids. Periodically, it will "bloom", starting by unfurling its rays, then forming epicycloids of decreasing order until it forms either an annulus or a point. Then the bloom will reverse its metamorphisis.

"Metastellum" means "changing star", and "multiformosa" means "many shapes". The name was given by my partner, Evonne.

## Setup

Clone this repo into ~/Metastellum-multiformosa.

Use `raspi-config` to enable automatic login.

Run `setup.sh` to:
* Install the required packages
* Create a RAM disk for the frames (otherwise you will wear out your flash storage)
* Append a line to `~/.bashrc` to run `start.sh`
* Write the settings for `fbi` to `~/.fbirc`

Reboot the pi. The first time the plant starts, it will record the date and time. The animation is always performed in reference to that epoch. If it loses power, it will resume where it would have been otherwise.
