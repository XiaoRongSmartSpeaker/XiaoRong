# ReachView code is placed under the GPL license.
# Written by Egor Fedorov (egor.fedorov@emlid.com)
# Copyright (c) 2015, Emlid Limited
# All rights reserved.

# If you are interested in using ReachView code as a part of a
# closed source project, please contact Emlid Limited (info@emlid.com).

# This file is part of ReachView.

# ReachView is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ReachView is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ReachView.  If not, see <http://www.gnu.org/licenses/>.

from asyncio.tasks import wait_for
import time
import pexpect
import subprocess
import sys
import logging
import re

logging.basicConfig(filename="bluetoothctl.log", filemode='w', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)

class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass


class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl", timeout=30 , echo = False)
        logging.info("bluetoothctl has started")

    def get_output(self, command = "", pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        if command != "":
            self.child.send(command + "\n")
        else:
            pass
        time.sleep(pause)
        
        status_index = self.child.expect(["#", "bluetooth", pexpect.TIMEOUT, pexpect.EOF])
        if status_index == 2:
            raise BluetoothctlError("Bluetoothctl timeout after running " + command)
        if status_index == 3:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)
        return self.child.before.decode("utf-8").split("\r\n")
    
    def start_scan(self):
        """Start bluetooth scanning process."""
        try:
            out = self.get_output("scan on")
        except BluetoothctlError as e:
            logging.error(e)
            return None
            
    def disable_passkey_authentication(self):
        try:
            logging.debug(self.get_output("agent off"))
            logging.debug(self.get_output("agent NoInputNoOutput"))
        except BluetoothctlError as e:
            logging.error(e)
        return None
    
    def make_discoverable(self):
        """Make device discoverable."""
        try:
            logging.debug(self.get_output("discoverable on"))
        except BluetoothctlError as e:
            logging.error(e)
            return None
    def make_pairable(self):
        """Make device pairable."""
        try:
            logging.debug(self.get_output("pairable on"))
        except BluetoothctlError as e:
            logging.error(e)
            return None

    def make_discoverable_off(self):
        """Make device discoverable."""
        try:
            logging.debug(self.get_output("discoverable off"))
        except BluetoothctlError as e:
            logging.error(e)
            return None
    def make_pairable_off(self):
        """Make device pairable."""
        try:
            logging.debug(self.get_output("pairable off"))
        except BluetoothctlError as e:
            logging.error(e)
            return None

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2]
                    }

        return device

    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        try:
            out = self.get_output("devices")
            logging.debug(out)
        except BluetoothctlError as e:
            logging.error(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            out = self.get_output("paired-devices")
        except BluetoothctlError as e:
            logging.error(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)

            return paired_devices

    def get_discoverable_devices(self):
        """Filter paired devices out of available."""
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]

    def get_device_info(self, mac_address):
        """Get device info by mac address."""
        try:
            out = self.get_output("info " + mac_address)
        except BluetoothctlError as e:
            logging.error(e)
            return None
        else:
            return out

    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            out = self.get_output("pair " + mac_address, 4)
        except BluetoothctlError as e:
            logging.error(e)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def remove(self, mac_address):
        """Remove paired device by mac address, return success of the operation."""
        try:
            out = self.get_output("remove " + mac_address, 3)
        except BluetoothctlError as e:
            logging.error(e)
            return None
        else:
            res = self.child.expect(["not available", "Device has been removed", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address, 2)
        except BluetoothctlError as e:
            logging.error(e)
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def disconnect(self, mac_address):
        """Try to disconnect to a device by mac address."""
        try:
            out = self.get_output("disconnect " + mac_address, 2)
        except BluetoothctlError as e:
            logging.error(e)
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False
            return success
    def wait_for_connection(self, timeout=60):
        try:
            self.child.timeout = timeout
            index = self.child.expect([pexpect.TIMEOUT, "Connected: yes", "Connected: no"])
            if index == 0:
                logging.info("pexpect timeout exceed. ")
                return None
            elif index == 1:
                out = self.child.before.decode("utf-8")
                search = re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", out)
                logging.debug(self.child.before.decode("utf-8"))
                if search:
                    device_mac_address = search.group(0)
                    #self.authorize_service()
                    return device_mac_address
                else:
                    logging.warning(f"bluetoothctl msg:\"{out}\". Device mac address not found.")
                    raise BluetoothctlError(f"bluetoothctl msg:\"{out}\". Device mac address not found.")
            elif index == 2:
                
                logging.debug(self.child.before.decode("utf-8"))
                logging.info("Connection unsuccessful.")
                return None
        except BluetoothctlError as e:
            logging.error(e)
            return None
    def authorize_service(self):
        try:
            index = self.child.expect(["Authorize service", pexpect.TIMEOUT])
            if index == 0:
                out = self.get_output("yes")
            else:
                logging.info("No need to authorize.")
            return None
        except BluetoothctlError as e:
            logging.error(e)
            return None
if __name__ == "__main__":
    ### Initialize
    print("Init bluetooth...")
    bl = Bluetoothctl()
    print("Initialize bluetooth done!")

    ### Disconnect from connected 
    print("Getting available device")
    devices = bl.get_available_devices()
    if devices:
        for device in devices:
            print(f"Disconnecting {device['name']}... ")
            bl.disconnect(device["mac_address"])

    ### Make discoverable and pairable
    bl.disable_passkey_authentication()      
    bl.make_discoverable()
    bl.make_pairable()
    print("Ready to pair!")

    ### Wait for connection
    deviceMacAddress = bl.wait_for_connection()
    if deviceMacAddress:
        logging.debug(bl.get_output(f"trust {deviceMacAddress}"))
        print(f"Success. Connected to {deviceMacAddress}")
    else:
        print("Fail to connect")

    ### Turn off bluetooth discoverable and pairable
    bl.make_discoverable_off()
    bl.make_pairable_off()

