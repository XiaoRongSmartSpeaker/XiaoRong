cd ./wifi_driver
chmod +x install.sh
sudo ./install.sh
cd ..

sudo apt update

sudo apt install hostapd dnsmasq iptables -y
sudo cp AP/hostapd.conf /etc/hostapd/
sudo cp AP/hostapd /etc/default/
sudo cp AP/dnsmasq.conf /etc/
sudo cp AP/sysctl.conf /etc/
sudo cp AP/dhcpcd.conf /etc/

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
sudo mv AP/rc.local /etc/
chmod +x /etc/rc.local

sudo apt-get install -y build-essential tk-dev libncurses5-dev libnss3-dev libatlas-base-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev libffi6-dev
if [-z "$(type -P python3.7)"] 
then
    curl -O https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
    tar -xf Python-3.7.3.tar.xz
    cd Python-3.7.3
    ./configure
    make -j 8
    sudo make altinstall
    cd ../
    sudo rm -rf Python-3.7.3
    rm Python-3.7.3.tar.xz
else
    echo "Python3.7 is already installed"
fi
sudo apt-get install -y python3-gst-1.0
sudo apt-get install -y alsa-utils
sudo apt-get install -y ofono
sudo apt-get install -y vlc
sudo apt-get install -y flac
sudo apt-get install -y libasound-dev
sudo apt-get install -y portaudio19-dev
sudo apt-get install -y python3-pyaudio
sudo apt-get install -y libdbus-1-dev
sudo apt-get install -y libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
sudo apt-get install -y llvm-11-dev
sudo rm /usr/bin/llvm-config
sudo ln -s /usr/bin/llvm-config-11 /usr/bin/llvm-config


if [ -z "$(cat /proc/cpuinfo | grep -E "Model\s+:\sRaspberry")"]
then
    echo "Not a raspberrypi, stop installing seeed-voicecard package & stop installing pip packages."
else
    python3.7 -m pip install --user -r requirements.txt
    git clone https://github.com/respeaker/seeed-voicecard.git
    cd ./seeed-voicecard
    sudo ./install.sh
    cd ..
    sudo rm -r ./seeed-voicecard
    sudo reboot
fi
