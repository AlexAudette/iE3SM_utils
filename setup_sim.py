#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import sys

from tracer_config import load_tracer_configuration, load_run_config
from namelist      import generate_user_nl_eam
from f90_patch     import generate_f90_tracer_block, patch_f90_file
from xml_config    import change_xml_config_files

# Directory containing this script - JSON configs and F90 source are resolved relative to it
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

F90_RELATIVE_PATH = os.path.join('SourceMods', 'src.eam', 'atm_import_export.F90')


def main():
    parser = argparse.ArgumentParser(
        description='Configure a CESM/EAM water tracer case.'
    )
    parser.add_argument(
        'casedir',
        help='Path to the CESM case directory (i.e. $CASEDIR)',
    )
    parser.add_argument(
        'tracer_config',
        help='Tracer configuration matching the name of the JSON file in the tracer_configs/ directory',
    )
    args = parser.parse_args()
    casedir = os.path.realpath(args.casedir)
    tracer_config = str(args.tracer_config)
    
    if not os.path.isdir(casedir):
        sys.exit('Error: case directory not found: {0}'.format(casedir))

    # Load configuration from alongside this script
    water_tags = load_tracer_configuration(os.path.join(SCRIPT_DIR, 'tracer_configs/{0}.json').format(tracer_config))
    run_config  = load_run_config(os.path.join(SCRIPT_DIR, 'run_config.json'))

    # Write the EAM namelist into the case directory
    generate_user_nl_eam(water_tags, output_path=os.path.join(casedir, 'user_nl_eam'))

    # Read F90 from run_setup/, write patched version into $CASEDIR/SourceMods/
    tracer_block = generate_f90_tracer_block(water_tags)
    patch_f90_file(
        source_path=os.path.join(SCRIPT_DIR, F90_RELATIVE_PATH),
        dest_path=os.path.join(casedir, F90_RELATIVE_PATH),
        tracer_block=tracer_block,
    )

    # Apply CESM XML settings - xmlchange must be run from inside the case directory
    change_xml_config_files(water_tags, casedir=casedir, **run_config)


if __name__ == '__main__':
    main()