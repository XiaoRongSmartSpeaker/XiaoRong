#!/bin/bash

sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
