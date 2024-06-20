#!/usr/bin/env python3
#
# Copyright (C) 2019 by Juan J. Martinez  <jjm@usebox.net>
# Copyright (C) 2021 by Rodrigo Siqueira
# Copyright (C) 2024 by Pedro de Medeiros <pedro.medeiros@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from argparse import ArgumentParser
from PIL import Image
from collections import defaultdict
from string import digits
from random import sample

import os
import subprocess
import sys
import tempfile
import traceback


__version__ = "1.1"
# Changes by Rodrigo Siqueira - May 2021
# ZX0 Compression
# APLIB Compression

# ALTERNATE MSX PALLETE
MSX_COLORS = [
    (0xff, 0x00, 0xff),
    (0x00, 0x00, 0x00),
    (0x20, 0x20, 0x20),
    (0x52, 0x27, 0x00),
    (0x00, 0x73, 0x27),
    (0x00, 0x9b, 0x52),
    (0x00, 0xba, 0x00),
    (0x73, 0x73, 0x73),
    (0xff, 0x27, 0x27),
    (0x27, 0x52, 0xff),
    (0xff, 0x27, 0x9b),
    (0xff, 0x9b, 0x27),
    (0x00, 0xba, 0xff),
    (0xba, 0xba, 0xba),
    (0xff, 0xe0, 0x00),
    (0xff, 0xff, 0xff),
]

def apultra_compress(data):
    with tempfile.NamedTemporaryFile(mode="wb") as fd:
        fd.write(bytearray(data))
        ap_name = fd.name + ".ap"
        subprocess.call(["apultra", "-v", fd.name, ap_name], stdout=sys.stderr)

    with open(ap_name, "rb") as fd:
        out = fd.read()
        os.unlink(fd.name)

    return [int(byte) for byte in out]


def zx0_compress(data):
    with tempfile.NamedTemporaryFile(mode="wb") as fd:
        fd.write(bytearray(data))
        zx_name = filename + ".zx0"
        subprocess.call(["zx0", filename, zx_name], stdout=sys.stderr)

    with open(zx_name, "rb") as fd:
        out = fd.read()
        os.unlink(fd.name)

    return [int(byte) for byte in out]


def to_hex_list_str(src):
    out = ""
    for i in range(0, len(src), 8):
        out += ', '.join(["0x%02x" % int(b) for b in src[i:i + 8]]) + ",\n"
    return out


def to_hex_list_str_asm(src):
    out = ""
    for i in range(0, len(src), 8):
        out += '\tdb ' + ', '.join(["#%02x" % b for b in src[i:i + 8]])
        out += '\n'
    return out


def main():
    parser = ArgumentParser(description="PNG to SCREEN5",
                            epilog="Copyright (C) 2024 Pedro de Medeiros <pedro.medeiros@gmail.com>")
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("-i", "--id", dest="id", default="tileset", type=str,
                        help="variable name (default: tileset)")
    parser.add_argument("-p", "--palette", dest="palette", default="default", type=str,
                        help="palette file (default to builtin palette)")
    parser.add_argument("-a", "--asm", dest="asm", action="store_true",
                        help="ASM output (default: C header)")
    parser.add_argument("--aplib", dest="aplib", action="store_true",
                        help="APLIB compressed")
    parser.add_argument("-z", "--zx0", dest="zx0", action="store_true",
                        help="ZX0 compressed")

    parser.add_argument("image", help="image to convert")

    args = parser.parse_args()

    if args.aplib and args.zx0:
        parser.error("Can't compress image again to same output. Choose between APLIB or ZX0")

    try:
        image = Image.open(args.image)
    except IOError:
        parser.error("failed to open the image")

    if image.mode != "RGB":
        image = image.convert('RGB')

    (w, h) = image.size
    if w != 256:
        parser.error("\"%s\" image width is not 256 pixels wide (SCREEN5): %d" %
                     (args.image, w))

    data = image.getdata()
    out = []
    size = 0
    for y in range(0, h):
        # put pixels from each row in a list
        row = [data[x + (y * w)] for x in range(w)]
        colors = []
        for x, c in enumerate(row):
            try:
                colors.append(MSX_COLORS.index(c))
            except ValueError as e:
                parser.error("pixel at (%d, %d) has a color not in the "
                             "expected MSX palette: %s" % (x, y, e.args[0]))
        # Update pattern table contents
        for c1, c2 in zip(colors[0::2], colors[1::2]):
            # each tile has 2 pixels per byte (4bpp)
            out.append((c1 << 4) | c2)

        size += 128

    if args.aplib:
        out = apultra_compress(out)

    if args.zx0:
        out = zx0_compress(out)

    if args.asm:
        if args.aplib:
            print(";; APLIB compressed")
        elif args.zx0:
            print(";; ZX0 compressed")
        else:
            print(";; RAW - not compressed")
        print(".equ sc5_%s_size %d\n" % (args.id, size))
        print("%s:" % args.id)
        print(to_hex_list_str_asm(out))
    else:
        print("#ifndef _%s_H" % args.id.upper())
        print("#define _%s_H\n" % args.id.upper())
        if args.aplib:
            print("/* APLIB compressed */")
        elif args.zx0:
            print("/* ZX0 compressed */")
        else:
            print("/* RAW - not compressed */")
        print("/* %d tiles */\n" % ntiles)

        data_out = to_hex_list_str(out)
        print("#define SC5_%s_SIZE %d\n" % (args.id.upper(), size))
        print("const unsigned char %s[%d] = {\n%s\n};\n" %
              (args.id, len(out), data_out))
        print("#endif // _%s_H\n" % args.id.upper())

if __name__ == "__main__":
    main()
