from __future__ import print_function

import os
import subprocess


def _xmlchange(*args, **kwargs):
    casedir = kwargs['casedir']
    cmd = [os.path.join(casedir, 'xmlchange')] + list(args)
    print('Running: ' + ' '.join(cmd))
    subprocess.check_call(cmd, cwd=casedir)


def change_xml_config_files(
    water_tags,
    casedir,
    resubmit=5,
    stop_n=5,
    stop_option='nyears',
    wallclock='48:00:00',
    dout_s=True,
):
    """
    Run xmlchange commands to configure the CESM case for a water tracer run.

    Parameters
    ----------
    water_tags  : tracer dict - used to derive the number of non-H2O tags.
    casedir     : path to the CESM case directory, used as the working directory
                  for xmlchange calls.
    resubmit    : number of resubmissions after the initial run.
    stop_n      : run length per submission (in units of stop_option).
    stop_option : time unit for stop_n (e.g. 'nyears', 'nmonths').
    wallclock   : wall-clock limit per job (HH:MM:SS).
    dout_s      : whether to enable short-term archiving (DOUT_S).
    """
    def xc(*args):
        _xmlchange(*args, casedir=casedir)

    N_WTRC = len(water_tags)
    xc('--append', 'CAM_CONFIG_OPTS=-water_tracer h2o -water_tag_num {0}'.format(N_WTRC - 1))
    xc('RESUBMIT={0}'.format(resubmit))
    xc('STOP_N={0}'.format(stop_n))
    xc('STOP_OPTION={0}'.format(stop_option))
    xc('DOUT_S={0}'.format('TRUE' if dout_s else 'FALSE'))
    xc('JOB_WALLCLOCK_TIME={0}'.format(wallclock), '--subgroup', 'case.run')