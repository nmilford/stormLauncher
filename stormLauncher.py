#!/usr/bin/python

# Copyright 2012, Nathan Milford

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The following script will control the Dream Cheeky Storm & Thunder USB
# Missile Launchers.  There are a few projects for using older launchers
# in Linux, but I couldn't find any for this launcher, so... enjoy.

# Thunder: http://www.dreamcheeky.com/thunder-missile-launcher
# O.I.C Storm: http://www.dreamcheeky.com/storm-oic-missile-launcher

# This script requires PyUSB 1.0+, apt in Debian/Ubuntu installs 0.4.
# Also, unless you want to toggle with udev rules, it needs to be run as root

# Use w, s, x and d to aim.  Sse the left shift button to fire.

import os
import sys
import time
import usb.core
from Tkinter import *

class launchControl(Frame):
   def __init__(self):
      self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
      if self.dev is None:
         raise ValueError('Launcher not found.')
      if self.dev.is_kernel_driver_active(0) is True:
         self.dev.detach_kernel_driver(0)
      self.dev.set_configuration()

      Frame.__init__(self)
      self.pack()
      self.master.title("Launch Control")
      self.master.geometry("250x25")

      self.message1 = StringVar()
      self.line1 = Label(self, textvariable = self.message1)
      self.message1.set("Aim (w/s/a/f) & Fire (left shift)!")
      self.line1.pack()

      self.message2 = StringVar()
      self.line2 = Label(self, textvariable = self.message2 )
      self.message2.set("")
      self.line2.pack()

      self.master.bind("<KeyPress>", self.keyPressed)
      self.master.bind("<KeyRelease>", self.keyReleased)

      self.master.bind("<KeyPress-Shift_L>", self.shiftPressed)
      self.master.bind("<KeyRelease-Shift_L>", self.shiftReleased)

   def keyPressed(self, event):
      if event.char == "w" or event.char == "W":
         self.message1.set("Turret Up.")
         self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00]) 
      elif event.char == "s" or event.char == "S":
         self.message1.set("Turret Down.")
         self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00])
      elif event.char == "a" or event.char == "A":
         self.message1.set("Turret Left.")
         self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00])
      elif event.char == "d" or event.char == "D":
         self.message1.set("Turret Right.")
         self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00])
   
   def keyReleased(self, event):
      self.message1.set("Turret Idle.")
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00])
   
   def shiftPressed(self, event):
      self.message1.set("FIRE!")
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00])

   def shiftReleased(self, event):
      self.message1.set("Turret Idle.")

if __name__ == '__main__':
   if not os.geteuid() == 0:
       sys.exit("Script must be run as root.")
   launchControl().mainloop()
