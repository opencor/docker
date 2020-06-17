Docker container for OpenCOR
============================

This [Docker](https://docker.com/) container can be used to run a simulation of a [CellML](https://www.cellml.org/) / [SED-ML](https://sed-ml.org/) file using [OpenCOR](https://opencor.ws/) through [Python](https://python.org/).

You can either build the container yourself or use one of the prebuilt versions available on [Docker Hub](https://hub.docker.com/) at <https://hub.docker.com/repository/docker/opencor/opencor>.

Pull a prebuilt version of the container
----------------------------------------

    docker pull opencor/opencor[:<tag>]

where `<tag>` is the tag of a specific version (`yyyy-mm-dd`) or the latest version (`latest`).
If no tag is provided then the latest version is assumed.

Build the container yourself
----------------------------

### From GitHub

#### Default version

A default container can be built using:

    docker build -t opencor https://github.com/opencor/docker.git

#### Specific version

A container with a specific version of OpenCOR can be built using:

    docker build -t opencor --build-arg version=<version> https://github.com/opencor/docker.git

where `<version>` can be either `x.y[.z]` (for an official version of OpenCOR) or `yyyy-mm-dd` (for a snapshot). Note that there is currently no official version of OpenCOR with Python support.

### From a clone

If you clone this repository, you will not only be able to build a container with a default or a specific version of OpenCOR, but also a container based on a local archive of OpenCOR:

    docker build -t opencor --build-arg archive=<archive> .

where `<archive>` is the filename of a `.tar.gz` file.

Run the container
-----------------

### Default

    docker run <image> <url>

where `<image>` is the name of the image (i.e. `opencor/opencor` if you pulled a prebuilt version of the container or `opencor` if you built it yourself), and `<url>` is the URL of a CellML / SED-ML file, e.g. <https://models.physiomeproject.org/workspace/5f5/rawfile/125f548ce204c1d815298d2c8c1d9b774d89e3a7/mcintyre_richardson_grill_model_2001.sedml>.

This will run the CellML / SED-ML file and output the results for the variable of integration, as well as all the state variables in the model, this in a [JSON](https://json.org/) format. For example, for the above URL, we get:

    {
      "environment/t": [
        0.0,
        ...,
        100.0
      ],
      "membrane/V_m": [
        -88.5901439103062,
        ...,
        -89.42705739292656
      ],
      "fast_sodium_channel/fast_sodium_channel_m_gate/m": [
        0.0302964457761589,
        ...,
        0.027969909786511916
      ],
      "fast_sodium_channel/fast_sodium_channel_h_gate/h": [
        0.841520865130776,
        ...,
        0.8560318033219113
      ],
      "persistent_sodium_channel/persistent_sodium_channel_p_gate/p": [
        0.0969864645712442,
        ...,
        0.11512881732943588
      ],
      "slow_potassium_channel/slow_potassium_channel_s_gate/s": [
        0.00997371545602793,
        ...,
        0.1297692977394969
      ],
      "juxtaparanodal_fast_potassium_channel/juxtaparanodal_fast_potassium_channel_n_gate/n": [
        0.000886041197111556,
        ...,
        0.000463917000795369
      ]
    }

### Using a configuration file

    docker run -i <image> <url> < <config>

where `<config>` is the filename of a configuration file in the JSON format, e.g. `config.json`:

    {
      "simulation": {
        "Starting point": 5,
        "Ending point": 50,
        "Point interval": 0.5
      },
      "parameters": {
        "fast_sodium_channel/g_Naf": 3.5,
        "membrane/V_m": -35
      },
      "output": [
        "fast_sodium_channel/i_Naf",
        "leakage_channel/i_Lk",
        "membrane/V_m",
        "membrane/V_m/prime",
        "persistent_sodium_channel/i_Nap",
        "slow_potassium_channel/i_Ks"
      ]
    }

The configuration file is used to configure the simulation (using the information in the `simulation` section, if present), customise the initial state of the model (using the information in the `parameters` section, if present). The simulation is then run and the variable of integration, as well as all the variables listed in the `output` section (if present otherwise all the state variables), are outputted. For example, for <https://models.physiomeproject.org/workspace/5f5/rawfile/125f548ce204c1d815298d2c8c1d9b774d89e3a7/mcintyre_richardson_grill_model_2001.sedml> and the above configuration file, we get:

    {
      "environment/t": [
        5.0,
        ...,
        50.0
      ],
      "membrane/V_m": [
        -35.0,
        ...,
        -72.4735314003255
      ],
      "membrane/V_m/prime": [
        -210.57350734894032,
        ...,
        3.572051321498071
      ],
      "fast_sodium_channel/i_Naf": [
        -0.006961885968193237,
        ...,
        -0.3051159365312024
      ],
      "leakage_channel/i_Lk": [
        0.385,
        ...,
        0.12268528019772151
      ],
      "persistent_sodium_channel/i_Nap": [
        -0.0007754473404489828,
        ...,
        -0.701626253584342
      ],
      "slow_potassium_channel/i_Ks": [
        0.04388434800652289,
        ...,
        0.8769128072748268
      ]
    }

Note that rate variables have an identifier that ends with `/prime`, e.g. `membrane/V_m/prime` refers to the rate variable for the `membrane/V_m` state variable.
