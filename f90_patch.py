def generate_f90_tracer_block(water_tags: dict) -> str:
    """
    Generate the Fortran if/else if block for water tracer surface flux sources.
    Skips the first entry (H2O, j==1, handled separately upstream).
    Supports lat_bounds and optional lon_bounds per tracer.
    """
    lines = []
    # Enumerate tags starting at j=2 (j=1 is always H2O)
    tag_items = [(name, cfg) for name, cfg in water_tags.items() if name != 'H2O']

    for idx, (name, cfg) in enumerate(tag_items):
        j = idx + 2  # j==1 is H2O
        keyword = 'if' if idx == 0 else 'else if'

        lat_bounds = cfg.get('lat_bounds')
        lon_bounds = cfg.get('lon_bounds')

        # Build the geographic condition
        conditions = []
        if lat_bounds is not None:
            lat_lo, lat_hi = lat_bounds
            conditions.append(f'(wtlat >= {lat_lo:.1f}_r8) .and. (wtlat <= {lat_hi:.1f}_r8)')
        if lon_bounds is not None:
            lon_lo, lon_hi = lon_bounds
            conditions.append(f'(wtlon >= {lon_lo:.1f}_r8) .and. (wtlon <= {lon_hi:.1f}_r8)')

        geo_condition = ' .and. '.join(conditions) if conditions else '.true.'

        lines.append(f'                     {keyword}(j .eq. {j}) then')
        lines.append(f'                        !{name}: {cfg.get("description", "")}')
        lines.append(f'                        if({geo_condition}) then')
        lines.append(f'                           cam_in(c)%cflx(i,wtrc_indices(wtrc_iasrfvap(j))) = -x2a(index_x2a_Faxx_evap,ig)')
        lines.append(f'                        else')
        lines.append(f'                           cam_in(c)%cflx(i,wtrc_indices(wtrc_iasrfvap(j))) = 0._r8')
        lines.append(f'                        end if')

    return '\n'.join(lines)


def patch_f90_file(f90_path: str, tracer_block: str) -> None:
    """
    Replace the region between the marker comments in the F90 file
    with the generated tracer block.
    """
    START_MARKER = '! *** Add water tracer source definition here:'
    END_MARKER   = '! *** Water tracer source definition ended.'

    with open(f90_path, 'r') as fh:
        content = fh.read()

    start_idx = content.find(START_MARKER)
    if start_idx == -1:
        raise ValueError(f'Start marker not found in {f90_path}')

    end_idx = content.find(END_MARKER, start_idx + len(START_MARKER))
    if end_idx == -1:
        raise ValueError(f'End marker not found after start marker in {f90_path}')

    new_content = (
        content[:start_idx]
        + START_MARKER + '\n\n'
        + tracer_block + '\n'
        + content[end_idx:]  # closing marker and everything after it
    )

    with open(f90_path, 'w') as fh:
        fh.write(new_content)

    print(f'Patched {f90_path} successfully.')