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
    print('Usage: docker run opencor <url> <config>')
    print('  where <url> is the URL to a CellML / SED-ML file')
    print('e.g. https://models.physiomeproject.org/workspace/5f5/rawfile/125f548ce204c1d815298d2c8c1d9b774d89e3a7'
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
    args = sys.argv

    args.pop(0)

    try:
        url = args.pop(0)
        config = args.pop(0)
    except:
        usage()

        sys.exit(1)

    main(url, config)
