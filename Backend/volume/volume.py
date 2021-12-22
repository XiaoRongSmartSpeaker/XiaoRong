import os

# for Development
playing = True

class volume:
    def __init__(self) -> None:
        self.systemVolume = 100
        self.musicVolume = 100
        return
    #alsa setting
    def set_amixer(self, value):
        cmd = "amixer -M set Master {}\%".format(value)
        returned_value = os.system(cmd)
        # print("returned value:", returned_value)
        return True

    #unspecified
    def get_volume(self)->int:
        if playing:
            return self.get_music_volume()
        return self.get_system_volume()
    def set_volume(self, value):
        if playing:
            return self.set_music_volume(value)
        return self.set_system_volume(value)
    def louder_volume(self, value):
        if playing:
            return self.louder_music_volume(value)
        return self.louder_system_volume(value)
    def quieter_volume(self, value):
        if playing:
            return self.quieter_music_volume(value)
        return self.quieter_system_volume(value)
    #system
    def get_system_volume(self)->int:
        return self.systemVolume
    def set_system_volume(self, value=5):
        if 10 <= value <= 100:
            self.systemVolume = value
            self.set_amixer(self.systemVolume)
        return True
    def louder_system_volume(self, value=5):
        if 10 <= self.systemVolume + value <= 100:
            self.systemVolume += value
            self.set_amixer(self.systemVolume)
    def quieter_system_volume(self, value=5):
        if 10 <= self.systemVolume - value <= 100:
            self.systemVolume -= value
            self.set_amixer(self.systemVolume)
    # music
    def get_music_volume(self):
        return self.musicVolume
    def set_system_volume(self, value=5):
        if 0 <= value <= 100:
            self.musicVolume = value
            self.set_amixer(self.musicVolume)
        return True
    def louder_system_volume(self, value=5):
        if 0 <= self.musicVolume + value <= 100:
            self.musicVolume += value
            self.set_amixer(self.musicVolume)
    def quieter_system_volume(self, value=5):
        if 0 <= self.musicVolume - value <= 100:
            self.musicVolume -= value
            self.set_amixer(self.musicVolume)