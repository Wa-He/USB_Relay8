# USB Relay

Simple example class to control dcttech.com USB Relay.

## example code / how to use:

Create the object and start the device. starting is not required but makes sure that all channels are reset
```
USBRelay8 = USBRelay8() 
USBRelay8.start_device()
```

status bytes carry information of the name and currently active channels (last byte)
```
received_data = USBRelay8.get_status()
```
opening all 8 channels at once
```
USBRelay8.open_all_channells()
```
closes single relay channel by number, e.g. channel 2
```
USBRelay8.close_channel(2)
```
check status of single channel, e.g. channel 3
```
print(USBRelay8.channel3)
```
check status of all channels as dictionary
```
channel_status_dict = USBRelay8.get_channel_status()
```
closes all channels
```
USBRelay8.close_all_channels()  
```
