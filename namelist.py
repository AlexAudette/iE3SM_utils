from __future__ import print_function


def generate_user_nl_eam(water_tags, output_path='namelist_files/user_nl_eam'):
    """
    Write a user_nl_eam namelist file from the water_tags definition.

    For each tracer the following output fields are generated:
      - Phase fields:  {TAG}V, {TAG}I, {TAG}L
      - Precip fields: PRECSL_{TAG}S, PRECRL_{TAG}R, PRECSC_{TAG}s, PRECRC_{TAG}r
      - Flux field:    QFLX_{TAG}  (non-H2O tags only)

    fincl1 contains the full diagnostic set (all phases + precip + flux).
    fincl2 contains a reduced set (vapour + precip only).
    """
    tag_names = list(water_tags.keys())  # preserves order (OrderedDict in 2.7)

    # wtrc_in_names
    wtrc_names_str = ', '.join("'{0}'".format(t) for t in tag_names)

    # wtrc_fixed_rstd: read from each tag's 'rstd' key in water_tags
    rstd_values = [str(water_tags[t].get('rstd', 0.0)) for t in tag_names]
    rstd_str = ', '.join(rstd_values)

    def phase_fields(tag):
        """V/I/L phase fields for a tracer."""
        return ['{0}V'.format(tag), '{0}I'.format(tag), '{0}L'.format(tag)]

    def precip_fields(tag):
        """Precip fields for a tracer (mixed case suffixes follow iCAM convention)."""
        return [
            'PRECSL_{0}S'.format(tag), 'PRECRL_{0}R'.format(tag),
            'PRECSC_{0}s'.format(tag), 'PRECRC_{0}r'.format(tag),
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
        ls_precip = ['PRECSL_{0}S'.format(tag), 'PRECRL_{0}R'.format(tag)]
        cv_precip = ['PRECSC_{0}s'.format(tag), 'PRECRC_{0}r'.format(tag)]
        fincl1_tracer += ls_precip + phase_fields(tag) + cv_precip
    for tag in tag_names:
        if tag != 'H2O':
            fincl1_tracer += ['QFLX_{0}'.format(tag)]

    # fincl2: base fields + vapour + precip per tag, then QFLX for non-H2O at end
    fincl2_base = [
        'PS', 'FLUT', 'PRECT', 'U200', 'V200', 'U850', 'V850',
        'TCO', 'SCO', 'TREFHT', 'QREFHT', 'U', 'V', 'Q', 'T',
    ]
    fincl2_tracer = []
    for tag in tag_names:
        fincl2_tracer += ['{0}V'.format(tag)] + precip_fields(tag)
    for tag in tag_names:
        if tag != 'H2O':
            fincl2_tracer += ['QFLX_{0}'.format(tag)]

    fincl1_str = ','.join("'{0}'".format(f) for f in fincl1_base + fincl1_tracer)
    fincl2_str = ','.join("'{0}'".format(f) for f in fincl2_base + fincl2_tracer)

    lines = [
        '',
        '',
        'wtrc_in_names = {0}'.format(wtrc_names_str),
        'wtrc_fixed_rstd = {0}'.format(rstd_str),
        '',
        'wisotope\t\t= .false.',
        'use_mass_borrower = .true.',
        '',
        'nhtfrq = 0,-24',
        'mfilt  = 1,1',
        "avgflag_pertape = 'A','A'",
        '',
        'fincl1 = {0}'.format(fincl1_str),
        '',
        'fincl2 = {0}'.format(fincl2_str),
    ]

    with open(output_path, 'w') as fh:
        fh.write('\n'.join(lines) + '\n')

    print('Written {0}'.format(output_path))