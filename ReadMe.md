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

Wiring pin 5 to ground, the device enters i2c mode.  Default
i2c address is 0x10.  Valid range of addresses are from 0x08
to 0x77.

The indicated FOV for the device is 2º.  To calculate the diameter of
required for object detection, the following formula can be used:

d = 2 ∗ D ∙ tanβ

Where d = diameter, D = distance of the object and β = 2º/2 (half of the FOV).
