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
from math import sqrt

MAX_VALUE = 9999
MSX2_RBG9_PALETTE = {
    (  0,  0,  0): '0x0000',
    ( 36,  1,  0): '0x0010',
    ( 72,  4,  0): '0x0020',
    (107,  9,  0): '0x0030',
    (143, 16,  0): '0x0040',
    (180, 23,  0): '0x0050',
    (216, 30,  0): '0x0060',
    (252, 36,  1): '0x0070',
    (  0, 36,  0): '0x0100',
    ( 36, 36,  0): '0x0110',
    ( 72, 36,  0): '0x0120',
    (107, 36,  0): '0x0130',
    (143, 36,  0): '0x0140',
    (180, 36,  0): '0x0150',
    (216, 36,  0): '0x0160',
    (252, 37,  2): '0x0170',
    (  0, 72,  0): '0x0200',
    ( 36, 72,  0): '0x0210',
    ( 72, 72,  0): '0x0220',
    (107, 72,  0): '0x0230',
    (143, 72,  0): '0x0240',
    (180, 72,  0): '0x0250',
    (216, 72,  0): '0x0260',
    (252, 72,  0): '0x0270',
    (  2,108,  0): '0x0300',
    ( 36,108,  0): '0x0310',
    ( 72,108,  0): '0x0320',
    (107,108,  0): '0x0330',
    (143,108,  0): '0x0340',
    (180,108,  0): '0x0350',
    (216,108,  0): '0x0360',
    (252,108,  0): '0x0370',
    (  0,143,  0): '0x0400',
    ( 35,143,  0): '0x0410',
    ( 74,143,  0): '0x0420',
    (108,143,  0): '0x0430',
    (144,144,  0): '0x0440',
    (180,144,  0): '0x0450',
    (216,144,  0): '0x0460',
    (252,144,  0): '0x0470',
    (  0,180,  0): '0x0500',
    ( 34,180,  0): '0x0510',
    ( 71,180,  0): '0x0520',
    (108,180,  0): '0x0530',
    (145,180,  0): '0x0540',
    (180,180,  0): '0x0550',
    (216,180,  0): '0x0560',
    (253,180,  0): '0x0570',
    (  0,216,  0): '0x0600',
    ( 34,216,  0): '0x0610',
    ( 71,216,  0): '0x0620',
    (106,216,  0): '0x0630',
    (144,216,  0): '0x0640',
    (180,216,  0): '0x0650',
    (216,216,  0): '0x0660',
    (252,216,  0): '0x0670',
    (  0,249,  0): '0x0700',
    ( 37,249,  0): '0x0710',
    ( 70,249,  0): '0x0720',
    (108,250,  0): '0x0730',
    (144,250,  0): '0x0740',
    (180,250,  0): '0x0750',
    (216,250,  0): '0x0760',
    (252,251,  0): '0x0770',
    (  0,  0, 36): '0x0001',
    ( 36,  1, 36): '0x0011',
    ( 72,  4, 36): '0x0021',
    (107,  9, 36): '0x0031',
    (143, 16, 36): '0x0041',
    (180, 23, 36): '0x0051',
    (216, 30, 36): '0x0061',
    (252, 36, 36): '0x0071',
    (  0, 36, 36): '0x0101',
    ( 36, 36, 36): '0x0111',
    ( 72, 36, 36): '0x0121',
    (107, 36, 36): '0x0131',
    (143, 36, 36): '0x0141',
    (180, 36, 36): '0x0151',
    (216, 36, 36): '0x0161',
    (252, 37, 36): '0x0171',
    (  0, 72, 36): '0x0201',
    ( 36, 72, 36): '0x0211',
    ( 72, 72, 36): '0x0221',
    (107, 72, 36): '0x0231',
    (143, 72, 36): '0x0241',
    (180, 72, 36): '0x0251',
    (216, 72, 36): '0x0261',
    (252, 72, 36): '0x0271',
    (  2,108, 36): '0x0301',
    ( 36,108, 36): '0x0311',
    ( 72,108, 36): '0x0321',
    (107,108, 36): '0x0331',
    (143,108, 36): '0x0341',
    (180,108, 36): '0x0351',
    (216,108, 36): '0x0361',
    (252,108, 36): '0x0371',
    (  0,143, 36): '0x0401',
    ( 35,143, 36): '0x0411',
    ( 74,143, 36): '0x0421',
    (108,143, 36): '0x0431',
    (144,144, 36): '0x0441',
    (180,144, 36): '0x0451',
    (216,144, 36): '0x0461',
    (252,144, 37): '0x0471',
    (  0,180, 36): '0x0501',
    ( 34,180, 36): '0x0511',
    ( 71,180, 36): '0x0521',
    (108,180, 36): '0x0531',
    (145,180, 36): '0x0541',
    (180,180, 36): '0x0551',
    (216,180, 37): '0x0561',
    (253,180, 37): '0x0571',
    (  0,216, 36): '0x0601',
    ( 34,216, 36): '0x0611',
    ( 71,216, 36): '0x0621',
    (106,216, 36): '0x0631',
    (144,216, 36): '0x0641',
    (180,216, 36): '0x0651',
    (216,216, 36): '0x0661',
    (252,216, 37): '0x0671',
    (  0,249, 36): '0x0701',
    ( 37,249, 36): '0x0711',
    ( 70,249, 36): '0x0721',
    (108,250, 36): '0x0731',
    (144,250, 36): '0x0741',
    (180,250, 36): '0x0751',
    (216,250, 38): '0x0761',
    (252,251, 38): '0x0771',
}

__version__ = "1.0"

def main():
    parser = ArgumentParser(description="Generate a MSX2 RBG9 Palette from 16 colors PNG file",
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
    for (r1,g1,b1) in png16palette:
        tmp = MAX_VALUE
        #print(f"testing ({r1},{g1},{b1})...")
        for r2,g2,b2 in MSX2_RBG9_PALETTE:
            d = sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)
            if min(d, tmp) < tmp:
                #print(f"replace {tmp} with {d} @ ({r2},{g2},{b2})")
                tmp = d
                rgb = r2,g2,b2
        if tmp < MAX_VALUE and not MSX2_RBG9_PALETTE[rgb] in rgb9palette:
            #print(f"@distance {tmp:.8}: found {rgb}: {MSX2_RBG9_PALETTE[rgb]}")
            rgb9palette.append(MSX2_RBG9_PALETTE[rgb])
        else:
            print(f"# warning: 24-bit ({r1},{g1},{b1}) not found:")


    # Print tuple data
    print("\npalette = [")
    for r,g,b in png16palette:
        print(f"({r:3}, {g:3}, {b:3}),")
    print("]\n")
    # Print assembly data
    PERLINE = 4
    print(f"; {len(rgb9palette)} x 0x0GRB")
    for n, index in enumerate(rgb9palette):
        if n == 0: print(".dw", end=" ")
        elif n % PERLINE == 0: print(f"\n.dw", end=" ")
        print(index, end=", ")
    print()

if __name__ == "__main__":
    main()
