Docker for OpenCOR
==================

Repository to build a `Docker <https://docker.com/>`_ image to run a simulation of a `CellML <https://www.cellml.org/>`_ or a `SED-ML <https://sed-ml.org/>`_ file using `OpenCOR <https://opencor.ws/>`_ through `Python <https://python.org/>`_.

Build Command
-------------

::

  docker build [--no-cache] -t opencor [--build-arg archive=<archive>|version=<version>] https://github.com/agarny/opencor_docker.git

where ``<archive>`` is the Linux ``.tar.gz`` file for a given version of OpenCOR, and ``<version>`` is the version of OpenCOR to use.
It can be either ``x.y[.z]`` (for an official version of OpenCOR) or ``yyyy-mm-dd`` (for a snapshot).

If no argument is provided then the ``2020-02-14`` snapshot will be used.

Run Command
-----------

::

  docker run opencor
