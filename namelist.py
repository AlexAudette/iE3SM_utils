def generate_user_nl_eam(water_tags: dict, output_path: str = 'namelist_files/user_nl_eam') -> None:
    """
    Write a user_nl_eam namelist file from the water_tags definition.

    For each tracer the following output fields are generated:
      - Phase fields:  {TAG}V, {TAG}I, {TAG}L
      - Precip fields: PRECSL_{TAG}S, PRECRL_{TAG}R, PRECSC_{TAG}s, PRECRC_{TAG}r
      - Flux field:    QFLX_{TAG}  (non-H2O tags only)

    fincl1 contains the full diagnostic set (all phases + precip + flux).
    fincl2 contains a reduced set (vapour + precip only).
    """
    tag_names = list(water_tags.keys())  # preserve dict order

    # wtrc_in_names
    wtrc_names_str = ', '.join(f"'{t}'" for t in tag_names)

    # wtrc_fixed_rstd: read from each tag's 'rstd' key in water_tags
    rstd_values = [str(water_tags[t].get('rstd', 0.0)) for t in tag_names]
    rstd_str = ', '.join(rstd_values)

    def phase_fields(tag):
        """V/I/L phase fields for a tracer."""
        return [f'{tag}V', f'{tag}I', f'{tag}L']

    def precip_fields(tag):
        """Precip fields for a tracer (mixed case suffixes follow iCAM convention)."""
        return [
            f'PRECSL_{tag}S', f'PRECRL_{tag}R',
            f'PRECSC_{tag}s', f'PRECRC_{tag}r',
        ]

    # fincl1: base fields, then per-tag: large-scale precip, phases, conv precip
    #         QFLX_{TAG} fields grouped at the end for non-H2O tags
    fincl1_base = [
        'PS', 'TREFHT', 'U', 'V', 'OMEGA', 'Q', 'T', 'ICEFRAC',
        'FLNT', 'FSNT', 'LHFLX', 'SHFLX', 'FLNS', 'FSNS',
        'PRECSC', 'PRECSL', 'QFLX', 'PRECC', 'PRECL',
    ]
    fincl1_tracer = []
    for tag in tag_names:
        ls_precip = [f'PRECSL_{tag}S', f'PRECRL_{tag}R']
        cv_precip = [f'PRECSC_{tag}s', f'PRECRC_{tag}r']
        fincl1_tracer += ls_precip + phase_fields(tag) + cv_precip
    for tag in tag_names:
        if tag != 'H2O':
            fincl1_tracer += [f'QFLX_{tag}']

    # fincl2: base fields + vapour + precip per tag, then QFLX for non-H2O at end
    fincl2_base = [
        'PS', 'FLUT', 'PRECT', 'U200', 'V200', 'U850', 'V850',
        'TCO', 'SCO', 'TREFHT', 'QREFHT', 'U', 'V', 'Q', 'T',
    ]
    fincl2_tracer = []
    for tag in tag_names:
        fincl2_tracer += [f'{tag}V'] + precip_fields(tag)
    for tag in tag_names:
        if tag != 'H2O':
            fincl2_tracer += [f'QFLX_{tag}']

    fincl1_str = ','.join(f"'{f}'" for f in fincl1_base + fincl1_tracer)
    fincl2_str = ','.join(f"'{f}'" for f in fincl2_base + fincl2_tracer)

    lines = [
        '',
        '',
        f'wtrc_in_names = {wtrc_names_str}',
        f'wtrc_fixed_rstd = {rstd_str}',
        '',
        'wisotope\t\t= .false.',
        'use_mass_borrower = .true.',
        '',
        'nhtfrq = 0,-24',
        'mfilt  = 1,1',
        "avgflag_pertape = 'A','A'",
        '',
        f'fincl1 = {fincl1_str}',
        '',
        f'fincl2 = {fincl2_str}',
    ]

    with open(output_path, 'w') as fh:
        fh.write('\n'.join(lines) + '\n')

    print(f'Written {output_path}')