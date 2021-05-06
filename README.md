py_edl_editor
=============

A python EDL (Edit Decision List) GUI, based on the EDL library
by Simon Hargreaves https://pypi.org/project/edl/ which is using
[pytimecode](https://code.google.com/p/pytimecode/).
Also using the cdl_convert library by Sean Wallitsch:
https://github.com/shidarin/cdl_convert

Work in progress, so collaboration welcome.

![py_edl_editor](py_edl_editor_gui.png?raw=true)

Reqirements:

    pip install PySide2
    pip install cdl_convert
    pip install opentimelineio
    pip install timecode
    pip install edl


Usage without EDL:

    python __main__.py

Usage with EDL:

    python __main__.py [path_to_edl] [framerate]
    python __main__.py path_to_edl.edl 24

Accepted framerate values ['60', '59.94', '50', '30', '29.97', '25', '24',
'23.98'].

(The MIT License)

Copyright © 2021 Thomas Weckenmann <tweckenmann0711@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the ‘Software’), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ‘AS IS’, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
