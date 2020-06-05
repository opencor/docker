import json
import sys

import opencor as oc


def error(msg):
    print('Error: ', msg, '.', sep='')

    exit(1)


def error_config(msg):
    error('the configuration file is invalid (' + msg + ')')


def main(url, config):
    # Open the simulation.

    try:
        s = oc.open_simulation(url)
    except:
        error('the URL does not point to a valid CellML / SED-ML file')

    # Configure the simulation.

    r = s.results()
    rv = r.voi()
    rs = r.states()
    rr = r.rates()
    rc = r.constants()
    ra = r.algebraic()

    strack = []
    rtrack = []
    ctrack = []
    atrack = []

    if config is not None:
        d = s.data()

        for key, value in config.items():
            if key == 'simulation':
                for sim_key, sim_value in value.items():
                    if sim_key == 'Starting point':
                        d.set_starting_point(sim_value)
                    elif sim_key == 'Ending point':
                        d.set_ending_point(sim_value)
                    elif sim_key == 'Point interval':
                        d.set_point_interval(sim_value)
                    else:
                        error_config('\'' + sim_key + '\' is not a valid simulation parameter')
            elif key == 'parameters':
                ds = d.states()
                dc = d.constants()

                for param_key, param_value in value.items():
                    if param_key in ds:
                        ds[param_key] = param_value
                    elif param_key in dc:
                        dc[param_key] = param_value
                    else:
                        error_config('\'' + param_key + '\' is not a valid state or constant variable identifier')
            elif key == 'output':
                for out_key in value:
                    if out_key == rv.uri():
                        continue  # Since we automatically track the variable of integration.
                    elif out_key in rs:
                        strack.append(out_key)
                    elif out_key in rr:
                        rtrack.append(out_key)
                    elif out_key in rc:
                        ctrack.append(out_key)
                    elif out_key in ra:
                        atrack.append(out_key)
                    else:
                        error_config('\'' + out_key + '\' is not a valid state, rate, constant or algebraic variable '
                                                      'identifier')
            else:
                error_config('\'' + key + '\' is not a valid key')

    # If nothing is tracked then track all the state variables.

    if not strack and not rtrack and not ctrack and not atrack:
        for key in rs:
            strack.append(key)

    # Run the simulation.

    s.run()

    # Output the variable of integration and all the data that we want tracked.

    output = {rv.uri(): rv.values().tolist()}

    for key in strack:
        output[key] = rs[key].values().tolist()

    for key in rtrack:
        output[key] = rr[key].values().tolist()

    for key in ctrack:
        output[key] = rc[key].values().tolist()

    for key in atrack:
        output[key] = ra[key].values().tolist()

    print(json.dumps(output, indent=2))


def usage():
    print('Usage: docker run opencor <url>')
    print('   or: docker run -i opencor <url> < <config>')
    print('  where <url> is the URL of a CellML / SED-ML file')
    print('  where <config> is the filename of a configuration file.')


if __name__ == "__main__":
    # Make sure that a URL is provided.

    if len(sys.argv) != 2:
        usage()

        exit(1)
    else:
        url = sys.argv[1]

    # Retrieve the config, if any.
    # Note: the sys.stdin.isatty() test is irrelevant when running this script from a Docker container, but it is needed
    #       if we want to test this script directly.

    if sys.stdin.isatty():
        config = None
    else:
        try:
            config = json.load(sys.stdin)
        except:
            config = None

    main(url, config)
