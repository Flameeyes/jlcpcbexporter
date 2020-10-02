<!--
SPDX-FileCopyrightText: 2020 Diego Elio Pettenò

SPDX-License-Identifier: MIT
-->

# `jlcpcbexporter`

Tool to generate BOM and CPL files compatible with JLCPCB's SMT process.

This tool takes an EAGLE CAM export zip file, and generates comma-separated
values (CSV) files that can be uploaded to JLCPCB's web interface to request
SMT treatment for a board.

## Usage

```
$ pip install jlcbpcexporter
$ jlcpcbexporter --layer top eagle-cam-export.zip
```

The `--layer` flag selects between `top` and `bottom` layer, as JLCPCB only
allows SMT on one of the two.

## Compatibility

The tool has been developed with Python 3.8 on Windows, but it should be
compatible with any reasonably modern Python on any operating system.

## Notes

I am providing code in the repository to you under an open source license.
Because this is my personal repository, the license you receive to my code
is from me and not my employer. (Facebook)
