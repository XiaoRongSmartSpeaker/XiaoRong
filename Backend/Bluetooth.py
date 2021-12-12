#!/usr/bin/python
# SPDX-License-Identifier: LGPL-2.1-or-later

from __future__ import absolute_import, print_function, unicode_literals

import sys
import logging
import threading
import dbus
import dbus.service
import dbus.mainloop.glib
try:
	from gi.repository import GLib
except ImportError:
	import Glib as GLib

logger = logging.getLogger()
fileHandler = logging.FileHandler("bluetooth.log")
streamHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.setLevel(logging.DEBUG)

BUS_NAME = 'org.bluez'
SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"
AGENT_INTERFACE = SERVICE_NAME + ".Agent1"
AGENT_MANAGER_INTERFACE = SERVICE_NAME + ".AgentManager1"
AGENT_PATH = "/xiaorong/agent"
DEVICE_PATH = "/xiaorong/device"
ADAPTER_ROOT = '/org/bluez/hci'

relevant_ifaces = [
    "org.bluez.Adapter1", "org.bluez.Device1", "org.bluez.MediaPlayer1"
]


def ask(prompt):
	try:
		return raw_input(prompt)
	except:
		return input(prompt)


def set_trusted(path, bus):
	props = dbus.Interface(bus.get_object("org.bluez", path),
	                       "org.freedesktop.DBus.Properties")
	props.Set("org.bluez.Device1", "Trusted", True)


def dev_connect(path, bus):
	dev = dbus.Interface(bus.get_object("org.bluez", path),
	                     "org.bluez.Device1")
	dev.Connect()


def proxyobj(bus, path, interface):
	""" commodity to apply an interface to a proxy object """
	obj = bus.get_object('org.bluez', path)
	return dbus.Interface(obj, interface)


def filter_by_interface(objects, interface_name):
	""" filters the objects based on their support
		for the specified interface """
	result = []
	for path in objects.keys():
		interfaces = objects[path]
		for interface in interfaces.keys():
			if interface == interface_name:
				result.append(path)
	return result


def get_managed_objects():
	bus = dbus.SystemBus()
	manager = dbus.Interface(bus.get_object("org.bluez", "/"),
	                         "org.freedesktop.DBus.ObjectManager")
	return manager.GetManagedObjects()


def find_adapter(pattern=None):
	return find_adapter_in_objects(get_managed_objects(), pattern)


def find_adapter_in_objects(objects, pattern=None):
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


def find_device(device_address, adapter_pattern=None):
	return find_device_in_objects(get_managed_objects(), device_address,
	                              adapter_pattern)


def find_device_in_objects(objects, device_address, adapter_pattern=None):
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
		self.deviceConnected = False

	@dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
	def Release(self):
		print("Release")
		if self.exit_on_release:
			self.mainloop.quit()

	@dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
	def AuthorizeService(self, device, uuid):
		print("AuthorizeService (%s, %s)" % (device, uuid))
		#authorize = ask("Authorize connection (yes/no): ")
		if (True):
			return
		raise Rejected("Connection rejected by user")

	@dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
	def RequestPinCode(self, device):
		print("RequestPinCode (%s)" % (device))
		set_trusted(device, self.bus)
		return ask("Enter PIN Code: ")

	@dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
	def RequestPasskey(self, device):
		print("RequestPasskey (%s)" % (device))
		set_trusted(device, self.bus)
		passkey = ask("Enter passkey: ")
		return dbus.UInt32(passkey)

	@dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
	def DisplayPasskey(self, device, passkey, entered):
		print("DisplayPasskey (%s, %06u entered %u)" %
		      (device, passkey, entered))

	@dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
	def DisplayPinCode(self, device, pincode):
		print("DisplayPinCode (%s, %s)" % (device, pincode))

	@dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
	def RequestConfirmation(self, device, passkey):
		print("RequestConfirmation (%s, %06d)" % (device, passkey))
		confirm = ask("Confirm passkey (yes/no): ")
		if (confirm == "yes"):
			set_trusted(device, self.bus)
			return
		raise Rejected("Passkey doesn't match")

	@dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
	def RequestAuthorization(self, device):
		print("RequestAuthorization (%s)" % (device))
		#auth = ask("Authorize? (yes/no): ")
		if (not self.deviceConnected):
			return
		raise Rejected("Pairing rejected")

	@dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
	def Cancel(self):
		print("Cancel")


class Adapter(dbus.service.Object):
	def __init__(self, conn=None, object_path=None, bus_name=None, idx=0):
		super(self.__class__, self).__init__(conn, object_path, bus_name)
		self.bus = conn
		self.path = f'{ADAPTER_ROOT}{idx}'
		self.adapterProps = proxyobj(self.bus, self.path,
		                             dbus.PROPERTIES_IFACE)

	def make_power_on(self):
		self.adapterProps.Set(ADAPTER_INTERFACE, 'Powered', True)

	def make_power_off(self):
		self.adapterProps.Set(ADAPTER_INTERFACE, 'Powered', False)

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


class Device():
	def __init__(self, bus):
		self.bus = bus

		# Disconnect connected devices
		connectedDevicesList = self.get_connected_devices_list()
		for device in connectedDevicesList:
			self.disconnect(device["address"], device["name"])

	def disconnect(self, address, name=None):
		device = find_device(address)
		device.Disconnect()
		if name != None:
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
			obj = proxyobj(self.bus, deviceObj,
			               'org.freedesktop.DBus.Properties')
			if obj.Get(DEVICE_INTERFACE, "Connected"):
				connectedDevicesObj.append({
				    "name":
				    str(obj.Get("org.bluez.Device1", "Name")),
				    "address":
				    str(obj.Get("org.bluez.Device1", "Address")),
				    "connected":
				    str(obj.Get("org.bluez.Device1", "Connected"))
				})
		return connectedDevicesObj


