#!/usr/bin/python3

import sys
import dbus
import logging


class Call:
    def __init__(self):
        pass

    def call(self, way, number):
        self.number = number

        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object('org.ofono', '/'),
                                 'org.ofono.Manager')

        modems = manager.GetModems()
        modem = modems[0][0]

        hide_callerid = "default"

        print("Using modem %s" % modem)

        vcm = dbus.Interface(bus.get_object('org.ofono', modem),
                             'org.ofono.VoiceCallManager')

        path = vcm.Dial(number, hide_callerid)
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
