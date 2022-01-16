#!/usr/bin/python3

import sys
import dbus
import logging
import Bluetooth
import TextToSpeech

class Call:
    def __init__(self):
        pass

    def make_call(self, way, number):
        if(Bluetooth.get_bluetooth_status() == False):   #get_bluetooth_status(): False
            #print('device not connected')
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
