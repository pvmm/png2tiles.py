# png2tiles.py

This is a new version of `png2tiles.py` that changes functionality considerably when
compared to the [ubox MSX lib](https://gitlab.com/reidrac/ubox-msx-lib) version.

Introduced `--preferred-bg` and `--preferred-fg` options with the following rules:

* If a 8x1 block (8 pixels aligned) contains color X, `--prefered-fg X` will set X
as the MSN (most significant nibble) in the respective colour byte, which is the
foreground colour position.

* If a 8x1 block (8 pixels aligned) contains color X, `--prefered-bg X` will set X
as the LSN (least significant nibble) in the respective colour byte, which is the
background colour position.

* if the 8x1 block has a single colour (white for instance), `--preferred-bg X`
will set the background to X, which means that pixels/colours of the block are now
`0xff/0xfX`. And in case of `--preferred-bg 15`, pixels/colours values of the block
are now `0x00/0xYf` (where Y is defined by `--preferred-fg Y` or defaults to 1).

* if the 8x1 block has a single colour (white for instance), `--preferred-fg X`
will set the foreground to X, which means that pixels/colours of the block are now
`0x00/0xXf`. And in case of `--preferred-fg 15`, pixels/colours values of the block
are now `0xff/0xfY` (where Y is defined by `--preferred-bg Y` or defaults to 1).

* `--preferred-bg X` has precedence over `--preferred-fg Y`, so in a Z-coloured
8x1 block, pixels/colour of the block are set to `0xff/0xZX` instead of `0x00/0xYZ`.

## Copying

This software is distributed under the MIT license, unless stated otherwise.

See [COPYING](https://gitlab.com/pvmm/png2tiles.py/-/blob/main/COPYING) file.

**TL;DR**: the only condition is that you are required to preserve the copyright
and license notices. Licensed works, modifications, and larger works may be
distributed under different terms and without source code; this includes any game
made with the help of this software.

This is a spin-off of `png2tiles.py` tool from the
[ubox MSX lib](https://gitlab.com/reidrac/ubox-msx-lib), which is also MIT licensed.

Some of the contents and structure of this README.md were shamelessly copied from
ubox's [README.md](https://gitlab.com/reidrac/ubox-msx-lib/-/blob/main/README.md).
