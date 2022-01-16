from feature import pafy
import vlc
from feature import youtube_dl
#import yt_dlp as youtube_dl
#import webbrowser
from googleapiclient.discovery import build
import urllib.request
import threading
import os
from dotenv import load_dotenv
import logger
logger = logger.get_logger(__name__)

import time

from TextToSpeech import TextToSpeech


class MusicStreaming():

    def __init__(self):
        self.thread = None
        self.play_video = None
        self.player = None
        self.isPlaying = None
        self.isPause = None
        self.isStop = None
        
    def import_thread(self, thread):
        self.thread = thread
        
    def pause_music(self):
        self.player.set_pause(True)
        self.isPlaying = False
        self.isPause = True
        self.isStop = False
        logger.info('Player paused')

    def continue_music(self):
        self.player.set_pause(False)
        self.isPlaying = True
        self.isPause = False
        self.isStop = False
        logger.info('Player continued')

    def stop_music(self):
        self.player.stop()
        self.isPlaying = False
        self.isPause = False
        self.isStop = True
        logger.info('Player stop')

    def now_playing(self):
        self.pause_music()

        title = self.pafy_video.title
        TextToSpeech.text_to_voice(title)

        self.continue_music()

    def repeat_playing(self):
        while(self.thread.is_run == False):
            self.playing()
        

    def return_playing_status(self):
        return [self.isPlaying, self.isPause, self.isStop]
        
    def playing(self):
        self.player.play()
        good_states = ["State.Playing", "State.NothingSpecial", "State.Opening", "State.Paused"]
        start = time.time()

        while str(self.player.get_state()) in good_states:
            end = time.time()
            self.isPlaying = True
            self.isPause = False
            self.isStop = False
            # print(self.thread.is_pause())
            if self.thread.is_pause():
                self.pause_music()
            else:
                self.continue_music()

            if self.thread.is_run() == False:
                self.stop_music()

            if ((end - start) % 10) == 0: 
                logger.debug('Stream is working. Current state = {}'.format(self.player.get_state()))

        logger.debug('Stream is not working. Current state = {}'.format(self.player.get_state()))
        self.stop_music()

    def pafy_video(self, videoId):
        url = 'https://www.youtube.com/watch?v={0}'.format(videoId)
        logger.info(url)
    #    ydl_opts = {"--no-check-certificate": True}
    #    play_video = pafy.new(url, ydl_opts)
        self.play_video = pafy.new(url)
        # print("title: ", self.play_video.title)
        best = self.play_video.getbestaudio()
        play_url = best.url
        Instance = vlc.Instance()
        self.player = Instance.media_player_new()
        
        code = urllib.request.urlopen(url).getcode()
        if str(code).startswith('2') or str(code).startswith('3'):
            logger.info('Stream is working')
        else:
            logger.info('Stream is dead')
        
        Media = Instance.media_new(play_url)
        Media.get_mrl()
        self.player.set_media(Media)
        events = self.player.event_manager()
        
        self.thread.add_thread({
        'class': 'MusicStreaming',
        'func': 'playing',
        })

    def play_music(self, target):

        if target == "":
            message = "請重講一次並加上歌名"

            self.thread.add_thread({
            'class': 'TextToSpeech',
            'func': 'text_to_voice',
            'args':(message,),
            })

            return

        load_dotenv()
        API_Key = os.getenv("YOUTUBE_API_KEY")
        
        youtube = build('youtube', 'v3', developerKey=API_Key)

        request = youtube.search().list(
                part = 'id, snippet',
                maxResults = 3,
                order = 'viewCount',
                q = target
            )

        response = request.execute()

        logger.info(response)

        videos = []

        for search_result in response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append('%s' % (search_result['id']['videoId']))

        if videos:
            logger.info('Videos:{0}'.format(videos))
            self.pafy_video(videos[0])