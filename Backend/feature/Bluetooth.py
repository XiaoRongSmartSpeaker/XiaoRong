#!/usr/bin/python
import sys
from xmlrpc.client import SERVER_ERROR
import dbus
import dbus.service
import dbus.mainloop.glib
import threading
import requests
from util import get_device_id
try:
    from gi.repository import GLib
except ImportError:
    import Glib as GLib
try:
    import logger
    logger = logger.get_logger(__name__)
except ModuleNotFoundError:
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
# Server Url setting
SERVER_URI = "http://www.xiaorongserver.tk"

# static name & path setting
SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"
AGENT_INTERFACE = SERVICE_NAME + ".Agent1"
AGENT_MANAGER_INTERFACE = SERVICE_NAME + ".AgentManager1"
MEDIA_PLAYER_INTERFACE = SERVICE_NAME + "MediaPlayer1"
OBJECT_MANAGER_INTERFACE = "org.freedesktop.DBus.ObjectManager"
PROPERTY_INTERFACE = "org.freedesktop.DBus.Properties"
AGENT_PATH = "/xiaorong/agent"
DEVICE_PATH = "/xiaorong/device"
ADAPTER_ROOT = '/org/bluez/hci'

relevant_ifaces = [ADAPTER_INTERFACE, DEVICE_INTERFACE, MEDIA_PLAYER_INTERFACE]

### Start -- Some useful utilty function ###


def proxyobj(bus, path, interface) -> dbus.proxies.Interface:
    """ commodity to apply an interface to a proxy object """
    obj = bus.get_object(SERVICE_NAME, path)
    return dbus.Interface(obj, interface)


def filter_by_interface(objects, interface_name) -> list:
    """ filters the objects based on their support
            for the specified interface """
    result = []
    for path in objects.keys():
        interfaces = objects[path]
        for interface in interfaces.keys():
            if interface == interface_name:
                result.append(path)
    return result


def get_managed_objects() -> dbus.proxies.Interface:
    bus = dbus.SystemBus()
    manager = proxyobj(bus, "/", OBJECT_MANAGER_INTERFACE)
    return manager.GetManagedObjects()


def find_adapter(pattern=None) -> dbus.proxies.Interface:
    return find_adapter_in_objects(get_managed_objects(), pattern)


def find_adapter_in_objects(objects, pattern=None) -> dbus.proxies.Interface:
    bus = dbus.SystemBus()
    for path, ifaces in objects.items():
        adapter = ifaces.get(ADAPTER_INTERFACE)
        if adapter is None:
            continue
        if not pattern or pattern == adapter["Address"] or \
                path.endswith(pattern):
            obj = bus.get_object(SERVICE_NAME, path)
            return dbus.Interface(obj, ADAPTER_INTERFACE)
    raise Exception("Bluetooth adapter not found")


def find_device(device_address,
                adapter_pattern=None) -> dbus.proxies.Interface:
    return find_device_in_objects(get_managed_objects(), device_address,
                                  adapter_pattern)


def find_device_in_objects(objects,
                           device_address,
                           adapter_pattern=None) -> dbus.proxies.Interface:
    bus = dbus.SystemBus()
    path_prefix = ""
    if adapter_pattern:
        adapter = find_adapter_in_objects(objects, adapter_pattern)
        path_prefix = adapter.object_path
    for path, ifaces in objects.items():
        device = ifaces.get(DEVICE_INTERFACE)
        if device is None:
            continue
        if (device["Address"] == device_address
                and path.startswith(path_prefix)):
            obj = bus.get_object(SERVICE_NAME, path)
            return dbus.Interface(obj, DEVICE_INTERFACE)

    raise Exception("Bluetooth device not found")


def get_device_address_by_path(path) -> str:
    try:
        address = path.split("dev_")[1].replace("_", ":")
        return address
    except BaseException:
        logger.error("Bluetooth address not found in path.")
        return
### End -- Some useful utilty function ###


class BluetoothError(Exception):
    pass


class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


class Agent(dbus.service.Object):
    def __init__(self,
                 conn=None,
                 object_path=None,
                 bus_name=None,
                 mainloop=None):
        super(self.__class__, self).__init__(conn, object_path, bus_name)
        self.mainloop = mainloop
        self.bus = conn
        self.exit_on_release = True
        self.connectedDevice = None

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        logger.info("Release")
        if self.exit_on_release:
            self.mainloop.quit()

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        logger.info("AuthorizeService (%s, %s)" % (device, uuid))
        # Authorize any service by default
        # TODO need to check whether there are security issues.
        if (True):
            return
        raise Rejected("Connection rejected by user")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        logger.info("RequestAuthorization (%s)" % (device))
        # Accept any request
        if (True):
            return
        raise Rejected("Pairing rejected")

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        logger.info("Cancel")


