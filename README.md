# Water Tracer Setup

Python tooling for configuring CESM/EAM water tracer simulations. Given a set of tracer definitions and run parameters in JSON, the script automatically edit the Fortran source code, writes the EAM namelist, and applies all required `xmlchange` settings.

## Project structure

```
iE3SM_utils/                          ← run scripts from here
├── setup_sim.py
├── tracer_config.py
├── namelist.py
├── f90_patch.py
├── xml_config.py
├── tracer_configuration.json       ← edit this to define your tracers
└── run_config.json                 ← edit this to set run length, wallclock, etc.

$CASEDIR/                           ← files will be written here
├── SourceMods/
│   └── src.eam/
│       └── atm_import_export.F90   ← will be patched by setup_sim.py
└── user_nl_eam                     ← will be written by setup_sim.py
```

## Requirements

Python 2.7 or later. No third-party packages are required — only modules from
the standard library (`json`, `collections`, `os`, `subprocess`, `argparse`).

## Usage

From the `iE3SM_utils/` directory, pass `$CASEDIR` and the tracer_configuration as arguments::

```bash
python setup_sim.py $CASEDIR <tracer_configuration>
```

The tracer configuration is a JSON file that defines the water tracer regions, withouth the `.json` extension.
```

This will:
1. Write `user_nl_eam` with tracer names, isotope ratios, and output field lists
2. Patch the tracer source block in `atm_import_export.F90`
3. Run the `xmlchange` commands to configure the case

## Configuration

### `tracer_configuration.json`

Defines the water tracers. `H2O` must always be the first entry — it is the bulk water reference tracer required by the water tagging scheme. All subsequent entries are regional tags. Add or modify regional tags (e.g. `ARC`, `ROW`) with their latitude/longitude bounds and isotope ratios. Here are examples for the two tracers describing the moisture evaporated from the Arctic and from the rest of the world:

```json
{
    "H2O": {
        "lat_bounds": [-90, 90],
        "rstd": 1.0,
        "description": "Bulk water reference. Required in every water tracer run."
    },
    "ARC": {
        "lat_bounds": [70, 90],
        "rstd": 0.003,
        "description": "Arctic water vapour"
    },
    "ROW": {
        "lat_bounds": [-90, 70],
        "rstd": 0.997,
        "description": "Rest of world water vapour"
    }
}
```

**Fields per tracer:**

| Field | Required | Description |
|---|---|---|
| `lat_bounds` | Yes | `[south, north]` latitude limits in degrees |
| `lon_bounds` | No | `[west, east]` longitude limits in degrees. Combined with `lat_bounds` if both are present |
| `rstd` | Yes | Standard isotope ratio used for `wtrc_fixed_rstd` in the namelist |
| `description` | No | Human-readable label, written as a comment in the Fortran block |

To add a new regional tracer, append an entry to the JSON. The Fortran `if/else if` block and all namelist field lists are generated automatically from the order of entries in the file.

### `run_config.json`

Controls the CESM case settings applied via `xmlchange`.

```json
{
    "resubmit": 5,
    "stop_n": 5,
    "stop_option": "nyears",
    "wallclock": "48:00:00",
    "dout_s": true
}
```

**Fields:**

| Field | Default | Description |
|---|---|---|
| `resubmit` | `5` | Number of automatic resubmissions after the initial job |
| `stop_n` | `5` | Run length per submission, in units of `stop_option` |
| `stop_option` | `"nyears"` | Time unit for `stop_n` — e.g. `"nyears"`, `"nmonths"`, `"ndays"` |
| `wallclock` | `"48:00:00"` | Wall-clock time limit per job (`HH:MM:SS`) |
| `dout_s` | `true` | Enable short-term archiving (`DOUT_S`) |

## Fortran patching

`atm_import_export.F90` must contain the following marker comments to delimit the region that will be replaced:

```fortran
! *** Add water tracer source definition here:

! *** Water tracer source definition ended.
```

Everything between these markers is overwritten on each run. Do not add manual edits inside the marked region — they will be lost when you run `setup_run.py`. If you edit manually the `atm_import_export.F90` file, do so after running this script. The generated block applies the evaporative flux to each tracer within its defined geographic bounds and sets it to zero elsewhere.

## Output fields

The generated `user_nl_eam` includes two output tapes:

**`fincl1`** (monthly mean, full diagnostics) — base meteorological fields plus, for each tracer: large-scale precipitation, vapour/ice/liquid phase fields, convective precipitation, and surface moisture flux (`QFLX_{TAG}`, non-H2O tracers only).

**`fincl2`** (daily mean, reduced set) — base meteorological fields plus, for each tracer: vapour field and precipitation only.

---
MIT License

Copyright (c) 2026 Alexandre Audette

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.