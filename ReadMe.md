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

### Set Frame Rate

### Set Low Power Mode

## Triggered Mode Operations

### Set Triggered Mode

### Trigger Reading

## Disable Lidar

### Disable Device

### Enable Device

## Thresholds

### Amplitude Threshold

### Dummy Distance

### Distance Limits



