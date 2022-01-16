#!/usr/bin/python3
import os
import sys
import dbus
import logging
from Bluetooth import Bluetooth
from TextToSpeech import TextToSpeech

class Call:
    def __init__(self):
        self.thread = None

    def import_thread(self, thread):
        self.thread = thread

    def make_call(self, way, number):
        b_instance = self.thread.get_instance('Bluetooth')
        if (b_instance != None):
            isConnected, address = b_instance.get_bluetooth_status()
            if(isConnected == False):
                TextToSpeech.text_to_voice('藍芽沒有鏈接')
                return
        else:
            TextToSpeech.text_to_voice('藍芽沒有鏈接')
            return
        os.system('./enable-modem')
        os.system('./online-modem')
        self.number = number.replace('-', '');

        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object('org.ofono', '/'),
                                 'org.ofono.Manager')

        modems = manager.GetModems()
        modem = modems[0][0]

        hide_callerid = "default"

        print("Using modem %s" % modem)

        vcm = dbus.Interface(bus.get_object('org.ofono', modem),
                             'org.ofono.VoiceCallManager')

        path = vcm.Dial(self.number, hide_callerid)
        logging.info('making a phone call')
        print(path)

    def hung_up(self):
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object('org.ofono', '/'),
                                 'org.ofono.Manager')

        modems = manager.GetModems()
        modem = modems[0][0]

        manager = dbus.Interface(bus.get_object('org.ofono', modem),
                                 'org.ofono.VoiceCallManager')

        manager.HangupAll()
        logging.info('hungup a phone call')
