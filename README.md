# GHEtool GUI

[![Tests](https://github.com/wouterpeere/GHEtool-GUI/actions/workflows/test.yml/badge.svg)](https://github.com/wouterpeere/GHEtool-GUI/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/wouterpeere/GHEtool-GUI/graph/badge.svg?token=uf1owumb25)](https://codecov.io/gh/wouterpeere/GHEtool-GUI)
[![Documentation Status](https://readthedocs.org/projects/ghetool-gui/badge/?version=latest)](https://ghetool-gui.readthedocs.io/en/latest/?badge=latest)

## What is GHEtool GUI?

This repository contains a Graphical User Interface for the python package [GHEtool](https://github.com/wouterpeere/GHEtool).
It is an open-source alternative for the professional version of GHEtool, which can be found on the website [https://ghetool.eu](https://ghetool.eu).
This GUI is built using [ScenarioGUI](https://github.com/tblanke/ScenarioGUI) and can be downloaded as an executable [here](https://ghetool.eu/community/).

**Please note that this version is developed and maintained by the community and has no official support from the developers of GHEtool Pro.**

<p align="center">
<img src="https://raw.githubusercontent.com/wouterpeere/GHEtool-GUI/main/docs/GHEtool.png" width="600">
</p>

## Development
This open-source graphical user interface is maintained by the community of users and welcomes also your contribution!
Below you can find the requirements of running GHEtool GUI yourself. More information about the package
structure and executable-creation can be found on our [readthedocs](https://ghetool-gui.readthedocs.io/en/latest/).

### Requirements
This code is tested with Python 3.10 and requires the following libraries (the versions mentioned are the ones with which the code is tested)

* GHEtool (=2.2.0)
* ScenarioGUI (>=0.3.0)

For the tests

* Pytest (>=7.1.2)

## License

*GHEtool GUI* is licensed under the terms of the 3-clause BSD-license.
See [GHEtool GUI license](LICENSE).

## Citation
Please cite this GHEtool GUI using the JOSS paper.

Peere, W., Blanke, T.(2022). GHEtool: An open-source tool for borefield sizing in Python. _Journal of Open Source Software, 7_(76), 4406, https://doi.org/10.21105/joss.04406
