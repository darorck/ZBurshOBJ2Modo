#!/usr/bin/env python

################################################################################
#
# ImportZObj.py
#
# Version: 0.1
#
# Compatible versions: MODO 901+ as it uses Python TD
#
# Author: darorck
#
# Description: A Script to open ZBrush custom OBJ files with vertex colors in MODO 901+
#
# Usage: copy it in ..AppData\Roaming\Luxology\Scripts and run it writing @ImportZObj.py
#
# Created: 30 Oct 2016
#
# Last Update: 30 Oct 2016
#
################################################################################

import traceback
import lx
import modo

def main():
    # Store the vertex colors
    vcolors = []

    # Create dialog to select the OBJ file
    lx.eval("dialog.setup fileOpen")
    lx.eval('dialog.open')
    objfile = lx.eval("dialog.result ?")

    def tofloat(hex):
        """Convert hex color code to OpenGL float"""
        return (1.0 / 255) * ord(hex.decode('hex'))

    def splitline(line):
        """Convert hex color code to OpenGL float"""

        ini = 6
        end = ini + 8
        while ini < len(line):
            val = line[ini:end]
            color = tofloat(val[2:4]), tofloat(val[4:6]), tofloat(val[6:8])
            vcolors.append(color)
            ini = end
            end = ini + 8

    # Reads the OBJ file looking for vertex information
    with open(objfile, 'r') as f:
        for line in f:
            if line[0:5] == '#MRGB':
                splitline(line.strip())

    # Default mesh name
    mesh = modo.Mesh('Mesh')

    # Creates a new vertex map
    vexmap = mesh.geometry.vmaps.addRGBMap('ZVertexColor')

    for vertex_index, color in enumerate(vexmap):
        vexmap[vertex_index] = vcolors[vertex_index]

    # Update the changes
    mesh.geometry.setMeshEdits()

if __name__ == '__main__':
    try:
        main()
    except:
        lx.out(traceback.format_exc())