class Player():
	def __init__(self, bus):
		self.bus = bus
		self.player_iface = None
		self.transport_prop_iface = None
		for path, ifaces in get_managed_objects().items():
			if 'org.bluez.MediaPlayer1' in ifaces:
				self.player_iface = dbus.Interface(
				    self.bus.get_object('org.bluez', path),
				    'org.bluez.MediaPlayer1')
			elif 'org.bluez.MediaTransport1' in ifaces:
				self.transport_prop_iface = dbus.Interface(
				    self.bus.get_object('org.bluez', path),
				    'org.freedesktop.DBus.Properties')
		if not self.player_iface:
			logger.error('Media Player not found.')
			return None
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

		# Main loop setting
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		self.mainloop = GLib.MainLoop()

		# Bus initialize
		self.bus = dbus.SystemBus()

		# Adpater initialize
		self.adapter = Adapter(self.bus)

		# Device initialize
		self.device = Device(self.bus)

		# Agent Initialize
		self.agent = Agent(conn=self.bus,
		                   object_path=AGENT_PATH,
		                   mainloop=self.mainloop)

		# Agent manager initialize
		self.manager = proxyobj(self.bus, "/org/bluez",
		                        AGENT_MANAGER_INTERFACE)

		## Register Agent
		self.manager.RegisterAgent(AGENT_PATH, capability)
		logger.info("Agent registered")

		# MediaPlayer Initialize
		self.player = None

		# Listener initialize
		self.__init_listener()

	def __init_listener(self):
		# Event listener
		self.bus.add_signal_receiver(
		    self.property_changed,
		    bus_name="org.bluez",
		    dbus_interface="org.freedesktop.DBus.Properties",
		    signal_name="PropertiesChanged",
		    path_keyword="path")

		self.bus.add_signal_receiver(
		    self.interfaces_added,
		    bus_name="org.bluez",
		    dbus_interface="org.freedesktop.DBus.ObjectManager",
		    signal_name="InterfacesAdded")

		self.bus.add_signal_receiver(
		    self.interfaces_removed,
		    bus_name="org.bluez",
		    dbus_interface="org.freedesktop.DBus.ObjectManager",
		    signal_name="InterfacesRemoved")

	def open_bluetooth(self):
		# adapter setting
		self.adapter.make_power_on()
		self.adapter.make_pairable()
		self.adapter.make_discoverable()
		#self.mainloop.run()
		t = threading.Thread(target=self.mainloop.run)
		t.start()
		return t

	def close_bluetooth(self):
		self.adapter.make_power_off()
		self.manager.UnregisterAgent(AGENT_PATH)
		self.mainloop.quit()

	def get_bluetooth_status(self):
		connectedDevicesList = self.device.get_connected_devices_list()
		if len(connectedDevicesList) > 1:
			logging.error("Multiple bluetooth devices connected.")
			raise BluetoothError
		elif len(connectedDevicesList) == 1:
			return True, connectedDevicesList[0]["address"]
		else:
			return False, None

	def pause_bluetooth_playing(self):
		try:
			if self.player:
				self.player.pause()
				logger.info("Pause bluetooth device's music")
			else:
				logger.error("Bluetooth's Media Player not found.")
				return 0
		except BluetoothError as e:
			logger.critical(f"Bluetooth.pause_bluetooth_playing failed, {e}")

	def play_bluetooth_playing(self):
		try:
			if self.player:
				self.player.play()
				logger.info("Pause bluetooth device's music")
			else:
				logger.error("Bluetooth's Media Player not found.")
				return 0
		except BluetoothError as e:
			logger.critical(f"Bluetooth.pause_bluetooth_playing failed, {e}")

	def property_changed(self, interface, changed, invalidated, path):
		iface = interface[interface.rfind(".") + 1:]
		for name, value in changed.items():
			val = str(value)
			logger.debug("{%s.PropertyChanged} [%s] %s = %s" %
			             (iface, path, name, val))
			# Event handling
			if name == "Volume":  # Volume change
				self.volume_change(value)
			elif iface == "Device1" and name == "Connected" and value == "1":  # Device connected
				self.agent.deviceConnected = True
			elif iface == "Device1" and name == "Connected" and value == "0":  # Device disconnected
				self.agent.deviceConnected = False

	def interfaces_added(self, path, interfaces):
		for iface, props in interfaces.items():
			if not (iface in relevant_ifaces):
				continue
			logger.debug("{Added %s} [%s]" % (iface, path))
			for name, value in props.items():
				logger.debug("      %s = %s" % (name, value))

			# Handle interfaces_added to create interfaces
			if iface == "org.bluez.MediaPlayer1":
				self.player = Player(self.bus)

	def interfaces_removed(self, path, interfaces):
		for iface in interfaces:
			if not (iface in relevant_ifaces):
				continue
			logger.debug("{Removed %s} [%s]" % (iface, path))

			# Handle interfaces_remove to delete interfaces
			if iface == "org.bluez.MediaPlayer1":
				self.player = None

	def volume_change(self, volume):
		# TODO: link to system volume change
		# add_thread(set_system_volume, volume)
		pass


if __name__ == '__main__':
	import time
	bl = Bluetooth()
	time.sleep(10)
	t = bl.open_bluetooth()
	#time.sleep(30)
	bl.pause_bluetooth_playing()
	#isConnected, addr = bl.get_bluetooth_status()
	#logging.info(f"status: {isConnected}, {addr}")
	time.sleep(30)
	bl.close_bluetooth()
