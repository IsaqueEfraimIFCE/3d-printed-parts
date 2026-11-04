# Water-Tank Ultrasonic Probe Clamp

## Sensor (assumed)
The design assumes a **JSN-SR04T / AJ-SR04M style** waterproof probe:
- probe body about 18 mm across, fitting an 18.4 mm hole
- front flange about 23 mm across
- driver board separate, on a cable (the board stays outside the clamp)

**Measure your probe before printing.** If it differs, edit `PROBE_D` in `make_clamp.py` and run `python make_clamp.py`.

## Parts
| File | Size (mm) | Qty | Notes |
|---|---|---|---|
| clamp_frame.stl | 178 x 74 x 24 | 1 | C-frame with a threaded boss for the screw and a square socket at the arm tip |
| clamp_screw.stl | 34 x 34 x 71 | 1 | 16 mm printed screw (3 mm pitch) with a knurled knob and a rounded tip |
| probe_holder.stl | 45 x 30 x 22 | 1 | Probe cup with a square tongue; the same shape top and bottom, so it can be flipped |
| lock_pin.stl | 7 x 18.5 | 1 | Holds the holder in the socket. An M3x20 screw can be used instead |

## Mechanics
- **Wall thickness:** the clamp grips tank walls about 64–105 mm thick (106 mm clear opening).
- **Probe position:** the probe sits 22 mm or more inward from the wall, over the water.
- **Frame:** 178 mm long, 10 mm jaws and spine, 24 mm wide.
- **Reversing the probe:** pull the pin, slide the holder out, turn it 180°, slide it back in and re-pin it. The probe can then face the water whichever way up the clamp is mounted.
- **Retaining the probe:** push the probe through from the flange side. The side hole takes an M3 set screw, or a drop of glue.

## Printing (Ender-3 V3 SE)
- **Settings:** PETG, 0.2 mm layers, 4 walls, 40% infill. No supports.
- **G-code:** `gcode/tank_clamp_EnderV3SE_PETG.gcode` has all 4 parts on one plate (about 5 h 15 min, 85 g, 250 °C nozzle / 70 °C bed).
- **Orientation:** the frame prints lying on its side, so its thread is printed horizontally. If the screw is stiff, run it in and out a few times, or open up `CLR` in `make_clamp.py`.

## Re-slicing
The flattened OrcaSlicer profiles and the command to regenerate the G-code are in `slicer/` (see `slicer/README.md`).
