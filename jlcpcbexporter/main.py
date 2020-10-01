# SPDX-FileCopyrightText: 2020 Diego Elio Pettenò
#
# SPDX-License-Identifier: MIT

import csv
import pathlib
import re
import zipfile

import click

_EAGLE_ASSEMBLY_DIR = "CAMOutputs/Assembly/"

_JLC_LAYER_TO_CAM = {
    "top": "front",
    "bottom": "back",
}

_CPL_HEADERS = ["Designator", "Mid X ", "Mid Y", "Layer", "Rotation"]
_BOM_HEADERS = ["Comment", "Designator", "Footprint", "LCSC Part #"]


def _calculate_dynamic_fixed_widths(headers):
    widths = []
    for header in re.split(r" ", headers):
        if header:
            widths.append(len(header) + 1)
        else:
            widths[-1] += 1

    return widths


def _split_by_widths(row, widths):
    columns = []
    cursor = 0
    for width in widths:
        columns.append(row[cursor : cursor + width].rstrip())
        cursor += width
    return columns


def _parse_eagle_parts_list(partslist):
    lines = re.split("\r?\n", partslist)

    headers = lines[2]
    column_widths = _calculate_dynamic_fixed_widths(headers)

    column_headers = _split_by_widths(headers, column_widths)
    parts = [
        dict(zip(column_headers, _split_by_widths(row, column_widths)))
        for row in lines[3:]
    ]
    return parts


@click.command()
@click.option("--layer", type=click.Choice(["top", "bottom"]), default="top")
@click.argument("cam_zip_files", type=click.File("rb"), nargs=-1, required=True)
def generate(*, layer, cam_zip_files):
    cam_layer = _JLC_LAYER_TO_CAM[layer]

    for cam_zip_file in cam_zip_files:
        filename = pathlib.Path(cam_zip_file.name)
        output_bom_file = open(f"{filename.parent / filename.stem}_bom.csv", mode="wt")
        output_cpl_file = open(f"{filename.parent / filename.stem}_cpl.csv", mode="wt")

        zip_path = zipfile.Path(cam_zip_file, at=_EAGLE_ASSEMBLY_DIR)

        (assembly_file,) = [
            filepath
            for filepath in zip_path.iterdir()
            if not filepath.name.startswith("PnP_")
        ]
        assembly_basename = pathlib.Path(assembly_file.name).stem
        click.echo(f"CAM Basename is {assembly_basename}")

        assembly_content = assembly_file.read_text()
        eagle_parts = list(_parse_eagle_parts_list(assembly_content))

        bom_csv = csv.writer(output_bom_file, dialect="unix")
        for part in eagle_parts:
            if part["Value"]:
                bom_csv.writerow([part["Value"], part["Parts"], part["Package"], ""])

        pnp_path = zip_path / f"PnP_{assembly_basename}_{cam_layer}.txt"
        assert pnp_path.exists()

        cpl_csv = csv.writer(output_cpl_file, dialect="unix")
        cpl_csv.writerow(_CPL_HEADERS)

        pnp_content = pnp_path.read_text()
        for row in re.split("\r?\n", pnp_content):
            # values are 'designator', 'x', 'y', 'rotation', 'value', 'footprint'
            if not row:
                continue
            values = row.split("\t")
            cpl_csv.writerow([values[0], values[1], values[2], layer, values[3]])


if __name__ == "__main__":
    generate()
