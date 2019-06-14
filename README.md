# well-schematics

[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/kinverarity1/well-schematics/blob/master/LICENSE)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/well-schematics.svg)](https://pypi.python.org/pypi/well-schematics/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/well-schematics.svg)](https://pypi.python.org/pypi/well-schematics/)
[![Documentation Status](https://readthedocs.org/projects/well-schematics/badge/?version=latest)](http://well-schematics.readthedocs.io/?badge=latest)

matplotlib code for drawing borehole/well schematic diagrams

## Install

```bash
$ pip install -U well-schematics
```

## Usage

Check out the [documentation](http://well-schematics.readthedocs.io/?badge=latest).

```python
>>> from well_schematics import draw_simple
>>> draw_simple(pzone_top=27, pzone_bottom=36, casing_top=-0.5, pzone_type="S")
```

![](example.png)

## Contributing / roadmap

I would love to have implementations of different types of schematics. Any 
contributions at all are [welcome](https://github.com/Unidata/MetPy#contributing)!

- <strike>The simplest well: casing with a production zone at the bottom</strike>
- Different types of production zones, particularly perforations
- Multiple production zones separated by blanks
- Different pipe diameters
- Risers (pipe inside pipe)
- Drilled hole
- Cemented zones outside pipe
- Cement plugs
- Annotations tied to each casing pipe/production zone

## License

Free to modify and re-distribute under the [MIT license](LICENSE).