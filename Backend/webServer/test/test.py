from server import *

device = "ERROR000000000"


def log_create():
    print(addLog(device, "hello world"))
    print(addLog(device, "i am xiaorong"))
    print(getLog(device))


def get_user():
    print(getAllUser())
    print(getUser("kizato1018@gmail.com"))


def get_device():
    print(getDevice(device))


def update_playing():
    print(isPlaying(device))
    print(getDevice(device))
    print(isPause(device))
    print(getDevice(device))
    print(isStop(device))
    print(getDevice(device))


get_user()
get_device()
update_playing()
# log_create()
