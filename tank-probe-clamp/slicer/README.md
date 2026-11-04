# Slicer profiles for the OrcaSlicer CLI

The OrcaSlicer CLI does not resolve a system profile's `inherits` chain, so the vendor profiles fail validation when loaded directly. `flat.py` merges each chain into a single self-contained JSON file.

- `m.json`: Creality Ender-3 V3 SE, 0.4 mm nozzle
- `p.json`: 0.20mm Standard @Creality Ender3V3SE 0.4
- `p40.json`: the same, with 4 walls and 40% infill (used for the clamp)
- `f.json`: Creality Generic PLA @Ender-3V3-all
- `petg.json`: Creality Generic PETG @Ender-3V3-all

In `p*.json`, `f.json` and `petg.json`, `compatible_printers` is pinned to the Ender-3 V3 SE and `compatible_printers_condition` is cleared. Without that, the CLI fails with "process not compatible with printer".

To re-slice, run this from the project folder in Git Bash:

    "/c/Program Files/OrcaSlicer/orca-slicer.exe" --arrange 1 \
      --load-settings "slicer/m.json;slicer/p40.json" --load-filaments "slicer/petg.json" \
      --slice 0 --outputdir gcode clamp_frame.stl probe_holder.stl clamp_screw.stl lock_pin.stl
