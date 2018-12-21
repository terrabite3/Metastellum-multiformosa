#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $DIR


apt-get update
apt-get install fbi python3 python3-pip python3-cairo python3-numpy

echo "tmpfs /mnt/ramdisk tmpfs nodev,nosuid,noexec,nodiratime,size=32M 0 0" >> /etc/fstab

ln -s /mnt/ramdisk/ frames

echo "$DIR/start.sh" >> ~/.bashrc

echo "[options]
verbose = false
cache-mem = 0
timeout = 1
once = false
auto-up = true
auto-down = true
blend-msecs = 1000" > ~/.fbirc


echo "Reboot the machine to start the plant"
