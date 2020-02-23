from setuptools import setup

setup(
    name="well-schematics",
    packages=("well_schematics",),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Drawing borehole schematic diagrams with matplotlib",
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
