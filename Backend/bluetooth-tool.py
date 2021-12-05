#!/usr/bin/python
# SPDX-License-Identifier: LGPL-2.1-or-later

from __future__ import absolute_import, print_function, unicode_literals

from optparse import OptionParser
import sys
import dbus
import dbus.service
import dbus.mainloop.glib
try:
  from gi.repository import GLib
except ImportError:
  import Glib as GLib
import bluezutils

BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"

ADAPTER_INTERFACE = 'org.bluez.Adapter1'
relevant_ifaces = [ "org.bluez.Adapter1", "org.bluez.Device1" ]

bus = None
device_obj = None
dev_path = None

def ask(prompt):
	try:
		return raw_input(prompt)
	except:
		return input(prompt)

def set_trusted(path):
	props = dbus.Interface(bus.get_object("org.bluez", path),
					"org.freedesktop.DBus.Properties")
	props.Set("org.bluez.Device1", "Trusted", True)

def dev_connect(path):
	dev = dbus.Interface(bus.get_object("org.bluez", path),
							"org.bluez.Device1")
	dev.Connect()

def property_changed(interface, changed, invalidated, path):
	iface = interface[interface.rfind(".") + 1:]
	for name, value in changed.items():
		val = str(value)
		print("{%s.PropertyChanged} [%s] %s = %s" % (iface, path, name,
									val))

def interfaces_added(path, interfaces):
	for iface, props in interfaces.items():
		if not(iface in relevant_ifaces):
			continue
		print("{Added %s} [%s]" % (iface, path))
		for name, value in props.items():
			print("      %s = %s" % (name, value))

def interfaces_removed(path, interfaces):
	for iface in interfaces:
		if not(iface in relevant_ifaces):
			continue
		print("{Removed %s} [%s]" % (iface, path))


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

class Rejected(dbus.DBusException):
	_dbus_error_name = "org.bluez.Error.Rejected"

class Agent(dbus.service.Object):
	exit_on_release = True

	def set_exit_on_release(self, exit_on_release):
		self.exit_on_release = exit_on_release

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="", out_signature="")
	def Release(self):
		print("Release")
		if self.exit_on_release:
			mainloop.quit()

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="os", out_signature="")
	def AuthorizeService(self, device, uuid):
		print("AuthorizeService (%s, %s)" % (device, uuid))
		#authorize = ask("Authorize connection (yes/no): ")
		if (True):
			return
		raise Rejected("Connection rejected by user")

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="s")
	def RequestPinCode(self, device):
		print("RequestPinCode (%s)" % (device))
		set_trusted(device)
		return ask("Enter PIN Code: ")

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="u")
	def RequestPasskey(self, device):
		print("RequestPasskey (%s)" % (device))
		set_trusted(device)
		passkey = ask("Enter passkey: ")
		return dbus.UInt32(passkey)

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="ouq", out_signature="")
	def DisplayPasskey(self, device, passkey, entered):
		print("DisplayPasskey (%s, %06u entered %u)" %
						(device, passkey, entered))

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="os", out_signature="")
	def DisplayPinCode(self, device, pincode):
		print("DisplayPinCode (%s, %s)" % (device, pincode))

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="ou", out_signature="")
	def RequestConfirmation(self, device, passkey):
		print("RequestConfirmation (%s, %06d)" % (device, passkey))
		confirm = ask("Confirm passkey (yes/no): ")
		if (confirm == "yes"):
			set_trusted(device)
			return
		raise Rejected("Passkey doesn't match")

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="")
	def RequestAuthorization(self, device):
		print("RequestAuthorization (%s)" % (device))
		#auth = ask("Authorize? (yes/no): ")
		if (True):
			return
		raise Rejected("Pairing rejected")

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="", out_signature="")
	def Cancel(self):
		print("Cancel")
		

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	bus = dbus.SystemBus()

	capability = "NoInputNoOutput"

	path = "/test/agent"
	agent = Agent(bus, path)

	mainloop = GLib.MainLoop()

	obj = bus.get_object(BUS_NAME, "/org/bluez");
	manager = dbus.Interface(obj, "org.bluez.AgentManager1")
	
	manager.RegisterAgent(path, capability)

	# Start to get devices info
	# we need a dbus object manager
	obj = bus.get_object(BUS_NAME, "/")
	dbusManager = dbus.Interface(obj, "org.freedesktop.DBus.ObjectManager")
	objects = dbusManager.GetManagedObjects()
	devices = filter_by_interface(objects, "org.bluez.Device1")

	# event listener
	bus.add_signal_receiver(property_changed, bus_name="org.bluez",
			dbus_interface="org.freedesktop.DBus.Properties",
			signal_name="PropertiesChanged",
			path_keyword="path")

	bus.add_signal_receiver(interfaces_added, bus_name="org.bluez",
			dbus_interface="org.freedesktop.DBus.ObjectManager",
			signal_name="InterfacesAdded")

	bus.add_signal_receiver(interfaces_removed, bus_name="org.bluez",
			dbus_interface="org.freedesktop.DBus.ObjectManager",
			signal_name="InterfacesRemoved")


	print("Agent registered")

	manager.RequestDefaultAgent(path)

	mainloop.run()
	#adapter.UnregisterAgent(path)
	#print("Agent unregistered")