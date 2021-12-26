sudo apt update
sudo apt-get install -y build-essential tk-dev libncurses5-dev libnss3-dev libatlas-base-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
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
sudo apt-get install -y flac
sudo apt-get install -y libasound-dev
sudo apt-get install -y portaudio19-dev
sudo apt-get install -y python3-pyaudio
sudo apt-get install -y libdbus-1-dev
sudo apt-get install -y libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
sudo apt-get install -y llvm-11-dev
sudo rm /usr/bin/llvm-config
sudo ln -s /usr/bin/llvm-config-11 /usr/bin/llvm-config


if [ -z "$(uname -a | grep raspberrypi)"]
then
    echo "Not a raspberrypi, stop installing seeed-voicecard package & stop installing pip packages."
else
    python3.7 -m pip install --user -r requirements.txt
    sudo apt-get update
    git clone https://github.com/respeaker/seeed-voicecard.git
    sudo ./seeed-voicecard/install.sh
    sudo rm -r ./seeed-voicecard
    sudo reboot
fi