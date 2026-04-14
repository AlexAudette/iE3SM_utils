from __future__ import print_function

import json
from collections import OrderedDict


def load_tracer_configuration(path='tracer_configuration.json'):
    """Load and return the water tracer definitions from a JSON file.
    Uses OrderedDict to preserve insertion order under Python 2.7.
    """
    with open(path, 'r') as fh:
        return json.load(fh, object_pairs_hook=OrderedDict)


def load_run_config(path='run_config.json'):
    """Load and return the CESM case run parameters from a JSON file."""
    with open(path, 'r') as fh:
        return json.load(fh)