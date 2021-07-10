# TF-Luna i2C Driver
### Python Driver for Raspberry Pi


Accuracy as specified in the manual for version A03:
At 100Hz output rate:

| Amp |  100  |  200  |  400  |  1000  | >=2000  |
| ----|-------|-------|-------|--------|---------|
| STD  |  3cm  |  3cm  |  2cm  |  1cm   | 0.5cm   |

Distances under 20cm are unreliable.  Reflectivity of
objects of 10% reduce the range to 0.2-2.5m (i.e. black
objects).  90% reflectivity increases the range to 0.2-8m.

Pins are numbered 1-6 from left to right, when lens is pointed
upwards.


| No.  | Function    | Description          |
|------|-------------|----------------------|
|  1   |  +5V        |  Power Supply        |
|  2   |  RXD/SDA    |  Receiving/Data      |
|  3   |  TXD/SCL    |  Transmitting/Clock  |
|  4   |  GND        |  Ground              |
|  5   |  Config in  |  Ground i2c mode     |
|      |             |  3.3V serial mode    |
|  6   |  Multiplex  |  on/off mode output  |
|      |  output     |  i2c mode: data      |
|      |             |  available signal    |

Wiring pin 5 to ground, the device enters i2c mode.  Default i2c address is 0x10.  Valid range of addresses are from 0x08 to 0x77.

The indicated FOV for the device is 2º.  To calculate the diameter of required for object detection, the following formula can be used:

d = 2 ∗ D ∙ tanβ

Where d = diameter, D = distance of the object and β = 2º/2 (half of the FOV).

## Usage

### Setting i2c Slave Address

By default, the new instance of TfLunaI2C will instantiate with the factory default address 0x10 and will  use imperial units for measurements.  In general settings need to be saved and the system reboot in order for the new settings to take effect.  For a change in the i2c slave address, however, this is updated immediately.  The driver updates this setting internally so subsequent calls (i.e., save()) can be performed. 
```
import time
from TfLunaI2C import TfLunaI2C

tfluna = TfLunaI2C()
tfluna.write_address(0x11)
tfluna.save()
tfluna.reboot()
time.sleep(2)
print(tfluna)
```

If the slave address has been altered or the desired units are to be metric, then the driver can be instantiated as follows.  This will load with a non-default address and will use metric units in data displays.
```
from TfLunaI2C import TFLunaI2C

tfluna = TfLunaI2C(0x08, False)
print(tfluna)
```

### Retrieving Data

In continuous mode, the device will take measurements at the specified frequency setting (between 1Hz-250Hz) with the factory default rate of 100Hz.  If you monitor pin 6 on the device, this go high when data is ready for reading and the following method can be invoked.
```
from TfLunaI2C import TFLunaI2C

tfluna = TfLunaI2C()
tfluna.read_data()
tfluna.print_data()
```
Output of the print_data() method will resemble the following:
```
distance:    12.3031496063 ft
amplitude:   1711
temperature: 118.4 Fahrenheit
ticks:       11594
error:       0
----------------------------------------
```
Data is stored in the instance and can be accessed directly after reads:
```
distance = tfluna.dist
amplitude = tfluna.amp
temperature = tfluna.temp
ticks = tfluna.ticks
error = tfluna.error
```
The above values are raw values and conversion may be desired.  The following outlines the specific properties:
* distance = integer representing centimeters
* amplitude = integer values between 100-3000 should be regarded as reliable
* temperature = integer:  Multiply by 0.01 to compute temperature in Celsius.
* ticks = integer representing ticks since startup.  This is a 16bit integer and will overflow at 65536 (0xFFFF)
* error = integer representing the error reading on the last data retrieval

Calculation of Fahrenheit: (0.018 * temperature) + 32.0

Calculation of feet: distance * 0.032808398950131

TODO: The following indicates a place holders for documentation

## Continuous Mode Operations

### Set Continuous Mode
To set into continuous mode (default configuration) perform the following.  This sets the device to scan at the specified frequency configured.
```
from TfLunaI2C import TFLunaI2C

tfluna = TfLunaI2C()
tfLuna.set_mode_continuous()
tfLuna.save()
tfLuna.reboot()
```
### Set Frame Rate
The frame rate is utilized when the device is in continuous mode.  Valid rates are 1Hz to 250Hz.  The rate is specified in as an integer value.  100Hz is the default frame rate from the factory.  Frame rates between 1-10Hz are utilized in Low Power mode.  If the device is in triggered mode, this value is ignored.

Several frame rates have been defined for usage:
####FPS (Low Power Mode)
* FPS_1  = 1Hz
* FPS_2  = 2Hz
* FPS_3  = 3Hz
* FPS_4  = 4Hz
* FPS_5  = 5Hz
* FPS_6  = 6Hz
* FPS_7  = 7Hz
* FPS_8  = 8Hz
* FPS_9  = 9Hz
* FPS_10 = 10Hz

