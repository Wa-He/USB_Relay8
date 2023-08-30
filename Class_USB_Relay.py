# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 09:26:27 2023

@author: Henning Wache

class to easily control USB Relay device from www.dcttech.com
using pyusb library

###############################################################################
# example code / how to use:

# create Object and start the device 
# starting is not required but makes sure that all channels are reset
USBRelay8 = USBRelay8() 
USBRelay8.start_device()

# status bytes carry information of the name and currently active channels (last byte)
received_data = USBRelay8.get_status()

# opening all 8 channels at once
USBRelay8.open_all_channells()

# closes single relay channel, i.e. 1
USBRelay8.close_channel(1)

# check status of single channel, i.e. number 1
print(USBRelay8.channel1)

# check status of all channels as dictionary
channel_status_dict = USBRelay8.get_channel_status()

# closes all channels
USBRelay8.close_all_channels()    
"""
import usb.core
import usb.util
import usb.backend.libusb1  # Import the appropriate backend
# Set the backend
usb.core.find(backend=usb.backend.libusb1.get_backend())

class USBRelay8():
    def __init__(self):
        idVendor = 5824
        idProduct = 1503
        # find device with ids
        self.device = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        if self.device is None:
            raise ValueError("USB device not found")
        # set device configuration
        self.device.set_configuration()
        usb.util.dispose_resources(self.device)
        # initialize input/output request types
        self.request_type_out = usb.util.CTRL_TYPE_CLASS | usb.util.CTRL_OUT
        self.request_type_in = usb.util.CTRL_TYPE_CLASS | usb.util.CTRL_IN
    
    def send_request(self, request_type, request, value, index, data_or_length):
        '''
        request_type : 'OUT'/'IN'
        request : 0x1 status, 0x9 open/close
        value : 0x300 status/open/close
        '''
        if request_type=='IN':
            request_type = self.request_type_in
        elif request_type=='OUT':
            request_type = self.request_type_out
        else:
            print('USB_Relay.send_request()', 'Invalid request_type!')
            return None
        #try:
        if True:
            received_data = self.device.ctrl_transfer(request_type, request, value, index, data_or_length)
        #except Exception as e:
            #print('USB_Relay.send_request()', e)
        return received_data
    
    def get_status(self):
        '''
        Reads status from device and checks status of channels. Returns status byte array. 
        # annotation:
        # possible request, value to get status via crtl_transfer with index=0 and data_or_length=0x8
        # 769, 768 ## 513, 768 ## 257, 768 ## 1, 768
        # value numbers up to 1023 are possible but return the difference to 768 as first byte
        '''
        received_data = self.device.ctrl_transfer(self.request_type_in, 0x1, 0x300, 0, 0x8)
        #print('status:', received_data)
        return received_data
    
    def set_channels(self, received_data=None):
        '''
        Updates channel variables to get current relay states. 1 (open), 0 (closed)
        '''
        if not received_data:
            received_data = self.get_status()
        binary_data = format(received_data[-1], 'b').rjust(8, '0')
        for ii, bit in enumerate(binary_data):
            if ii==7:
                self.channel1 = int(bit)
            if ii==6:
                self.channel2 = int(bit)
            if ii==5:
                self.channel3 = int(bit)
            if ii==4:
                self.channel4 = int(bit)
            if ii==3:
                self.channel5 = int(bit)
            if ii==2:
                self.channel6 = int(bit)
            if ii==1:
                self.channel7 = int(bit)
            if ii==0:
                self.channel8 = int(bit)
    
    def start_device(self):
        '''
        Closes all open channels to enable correct communication. Returns status byte array.
        '''
        received_data = USB_Relay.get_status()
        if received_data[-1]!=0:
            USB_Relay.close_all_channels()
            print('There were open channels. Closing now and trying again!')
            USB_Relay.open_device()
        else:
            print('Initialized USB Relay...', 'Hello', ''.join(chr(code) for code in received_data))
        self.set_channels(received_data)
        return received_data
    
    def open_all_channells(self):
        '''
        Opens all channels. Returns number of bytes sent.
        '''
        sent_bytes = self.device.ctrl_transfer(self.request_type_out, 0x9, 0x300, 0, 
                                               bytes.fromhex('FE 00 00 00 00 00 00 00'))
        self.set_channels()
        return sent_bytes
    
    def close_all_channels(self):
        '''
        Closes all channels. Returns number of bytes sent.
        '''
        sent_bytes = self.device.ctrl_transfer(self.request_type_out, 0x9, 0x300, 0, 
                                               bytes.fromhex('FC 00 00 00 00 00 00 00'))
        self.set_channels()
        return sent_bytes
    
    def open_channel(self, channel_num):
        '''
        Opens a specified channel. Returns number of bytes sent.
        '''
        channel_num = int(abs(channel_num))
        sent_bytes = self.device.ctrl_transfer(self.request_type_out, 0x9, 0x300, 0, 
                                               bytes.fromhex(f'FF 0{channel_num} 00 00 00 00 00 00'))
        self.set_channels()
        return sent_bytes
    
    def close_channel(self, channel_num):
        '''
        Closes a specified channel. Returns number of bytes sent.
        '''
        channel_num = int(channel_num)
        sent_bytes = self.device.ctrl_transfer(self.request_type_out, 0x9, 0x300, 0, 
                                               bytes.fromhex(f'FD 0{channel_num} 00 00 00 00 00 00'))
        self.set_channels()
        return sent_bytes
    
    def get_channel_status(self):
        '''
        Returns a dictionary with information about the status on/off of each channel.
        '''
        self.set_channels()
        channel_status = {'Channel 1': self.channel1, 'Channel 2': self.channel2, 
                          'Channel 3': self.channel1, 'Channel 4': self.channel2, 
                          'Channel 5': self.channel1, 'Channel 6': self.channel2, 
                          'Channel 7': self.channel1, 'Channel 8': self.channel2}
        
        return channel_status


        