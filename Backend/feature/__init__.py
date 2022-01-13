import sys
import os
# add feature path to sys.path
sys.path.append(os.path.dirname(__file__))  # noqa: E402
from .SpeechToText import SpeechToText
from .TextToSpeech import TextToSpeech
from .Extract import Extract
from .Bluetooth import Bluetooth
from .Volume import Volume
from .Translate import Translate
from .MusicStreaming import MusicStreaming
from .QuestionAnswering import QuestionAnswering
from .Weather import Weather
from .WorldTime import WorldTime
from .Countdown import Countdown
from .Test import Test