import json
 
 
def load_tracer_configuration(path: str = 'tracer_configuration.json') -> dict:
    """Load and return the water tracer definitions from a JSON file."""
    with open(path, 'r') as fh:
        return json.load(fh)
 
 
def load_run_config(path: str = 'run_config.json') -> dict:
    """Load and return the CESM case run parameters from a JSON file."""
    with open(path, 'r') as fh:
        return json.load(fh)