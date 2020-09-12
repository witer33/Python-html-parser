# Python HTML Parser - A simple, fast and pure-python HTML parser
# Copyright (C) 2020-2021 witer33 <https://github.com/witer33>
#
# This file is part of Python HTML Parser.
#
# Python HTML Parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Python HTML Parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Python HTML Parser.  If not, see <http://www.gnu.org/licenses/>.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="PyHTML",
    version="0.1.0",
    author="Witer33",
    author_email="dev@witer33.com",
    description="A simple, fast and pure-python HTML parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/witer33/Python-HTML-Parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ],
    python_requires='>=3.5'
)
