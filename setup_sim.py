#!/usr/env/python

from tracer_config import load_tracer_configuration, load_run_config
from namelist     import generate_user_nl_eam
from f90_patch    import generate_f90_tracer_block, patch_f90_file
from xml_config   import change_xml_config_files


def main():
    # Load configuration
    water_tags = load_tracer_configuration('tracer_configuration.json')
    run_config  = load_run_config('run_config.json')

    # Write the EAM namelist
    generate_user_nl_eam(water_tags)

    # Patch the Fortran source file
    tracer_block = generate_f90_tracer_block(water_tags)
    patch_f90_file('SourceMods/src.eam/atm_import_export.F90', tracer_block)

    # Apply CESM XML settings
    change_xml_config_files(water_tags, **run_config)


if __name__ == '__main__':
    main()