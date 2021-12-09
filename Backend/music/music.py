import pafy
import vlc
import youtube_dl
#import webbrowser
from googleapiclient.discovery import build

API_KEY = 'AIzaSyDYvK29Z74AqL3lGK8c3tgR0RsFygKyJkU'

def pafy_video(videoId):
    url = 'https://www.youtube.com/watch?v={0}'.format(videoId)
    print(url)
#    webbrowser.open(url)
    ydl_opts = {"--no-check-certificate": True}
    play_video = pafy.new(url, ydl_opts)
    best = play_video.getbestaudio()
#    media = vlc.MediaPlayer(best.url)
#    media.play()
    play_url = best.url
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(play_url)
    Media.get_mrl()
    player.set_media(Media)
    player.play()

youtube = build('youtube', 'v3', developerKey=API_KEY)

text = '周杰倫的給我一首歌的時間'

request = youtube.search().list(
        part = 'id, snippet',
        maxResults = 3,
        order = 'viewCount',
        q = text
    )

response = request.execute()

print(response)

videos = []

for search_result in response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
        videos.append('%s' % (search_result['id']['videoId']))

if videos:
    print('Videos:{0}'.format(videos))
    pafy_video(videos[0])

#import mpv
#import yt_dlp
#player = mpv.MPV(ytdl=True)
#player.play('https://youtu.be/DOmdB7D-pUU');
#print(player.metadata);
#player.wait_for_playback();