class Adapter(dbus.service.Object):
    def __init__(self, conn=None, object_path=None, bus_name=None, idx=0):
        super(self.__class__, self).__init__(conn, object_path, bus_name)
        self.bus = conn
        self.path = f'{ADAPTER_ROOT}{idx}'
        self.adapterProps = proxyobj(self.bus, self.path,
                                     dbus.PROPERTIES_IFACE)

    def make_power_on(self):
        self.adapterProps.Set(ADAPTER_INTERFACE, 'Powered', True)
        logger.info("Bluetooth power on")

    def make_power_off(self):
        self.adapterProps.Set(ADAPTER_INTERFACE, 'Powered', False)
        logger.info("Bluetooth power off")

    def make_discoverable(self, secs=60):
        self.adapterProps.Set(ADAPTER_INTERFACE, 'DiscoverableTimeout',
                              dbus.UInt32(secs))
        self.adapterProps.Set(ADAPTER_INTERFACE, 'Discoverable', True)
        logger.info("Bluetooth discoverable on")

    def make_pairable(self, secs=60):
        self.adapterProps.Set(ADAPTER_INTERFACE, 'PairableTimeout',
                              dbus.UInt32(secs))
        self.adapterProps.Set(ADAPTER_INTERFACE, 'Pairable', True)
        logger.info("Bluetooth pairable on")

    def change_alias(self, alias):
        self.adapterProps.Set(ADAPTER_INTERFACE, 'Alias', alias)
        if alias == "":
            alias = self.adapterProps.Get(ADAPTER_INTERFACE, 'Name')
        logger.info(f"Change bluetooth alias into {alias}")


class Device():
    def __init__(self, bus):
        # initialize
        self.bus = bus

        # disconnect already connected devices
        connectedDevicesList = self.get_connected_devices_list()
        for device in connectedDevicesList:
            self.disconnect(device["address"], device["name"])

    def disconnect(self, address, name=None):
        device = find_device(address)
        device.Disconnect()
        if name is not None:
            logger.info(f"Disconnect from { address }({ name }).")
        else:
            logger.info(f"Disconnect from { address }.")

    def get_devices_obj(self):
        # Get devices object
        objects = get_managed_objects()
        devicesObj = filter_by_interface(objects, DEVICE_INTERFACE)

        return devicesObj

    def get_connected_devices_list(self):
        connectedDevicesObj = []
        devicesObj = self.get_devices_obj()
        for deviceObj in devicesObj:
            obj = proxyobj(self.bus, deviceObj, PROPERTY_INTERFACE)
            if obj.Get(DEVICE_INTERFACE, "Connected"):
                connectedDevicesObj.append({
                    "name":
                    str(obj.Get(DEVICE_INTERFACE, "Name")),
                    "address":
                    str(obj.Get(DEVICE_INTERFACE, "Address")),
                    "connected":
                    str(obj.Get(DEVICE_INTERFACE, "Connected"))
                })
        return connectedDevicesObj


class MediaPlayer():
    def __init__(self, bus):
        # initialize
        self.bus = bus
        self.player_iface = None
        self.transport_prop_iface = None

        # obtain MediaPlayer1 & MediaTransport1 interface
        for path, ifaces in get_managed_objects().items():
            if MEDIA_PLAYER_INTERFACE in ifaces:
                self.player_iface = proxyobj(SERVICE_NAME, path,
                                             MEDIA_PLAYER_INTERFACE)

            elif 'org.bluez.MediaTransport1' in ifaces:
                self.transport_prop_iface = proxyobj(SERVICE_NAME, path,
                                                     PROPERTY_INTERFACE)

        # can't obtain MediaPlayer1 interface
        if not self.player_iface:
            logger.error('Media Player not found.')
            return None

        # can't obtain MediaTransport1 interface
        if not self.transport_prop_iface:
            logger.error('DBus.Properties MediaTransport1 iface not found.')
            return None

        logger.info("Bluetooth's Player successfully initialize.")

    def pause(self):
        self.player_iface.Pause()

    def play(self):
        self.player_iface.Play()


