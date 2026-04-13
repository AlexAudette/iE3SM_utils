# Water Tracer Setup

Python tooling for configuring CESM/EAM water tracer simulations. Given a set of tracer definitions and run parameters in JSON, the script automatically patches the Fortran source code, writes the EAM namelist, and applies all required `xmlchange` settings.

## Project structure

```
setup_sim.py               # Entry point — run this
tracer_config.py           # JSON loading
namelist.py                # Generates user_nl_eam
f90_patch.py               # Patches atm_import_export.F90
xml_config.py              # Runs xmlchange commands
tracer_configuration.json  # Tracer definitions (edit this)
run_config.json            # CESM case run parameters (edit this)
atm_import_export.F90      # Fortran source to be patched
```

## Usage

From inside your CESM case directory:

```bash
python setup_sim.py
```

This will:
1. Write `user_nl_eam` with tracer names, isotope ratios, and output field lists
2. Patch the tracer source block in `atm_import_export.F90`
3. Run the `xmlchange` commands to configure the case

## Configuration

### `tracer_configuration.json`

Defines the water tracers. `H2O` must always be the first entry — it is the bulk water reference tracer required by the water tagging scheme. All subsequent entries are regional tags.

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

Everything between these markers is overwritten on each run. Do not add manual edits inside the marked region — they will be lost. The generated block applies the evaporative flux to each tracer within its defined geographic bounds and sets it to zero elsewhere.

## Output fields

The generated `user_nl_eam` includes two output tapes:

**`fincl1`** (monthly mean, full diagnostics) — base meteorological fields plus, for each tracer: large-scale precipitation, vapour/ice/liquid phase fields, convective precipitation, and surface moisture flux (`QFLX_{TAG}`, non-H2O tracers only).

**`fincl2`** (daily mean, reduced set) — base meteorological fields plus, for each tracer: vapour field and precipitation only.