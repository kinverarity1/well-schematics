# well-schematics

matplotlib code for drawing borehole schematic diagrams

## Usage

```python
>>> import matplotlib.pyplot as plt
>>> from well_schematics import draw_simple
>>> fig = plt.figure(figsize=(1, 5))
>>> ax = fig.add_subplot(111)
>>> _ = draw_simple(pzone_top=27, pzone_bottom=36, casing_top=-0.5, pzone_type="S", ax=ax)
```

![](example.png)

