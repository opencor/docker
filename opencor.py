import json

import opencor as oc

if __name__ == "__main__":
    s = oc.open_simulation('https://models.physiomeproject.org/workspace/5f5/rawfile'
                           '/125f548ce204c1d815298d2c8c1d9b774d89e3a7/mcintyre_richardson_grill_model_2001.sedml')

    s.run()

    r = s.results()
    voi = r.voi()
    v_m = r.states()['membrane/V_m']

    print(json.dumps({
        voi.uri(): voi.values().tolist(),
        v_m.uri(): v_m.values().tolist()
    }, indent=2))
