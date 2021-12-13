import pafy
import vlc
#import youtube_dl
import yt_dlp as youtube_dl
#import webbrowser
from googleapiclient.discovery import build
import urllib.request

API_KEY = 'AIzaSyDYvK29Z74AqL3lGK8c3tgR0RsFygKyJkU'

class MusicStreaming():

    def __init__(self, text):
        self.target = text

    def pafy_video(self, videoId):
        url = 'https://www.youtube.com/watch?v={0}'.format(videoId)
        print(url)
    #    webbrowser.open(url)
    #    ydl_opts = {"--no-check-certificate": True}
    #    play_video = pafy.new(url, ydl_opts)
        play_video = pafy.new(url)
        best = play_video.getbestaudio()
    #    media = vlc.MediaPlayer(best.url)
    #    media.play()
        play_url = best.url
        Instance = vlc.Instance()
        player = Instance.media_player_new()
        
        code = urllib.request.urlopen(url).getcode()
        if str(code).startswith('2') or str(code).startswith('3'):
            print('Stream is working')
        else:
            print('Stream is dead')
        
        Media = Instance.media_new(play_url)
        Media.get_mrl()
        player.set_media(Media)
        events = player.event_manager()
        player.play()
        print(events)
        
        good_states = ["State.Playing", "State.NothingSpecial", "State.Opening"]
        while str(player.get_state()) in good_states:
            print('Stream is working. Current state = {}'.format(player.get_state()))

        print('Stream is not working. Current state = {}'.format(player.get_state()))
        player.stop()

    def play_music(self):
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        request = youtube.search().list(
                part = 'id, snippet',
                maxResults = 3,
                order = 'viewCount',
                q = self.target
            )

        response = request.execute()

        print(response)

        videos = []

        for search_result in response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append('%s' % (search_result['id']['videoId']))

        if videos:
            print('Videos:{0}'.format(videos))
            self.pafy_video(videos[0])
        
        
if __name__ == "__main__":
    text = 'chungha killing me'
    music = MusicStreaming(text)
    music.play_music()
    
#Instance = vlc.Instance()
#player = Instance.media_player_new()
#Media = Instance.media_new('test.mp3')
#Media.get_mrl()
#player.set_media(Media)
#player.play()
#
#print(player.play())

#import mpv
#import yt_dlp
#player = mpv.MPV(ytdl=True)
#player.play('https://youtu.be/DOmdB7D-pUU');
#print(player.metadata);
#player.wait_for_playback();

