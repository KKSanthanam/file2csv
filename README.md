# File2CSV

Fixed width file to CSV

## Parse fixed width file

- Generates a fixed width file using the provided spec (offset provided in the spec file represent the length of each field).
- Implements a parser that can parse the fixed width file and generate a delimited file, like CSV for example.

### Features

- fixed2csv encoder
- docker image to run the Apache Beam
- CI/CD for publishing the PyPi package

### Installation

_file2csv_ is a registered [PyPI module](https://pypi.python.org/pypi/file2csv), so the installation
with _pip_ is quite easy:

```console
pip install file2csv
```

Apache beam is built into docker image

Build docker image
```console
./dockerbuild.sh
```

Run docker image with _remotedata_ volume
```console
./dockerrun.sh
```

## Development

- Source hosted at [GitHub](https://github.com/KSanthanam/file2csv)
- Python module hostet at [PyPI](https://pypi.python.org/pypi/file2csv)
- Report issues, questions, feature requests on
  [GitHub Issues](https://github.com/KSanthanam/file2csv/issues)

## License

The MIT License (MIT)

Copyright (c) 2019 KK Santhanam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## Authors

KK Santhanam ([KSanthanam](https://github.com/KSanthanam))
