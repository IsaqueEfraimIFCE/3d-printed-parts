# ESP32 + Accelerometer Case: Specifications

## Electronics
| Part | Choice | Size | Why |
|---|---|---|---|
| MCU | ESP32-C3 SuperMini | 22.5 x 18 x ~3.5 mm | Tiny, cheap, native USB-C, Wi-Fi + BLE |
| Accelerometer | GY-521 (MPU-6050, 3-axis accel + 3-axis gyro) | 21.2 x 15.6 mm, 2x 3 mm holes | Very common, I2C, lots of libraries |

### Wiring (I2C)
| GY-521 | ESP32-C3 SuperMini |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SDA | GPIO8 |
| SCL | GPIO9 |
| INT (optional) | GPIO3 |

Solder the wires directly to the boards (no pin headers). Headers will not fit under the lid.

## Enclosure
- **Outside size:** 60 x 32 x 16 mm base, plus a 2 mm lid, so 60 x 32 x 18 mm assembled.
- **Walls:** 2 mm walls, 2 mm floor, 2 mm lid. The lid has a 3 mm locating lip with 0.25 mm clearance per side.
- **ESP32 bay:** the board sits on two 2 mm side ledges and is held against the USB wall by a rear fence. There is a USB-C cutout (9 x 3.2 mm, rounded) in the −X wall.
- **Accelerometer bay:** 2x M2 screw bosses, 4 mm tall, 15.24 mm apart, plus a support pad. The sensor is screwed down firmly so the readings aren't affected by the board rattling.
- **Lid:** 4 corner M2 screws with recessed heads, 2x 3 mm pin-poke holes for BOOT/RST, and 4 vent slots.
- **Fasteners:** 6x M2 self-tapping screws: 4x M2x6 for the lid and 2x M2x4 for the sensor. The pilot holes are 1.8 mm.

## Printing
- **Material:** PLA or PETG. Use PETG if the case will get warm or sit outside.
- **Settings:** 0.2 mm layers, 3 perimeters, 20% infill. No supports needed.
- **Orientation:** print `case_base.stl` with the open side up. `case_lid.stl` is already flipped so its flat face is down.
- **Filament:** about 15 cm³ of plastic in total (~19 g PLA).

## Files
- `case_base.stl`, `case_lid.stl`: the printable parts.
- `make_case.py`: the parametric source (Python + trimesh/manifold3d). Change the dimensions and run `python make_case.py` to rebuild the STLs.

## Verify before printing
Clone boards vary. Measure yours and adjust `make_case.py` if needed:
- SuperMini BOOT/RST button position (the lid holes are at x=8, y=11/21)
- GY-521 hole spacing (15.24 mm) and edge offset (2.54 mm)
