#!/usr/bin/env python

import glob
from collections import namedtuple
import os.path
import psutil
import threading

class FsScanner:
    """Class responsible for scanning the system for presence of FlySight device."""
    
    def __init__(self, onFlysight):
        """
        Initialized FsScanner object.
        
        Args:
          onFlysight: A callback taking a single FlySight object whenever a device
                      is found.
        """
        self._timer = threading.Timer(2, self.onTick)
        self._is_scanning = False
        self._callback = onFlysight
        self._already_plugged_in_flysights = set()
    
    
    def start(self):
        if self._is_scanning:
            return
        self._is_scanning = True
        self.timer.start()
        
    def stop(self):
        if not self._is_scanning:
            return
        self._is_scanning = False
        self.timer.cancel()
       
    def onTick(self):
        detected_flysights = set()
        for disk_entry in psutil.disk_partitions():
            if os.path.exists(os.path.join(disk_entry.mountpoint, "FLYSIGHT.TXT")):
                detected_flysights.add(disk_entry.mountpoint)
        
        for mountpoint in (detected_flysights - self._already_plugged_in_flysights):
            self._callback(FlySight(mountpoint))

        self._already_plugged_in_flysights = detected_flysights
        
                 
class FlySight:
    """A class for obtaining various info from mounted FlySight device."""
    
    def __init__(self, mountpoint):
        self._mountpoint = mountpoint
        
    def get_all_logs(self):
        """
        Returns a list of tuples corresponding to logs on this device.
        Each tuple consists of "name" and "path" fields.
        Name is stable and unique within a single device, path is absolute.
        """
        logs = glob.glob(os.path.join(
            self._mountpoint,
            "[0-9][0-9]-[0-9][0-9]-[0-9][0-9]/[0-9][0-9]-[0-9][0-9]-[0-9][0-9].CSV"))
        FlySightLogEntry = namedtuple("FlySightLogEntry", "name path")
        mountpoint_len = len(self._mountpoint)
        return [FlySightLogEntry(p[mountpoint_len:], p) for p in logs]
        
    