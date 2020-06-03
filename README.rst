Docker container for OpenCOR
============================

Repository to build a `Docker <https://docker.com/>`_ image to run a simulation of a `CellML <https://www.cellml.org/>`_ or a `SED-ML <https://sed-ml.org/>`_ file using `OpenCOR <https://opencor.ws/>`_ through `Python <https://python.org/>`_.

Build the container
-------------------

A container with the ``2020-02-14`` snapshot of OpenCOR can be built using:

::

  docker build -t opencor https://github.com/agarny/opencor_docker.git

A container with a specific version of OpenCOR can be built using:

::

  docker build -t opencor [--build-arg version=<version>] https://github.com/agarny/opencor_docker.git

where ``<version>`` can be either ``x.y[.z]`` (for an official version of OpenCOR) or ``yyyy-mm-dd`` (for a snapshot).
Note that there is currently no official version of OpenCOR with Python support.

If you clone this repository and copy to it the Linux archive of a given version of OpenCOR, then a container with that version of OpenCOR can be built using:

::

  docker build -t opencor [--build-arg archive=<archive>] .

where ``<archive>`` is the filename of a ``.tar.gz`` file.

Run the container
-----------------

::

  docker run opencor
