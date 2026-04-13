#!/usr/env/python

import argparse
from pathlib import Path

from tracer_config import load_tracer_configuration, load_run_config
from namelist     import generate_user_nl_eam
from f90_patch    import generate_f90_tracer_block, patch_f90_file
from xml_config   import change_xml_config_files

# Directory containing this script — JSON configs are resolved relative to it
SCRIPT_DIR = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser(
        description='Configure a CESM/EAM water tracer case.'
    )
    parser.add_argument(
        'casedir',
        type=Path,
        help='Path to the CESM case directory (i.e. $CASEDIR)',
    )
    args = parser.parse_args()
    casedir = args.casedir.resolve()

    if not casedir.is_dir():
        raise SystemExit(f'Error: case directory not found: {casedir}')

    # Load configuration from alongside this script
    water_tags = load_tracer_configuration(SCRIPT_DIR / 'tracer_configuration.json')
    run_config  = load_run_config(SCRIPT_DIR / 'run_config.json')

    # Write the EAM namelist into the case directory
    generate_user_nl_eam(water_tags, output_path=casedir / 'user_nl_eam')

    # Patch the Fortran source file inside the case directory
    tracer_block = generate_f90_tracer_block(water_tags)
    patch_f90_file(casedir / 'SourceMods/src.eam/atm_import_export.F90', tracer_block)

    # Apply CESM XML settings — xmlchange must be run from inside the case directory
    change_xml_config_files(water_tags, casedir=casedir, **run_config)


if __name__ == '__main__':
    main()