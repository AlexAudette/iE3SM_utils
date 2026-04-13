import subprocess


def _xmlchange(*args: str) -> None:
    cmd = ['./xmlchange'] + list(args)
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def change_xml_config_files(
    water_tags: dict,
    resubmit: int = 5,
    stop_n: int = 5,
    stop_option: str = 'nyears',
    wallclock: str = '48:00:00',
    dout_s: bool = True,
) -> None:
    """
    Run xmlchange commands to configure the CESM case for a water tracer run.

    Parameters
    ----------
    water_tags  : tracer dict — used to derive the number of non-H2O tags.
    resubmit    : number of resubmissions after the initial run.
    stop_n      : run length per submission (in units of stop_option).
    stop_option : time unit for stop_n (e.g. 'nyears', 'nmonths').
    wallclock   : wall-clock limit per job (HH:MM:SS).
    dout_s      : whether to enable short-term archiving (DOUT_S).
    """
    N_WTRC = len(water_tags)
    _xmlchange('--append', f'CAM_CONFIG_OPTS=-water_tracer h2o -water_tag_num {N_WTRC - 1}')

    _xmlchange(f'RESUBMIT={resubmit}')
    _xmlchange(f'STOP_N={stop_n}', f'STOP_OPTION={stop_option}')
    _xmlchange(f'DOUT_S={"TRUE" if dout_s else "FALSE"}')
    _xmlchange(f'JOB_WALLCLOCK_TIME={wallclock}', '--subgroup', 'case.run')