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

### JLCPCB Part Number Selection

In some cases, JLCPCB's BOM parsing fails to match the correct part number for
the generated BOM, particularly if the supplier uses different part numbers
for different packaging (e.g. reel suffixes.)

If that is the case, you can add an attribute named `JLCPCBPART#` to the
component, either in your library or design. As long as the attributes are
exported in the CAM files, the attribute will be present in the generated BOM
listing.

## Compatibility

The tool has been developed with Python 3.8 on Windows, but it should be
compatible with any reasonably modern Python on any operating system.

## Notes

I am providing code in the repository to you under an open source license.
Because this is my personal repository, the license you receive to my code
is from me and not my employer. (Facebook)