####FPS (High Power Mode)
* FPS_25  = 25Hz
* FPS_35  = 35Hz
* FPS_50  = 50Hz
* FPS_100 = 100Hz (Default)
* FPS_125 = 125Hz
* FPS_166 = 166Hz
* FPS_250 = 250Hz

```
from TfLunaI2C import TFLunaI2C

tfluna = TfLunaI2C()
tfLuna.set_frame_rate(TfLunaI2C.FPS_50)
tfLuna.save()
tfLuna.reboot()
```

### Set Low Power Mode
Set device into low power mode.  Additionally insure that the frame rate is set to a supported frequency (1Hz - 10Hz).
```
tfluna = TfLunaI2C()
tfLuna.set_low_power_mode()
tfLuna.save()
tfLuna.reboot()
```
## Triggered Mode Operations
Set device into triggered mode (default state).  Additionally, setting an appropriate frequency should be configured (1hz-250Hz).
### Set Triggered Mode
```
tfluna = TfLunaI2C()
tfLuna.set_mode_triggered()
tfLuna.save()
tfLuna.reboot()
```
### Trigger Reading
Trigger reading is used to initiate a one-shot Lidar reading.  This would be useful in the case that your script is running checks on a frequency determined by your software application.
```
tfluna = TfLunaI2C()
tfLuna.trigger()
# You may want to wait until pin 6 indicates data is ready
tfluna.read_data()
tfluna.print_data()
```

## Disable Lidar

### Disable Device
Disables Lidar on the device - documentation is unclear if this requires a reboot like other settings, however, it would make more sense if it did not require that for any use case that seems apparent (i.e, power preservation, or temperature reduction). 
```
tfluna = TfLunaI2C()
tfLuna.set_disabled()
tfLuna.save()
```
### Enable Device
Enable Lidar on the device - see Disable Device for additional notes.
```
tfluna = TfLunaI2C()
tfLuna.set_enabled()
tfLuna.save()
```
## Thresholds

### Amplitude Threshold
Amplitude has a range between 0-32768.  By default, this threshold is set to 100 (the recommended value).  When a value from the device is returned that is below this threshold, the dummy distance will be returned.  This can be adjusted using the following example. 

The TF-Luna manual has contradictory information on this, however.  The serial interface indicates this should be set using a single byte which will be multilied by 10 (giving a range between 0-2550 in increments of 10).  The registers in i2c are 2 bytes.  This is not really a contradiction, but it raises several questions about how this is implemented.  We are operating here under the assumption that the serial interface uses 1 byte for this value purely to reduce the message size rather than a limitation of what the device will support.
```
tfluna = TfLunaI2C()
tfLuna.set_amp_threshold(150)
tfLuna.save()
tfLuna.reboot()
```

### Dummy Distance
When the amplitude threshold is not met, the value set in the dummy distance will be passed back from the device as the distance reading.  By default this is set to 0.  It is not clear from the documentation what the full range of supported values are so we are assuming 0x0000 - 0xFFFF.
```
tfluna = TfLunaI2C()
tfLuna.set_dummy_distance(0)
tfLuna.save()
tfLuna.reboot()
```
### Distance Limits
Distance limits sets the minimum and maximum distances from the device.  By default this is set to 0cm - 900cm.  The manual indicates that 20cm - 800cm is the most reliable.  The documentation does not indicate how these settings are utilized, so some experimentation will need to be performed to determine what the general effects of this will be.
```
tfluna = TfLunaI2C()
tfLuna.set_distance_limits(20,800)
tfLuna.save()
tfLuna.reboot()
```
## Unsupported Features

### Features Not Available in i2c
#### On/Off Mode
This appears to only be available in serial mode.  The primary function is to set a distance, a distance on which to trigger readings.  In addition to this distance a zone and two delay settings are required for accuracy.

#### Single Frequency Mode
This appears to only be available in serial mode.  The unit is in dual frequency mode by default.  According to the documentation there are specific use cases where single mode may benifit the readings.

#### Distance Limit Silence
When setting distance limits in serial mode, there is a 5th byte passed to the device indicating the silence setting.  Unfortunately this is not currently implemented in i2c.  This setting suppresses output when distances are out of the specified range.

#### Frequency Calibration
This is a new feature in firmware 3.0.7 but is currently only available in serial mode.  Operation appears to take about 2 seconds to complete.

## Unimplemented Features

### Features Available for i2c but Not Implemented
The following features have not been implemented currently and will be developed in the near future.

#### Ultra Low Power Mode
The ultra low power mode is a mode that puts the device asleep to reduce power utilization.  In this mode, the device needs to be sent a basic read operation to wake from sleep.  Upon waking, pin 6 is set to high by the device in order to indicate it is ready for a command.  A command must be issued within 6ms in order to keep awake.  At this point a trigger of a reading would be appropriate and a subsequent read of the data once the reading is complete (pin 6 high again).  

#### Firmware Verification of Operations
Although this is not a feature implementation, it would make sense to add error checking throughout for features not implemented in earlier firmware versions.
