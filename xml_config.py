import subprocess
from pathlib import Path


def _xmlchange(*args: str, casedir: Path) -> None:
    cmd = [f'{casedir}/xmlchange'] + list(args)
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd, check=True, cwd=casedir)


def change_xml_config_files(
    water_tags: dict,
    casedir: Path,
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
    casedir     : path to the CESM case directory, used as the working directory
                  for xmlchange calls.
    resubmit    : number of resubmissions after the initial run.
    stop_n      : run length per submission (in units of stop_option).
    stop_option : time unit for stop_n (e.g. 'nyears', 'nmonths').
    wallclock   : wall-clock limit per job (HH:MM:SS).
    dout_s      : whether to enable short-term archiving (DOUT_S).
    """
    xc = lambda *args: _xmlchange(*args, casedir=casedir)

    N_WTRC = len(water_tags)
    xc('--append', f'CAM_CONFIG_OPTS=-water_tracer h2o -water_tag_num {N_WTRC - 1}')

    xc(f'RESUBMIT={resubmit}')
    xc(f'STOP_N={stop_n}', f'STOP_OPTION={stop_option}')
    xc(f'DOUT_S={"TRUE" if dout_s else "FALSE"}')
    xc(f'JOB_WALLCLOCK_TIME={wallclock}', '--subgroup', 'case.run')