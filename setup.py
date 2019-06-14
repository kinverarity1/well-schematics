from setuptools import setup

setup(
    name="well-schematics",
    packages=("well_schematics",),
    version="0.2.0",
    description="matplotlib code for drawing borehole schematic diagrams",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kinverarity1/well-schematics",
    author="Kent Inverarity",
    author_email="kinverarity@hotmail.com",
    license="MIT",
    install_requires=("matplotlib"),
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ),
    keywords="groundwater data",
)
