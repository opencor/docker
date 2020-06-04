import json
import sys

import opencor as oc


def main(url, config):
    s = oc.open_simulation(url)

    s.run()

    r = s.results()
    voi = r.voi()
    v_m = r.states()['membrane/V_m']

    print(json.dumps({
        voi.uri(): voi.values().tolist(),
        v_m.uri(): v_m.values().tolist()
    }, indent=2))


def usage():
    print('Usage: docker run opencor <url>')
    print('   or: docker run -i opencor <url> < <config>')
    print('  where <url> is the URL of a CellML / SED-ML file')
    print('    e.g. https://models.physiomeproject.org/workspace/5f5/rawfile/125f548ce204c1d815298d2c8c1d9b774d89e3a7'
          '/mcintyre_richardson_grill_model_2001.sedml')
    print('  where <config> is the filename of a configuration (JSON) file.')
    print('    e.g. config.json')
    print('    {')
    print('      "simulation": {')
    print('        "Starting point": 0,')
    print('        "Ending point": 100,')
    print('        "Point interval": 0.1')
    print('      },')
    print('      "parameters": {')
    print('        "fast_sodium_channel/g_Naf": 3,')
    print('        "membrane/stim_amplitude": 0.05,')
    print('        "membrane/stim_duration": 0.5')
    print('      },')
    print('      "output": [')
    print('        "membrane/V_m",')
    print('        "membrane/V_m/prime"')
    print('      ]')
    print('    }')


if __name__ == "__main__":
    # Make sure that a URL is provided.

    if len(sys.argv) != 2:
        usage()

        exit(1)
    else:
        url = sys.argv[1]

    # Retrieve the config, if any.
    # Note: the sys.stdin.isatty() test is irrelevant when running this script from a container, but it is needed if we
    #       want to test this script directly.

    if sys.stdin.isatty():
        config = None
    else:
        try:
            config = json.load(sys.stdin)
        except:
            config = None

    main(url, config)