class Bluetooth():
    def __init__(self):
        capability = "NoInputNoOutput"
        # threadHandler initialize (for main function)
        self.threadHandler = None

        # Main loop setting (bluetooth monitor daemon)
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.mainloop = GLib.MainLoop()

        # Bus, Adapter, Device, Agent, MediaPlayer initialize
        self.bus = dbus.SystemBus()
        self.adapter = Adapter(self.bus)
        self.device = Device(self.bus)
        self.agent = Agent(conn=self.bus,
                           object_path=AGENT_PATH,
                           mainloop=self.mainloop)
        self.mediaPlayer = None
        self.isPlaying = None

        # Agent manager initialize
        self.manager = proxyobj(self.bus, "/org/bluez",
                                AGENT_MANAGER_INTERFACE)

        # Register Agent
        self.manager.RegisterAgent(AGENT_PATH, capability)
        logger.info("Agent registered")
        self.manager.RequestDefaultAgent(AGENT_PATH)

        # Event Listener initialize
        self.__init_listener()

        # Bluetooth device name initialize
        device_id = get_device_id()
        if device_id != "ERROR000000000":
            device_name = None
            try:
                r = requests.session()
                response = r.get(f"{SERVER_URI}/devicedata/{device_id}")
                if response.status_code != 404:
                    device_name = response.json()["device_name"]
                else:
                    device_name = None
                    logger.error(f"Error msg from server \"{response.json()['detail']}\"")
            except ConnectionError:
                logger.error("Network failed to connect. Unable to fetch device_name from server.")
            except BaseException as e:
                logger.error(e)
                
            if device_name == None or device_name == "":
                self.set_bluetooth_alias("小瀜音箱")
                logger.debug("The device_name fetch from server is None or empty, therefore set bluetooth device name into 小瀜音箱")
            else:
                self.set_bluetooth_alias(device_name)
        else:
            logger.error("Failed to get the device_id from system")

        logger.info("Ready to start bluetooth daemon")

    def bluetooth_daemon_start(self) -> None:
        if self.threadHandler:
            self.threadHandler.add_thread({
                'class': 'TextToSpeech',
                'func': 'text_to_voice',
                'args': ('藍芽已開啟', )
            })
            logger.info("Bluetooth daemon opened")
        else:
            logger.error("threadHandler not exist. Failed to add thread.")
        self.mainloop.run()

    def open_bluetooth(self):
        logger.info("Bluetooth daemon start")
        # adapter setting
        self.adapter.make_power_on()
        self.adapter.make_pairable()
        self.adapter.make_discoverable()
        if self.threadHandler:
            self.threadHandler.add_thread({
                'class': 'Bluetooth',
                'func': 'bluetooth_daemon_start',
            })
            return
        else:
            # When threadHandler doesn't exist return thread to start.
            logger.error("threadHandler not exist. Failed to add thread.")
            logger.info("try to start bluetooth daemon in current thread...")
            t = threading.Thread(target=self.bluetooth_daemon_start)
            return t

    def close_bluetooth(self) -> None:
        self.adapter.make_power_off()
        self.manager.UnregisterAgent(AGENT_PATH)
        self.mainloop.quit()
        if self.threadHandler:
            self.threadHandler.add_thread({
                'class': 'TextToSpeech',
                'func': 'text_to_voice',
                'args': ('藍芽已關閉', )
            })
        else:
            logger.error("threadHandler not exist. Failed to add thread.")
        logger.info("Bluetooth daemon closed")

    def get_bluetooth_status(self):
        connectedDevicesList = self.device.get_connected_devices_list()
        if len(connectedDevicesList) > 1:
            logger.error("Multiple bluetooth devices connected.")
            raise BluetoothError
        elif len(connectedDevicesList) == 1:
            return True, connectedDevicesList[0]["address"]
        else:
            return False, None

    def get_bluetooth_playing_status(self) -> bool:
        if self.isPlaying == True:
            return True
        else:
            return False

    def pause_bluetooth_playing(self) -> bool:
        try:
            if self.mediaPlayer:
                self.mediaPlayer.pause()
                logger.info("Pause bluetooth device's music")
                return 1
            else:
                logger.error("Bluetooth's Media Player not found.")
                return 0
        except BluetoothError as e:
            logger.critical(f"Bluetooth.pause_bluetooth_playing failed, {e}")
            return 0

    def play_bluetooth_playing(self) -> bool:
        try:
            if self.mediaPlayer:
                self.mediaPlayer.play()
                logger.info("Pause bluetooth device's music")
                return 1
            else:
                logger.error("Bluetooth's Media Player not found.")
                return 0
        except BluetoothError as e:
            logger.critical(f"Bluetooth.pause_bluetooth_playing failed, {e}")
            return 0

    def volume_change(self, volume):
        self.threadHandler.add_thread({
            'class': 'Volume',
            'func': 'set_music_volume',
            'args': (volume, ),
        })

    def set_bluetooth_alias(self, alias):
        self.adapter.change_alias(alias)

    def import_thread(self, thread):
        self.threadHandler = thread

    def __init_listener(self):
        # Event listener
        self.bus.add_signal_receiver(self.property_changed,
                                     bus_name=SERVICE_NAME,
                                     dbus_interface=PROPERTY_INTERFACE,
                                     signal_name="PropertiesChanged",
                                     path_keyword="path")

        self.bus.add_signal_receiver(self.interfaces_added,
                                     bus_name=SERVICE_NAME,
                                     dbus_interface=OBJECT_MANAGER_INTERFACE,
                                     signal_name="InterfacesAdded")

        self.bus.add_signal_receiver(self.interfaces_removed,
                                     bus_name=SERVICE_NAME,
                                     dbus_interface=OBJECT_MANAGER_INTERFACE,
                                     signal_name="InterfacesRemoved")

    def property_changed(self, interface, changed, invalidated, path):
        iface = interface[interface.rfind(".") + 1:]
        for name, value in changed.items():
            stringValue = str(value)
            logger.debug("{%s.PropertyChanged} [%s] %s = %s" %
                         (iface, path, name, stringValue))
            # Event handling
            if name == "Volume":  # Volume change
                self.volume_change(value)
            elif iface == "Device1" and name == "Connected" and value == 1:  # Device connected
                device_address = get_device_address_by_path(path)
                if self.agent.connectedDevice:
                    self.device.disconnect(device_address)
                    logger.info("Other device already connected.")
                else:
                    self.agent.connectedDevice = device_address

                    obj = proxyobj(self.bus, path, PROPERTY_INTERFACE)
                    deviceName = obj.Get(DEVICE_INTERFACE, "Name")
                    logger.info(f"已連接{deviceName}")

                    if self.threadHandler:
                        self.threadHandler.add_thread({
                            'class': 'TextToSpeech',
                            'func': 'text_to_voice',
                            'args': (f'已連接{deviceName}', )
                        })
                    else:
                        logger.error("threadHandler not exist. Failed to add thread.")
            # Device disconnected
            elif iface == "Device1" and name == "Connected" and value == 0 and self.agent.connectedDevice == get_device_address_by_path(path):
                self.agent.connectedDevice = None

                obj = proxyobj(self.bus, path, PROPERTY_INTERFACE)
                deviceName = obj.Get(DEVICE_INTERFACE, "Name")
                logger.info(f"{deviceName}已斷開連接")
                if self.threadHandler:
                    self.threadHandler.add_thread({
                        'class': 'TextToSpeech',
                        'func': 'text_to_voice',
                        'args': (f'{deviceName}已斷開連接', )
                    })
                else:
                    logger.error("threadHandler not exist. Failed to add thread.")
            elif iface == "MediaPlayer1" and name == "status" and value == "pause":
                self.threadHandler.pause()
                self.isPlaying = False
            elif iface == "MediaPlayer1" and name == "status" and value == "playing":
                self.threadHandler.resume()
                self.isPlaying = True

    def interfaces_added(self, path, interfaces):
        for iface, props in interfaces.items():
            if not (iface in relevant_ifaces):
                continue
            logger.debug("{Added %s} [%s]" % (iface, path))
            for name, value in props.items():
                logger.debug("      %s = %s" % (name, value))

            # Handle interfaces_added to create interfaces
            if iface == MEDIA_PLAYER_INTERFACE:
                self.mediaPlayer = MediaPlayer(self.bus)

    def interfaces_removed(self, path, interfaces):
        for iface in interfaces:
            if not (iface in relevant_ifaces):
                continue
            logger.debug("{Removed %s} [%s]" % (iface, path))

            # Handle interfaces_remove to delete interfaces
            if iface == MEDIA_PLAYER_INTERFACE:
                self.mediaPlayer = None


if __name__ == '__main__':
    '''		Demo	 '''
    import time
    # initialize Bluetooth instance
    bl = Bluetooth()
    time.sleep(3)

    # start bluetooth
    t = bl.open_bluetooth()
    t.start()

    # pause bluetooth music playing
    bl.pause_bluetooth_playing()

    # set bluetooth shown name
    bl.set_bluetooth_alias("Hello")

    # check bluetooth connection status
    isConnected, addr = bl.get_bluetooth_status()
    print(f"status: {isConnected}, {addr}")
    time.sleep(60)

    # close bluetooth
    bl.close_bluetooth()
