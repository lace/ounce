ounce
=====

[![version](https://img.shields.io/pypi/v/ounce?style=flat-square)][pypi]
[![python version](https://img.shields.io/pypi/pyversions/ounce?style=flat-square)][pypi]
[![license](https://img.shields.io/pypi/l/ounce?style=flat-square)][pypi]
[![](https://img.shields.io/badge/coverage-100%25-brightgreen?style=flat-square)][coverage]
[![build](https://img.shields.io/circleci/project/github/lace/ounce/master?style=flat-square)][build]
[![docs build](https://img.shields.io/readthedocs/ounce?style=flat-square)][docs build]
[![code style](https://img.shields.io/badge/code%20style-black-black?style=flat-square)][black]

Fast, simple, non-fancy, and non-magical package for manipulating units of
measure.

It's a faster and less fancy counterpart to [Pint][].

[pypi]: https://pypi.org/project/ounce/
[coverage]: https://github.com/lace/ounce/blob/master/.coveragerc
[build]: https://circleci.com/gh/lace/ounce/tree/master
[docs build]: https://ounce.readthedocs.io/en/latest/
[black]: https://black.readthedocs.io/en/stable/
[numpy]: https://www.numpy.org/
[pint]: https://pint.readthedocs.io/

Installation
------------

```sh
pip install ounce
```


Usage
-----

```py
import ounce

value, units = ounce.convert(value, "in", "cm")
```


Versioning
----------

This library adheres to [Semantic Versioning][semver].

[semver]: https://semver.org/


Development
-----------

First, [install Poetry][].

After cloning the repo, run `./bootstrap.zsh` to initialize a virtual
environment with the project's dependencies.

Subsequently, run `./dev.py install` to update the dependencies.

[install poetry]: https://python-poetry.org/docs/#installation


Acknowledgements
----------------

This was extracted from [blmath][] by [Paul Melnikow][]. blmath itself was
extracted from the Body Labs codebase and open-sourced by [Alex Weiss][].

[blmath]: https://github.com/metabolize/blmath
[paul melnikow]: https://github.com/paulmelnikow
[alex weiss]: https://github.com/algrs


License
-------

The project is licensed under the two-clause BSD license.
