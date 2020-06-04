############################
Docker container for OpenCOR
############################

Repository to build a `Docker <https://docker.com/>`_ container to run a simulation of a `CellML <https://www.cellml.org/>`_ / `SED-ML <https://sed-ml.org/>`_ file using `OpenCOR <https://opencor.ws/>`_ through `Python <https://python.org/>`_.

*******************
Build the container
*******************

From GitHub
===========

Default version
---------------

A default container can be built using:

::

  docker build -t opencor https://github.com/agarny/opencor_docker.git

Specific version
----------------

A container with a specific version of OpenCOR can be built using:

::

  docker build -t opencor --build-arg version=<version> https://github.com/agarny/opencor_docker.git

where ``<version>`` can be either ``x.y[.z]`` (for an official version of OpenCOR) or ``yyyy-mm-dd`` (for a snapshot).
Note that there is currently no official version of OpenCOR with Python support.

From a clone
============

If you clone this repository, you will not only be able to build a container with a default or a specific version of OpenCOR, but also a container based on a local archive of OpenCOR:

::

  docker build -t opencor --build-arg archive=<archive> .

where ``<archive>`` is the filename of a ``.tar.gz`` file.

*****************
Run the container
*****************

::

  docker run opencor

This will output the membrane potential for the `MRG model <https://models.physiomeproject.org/e/5f7>`_:

::

  {
    "environment/t": [
      0.0,
      0.1,
      0.2,
      ...,
      99.80000000000001,
      99.9,
      100.0
    ],
    "membrane/V_m": [
      -88.5901439103062,
      -88.59014391030621,
      -88.59014391030622,
      ...,
      -89.42743936614418,
      -89.42724991998269,
      -89.42705739292656
    ]
  }
