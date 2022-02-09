#!/bin/sh

# check admin
if ![ "$EUID" -eq 0 ] ; then
    echo "you need root"
	exit 1
fi

# install robotpy-cscore
echo 'deb http://download.opensuse.org/repositories/home:/auscompgeek:/robotpy/Ubuntu_18.04_Ports/ /' | sudo tee /etc/apt/sources.list.d/home:auscompgeek:robotpy.list
wget https://download.opensuse.org/repositories/home:auscompgeek:robotpy/Ubuntu_18.04_Ports/Release.key 
cat Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_auscompgeek_robotpy.gpg > /dev/null
apt update
apt install -y python3-cscore
rm Release.key

# setup /etc/hosts to connect to rio
echo "10.8.62.10 roboRIO-862-FRC.lan" >> /etc/hosts # jetson ip on team image radio
echo "10.8.62.10 roboRIO-862-FRC.frc-field.lan" >> /etc/hosts # jetson ip on fms image radio

# make app environment
mkdir -p /home/lightning/voidvision/
touch /home/lightning/voidvision/runCamera # make sure this file exists - empty version will be overwritten on deploy

# configure app to run on boot
echo "@reboot sh /home/lightning/voidvision/runCamera" >> /etc/crontab
