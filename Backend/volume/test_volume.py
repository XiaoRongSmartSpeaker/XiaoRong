from volume import volume

def get_all_volume():
    print("System:", a.get_system_volume())
    print("Music:", a.get_music_volume())
a = volume()
a.set_system_volume(50)
get_all_volume()
a.louder_system_volume()
get_all_volume()
a.quieter_system_volume()
get_all_volume()
a.louder_system_volume(10)
get_all_volume()
a.louder_system_volume(100)
get_all_volume()
a.quieter_system_volume(10)
get_all_volume()
a.quieter_system_volume(100)
get_all_volume()



