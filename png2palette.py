#!/usr/bin/env python3
#
# Copyright (C) 2024 by Rodrigo Siqueira and Pedro de Medeiros <pedro.medeiros@gmail.com>
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

__version__ = "1.0"

def main():
    parser = ArgumentParser(description="Generate a MSX2 RGB9 Palette from 16 colors PNG file",
                            epilog="Copyright (C) 2024 Rodrigo Siqueira and Pedro de Medeiros",
                            )
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("image", help="16 colors PNG image to process")

    args = parser.parse_args()

    try:
        image = Image.open(args.image)
    except IOError:
        parser.error("failed to open the image")

    if image.mode != "RGB":
        image = image.convert('RGB')
        
    if image.mode != "RGB":
        parser.error("not a RGB image (%s)" % (image.mode))

    (w, h) = image.size
    data = image.getdata()

    png16palette = {}
    for y in range(0, h):
        for x in range(0, w):
            pixel = data[x + (y * w)]
            png16palette[pixel] = png16palette.get(pixel, 0) + 1
    if len(png16palette) > 16:
        parser.error("more than 16 colors")
    elif len(png16palette) < 16:
        print(f"# warning: less than 16 colors found ({len(png16palette)}).")

    rgb9palette = []
    for rgb in png16palette:
        tmp = rgb[0] >> 5, rgb[1] >> 5, rgb[2] >> 5
        rgb9palette.append(tmp)

    # Print tuple data
    print("\npalette = [")
    for r,g,b in png16palette:
        print(f"({r:3}, {g:3}, {b:3}),")
    print("]\n")
    # Print assembly data
    PERLINE = 4
    print(f"; {len(rgb9palette)} x 0x0GRB")
    for n, (r,g,b) in enumerate(rgb9palette, start=0):
        if n == 0: print(".dw", end='')
        elif n % PERLINE == 0: print(f"\n.dw", end='')
        print(f" 0x0{g:x}{r:x}{b:x},", end='')
    print()

if __name__ == "__main__":
    main()
