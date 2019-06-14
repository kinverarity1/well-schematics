Borehole/well schematics in matplotlib
======================================

``well-schematics`` is a package to help with making schematic diagrams of the construction
of boreholes and wells in matplotlib.

The project's homepage is at `GitHub <https://github.com/kinverarity1/well-schematics>`__.

Install
-------

It can be installed from PyPI:

.. code-block:: bash

    $ pip install well-schematics

Usage
-----

.. code-block:: python

    >>> from well_schematics import draw_simple
    >>> draw_simple(pzone_top=27, pzone_bottom=36, casing_top=-0.5, pzone_type="S")

.. figure:: ../example.png

Docstrings
----------

.. autofunction:: well_schematics.draw_simple

Changelog
---------

Version 0.1.0
~~~~~~~~~~~~~

- Initial release

