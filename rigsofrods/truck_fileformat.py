# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
    Data structures and input/output helpers

    Author: Petr Ohlidal 2019
"""

# Blender's UV layers always contain all vertices, but RoR's `texcoords` section explicitly lists used vertices.
# To disambiguate when editing and exporting, the "unused" vertices are assigned with the following value:
UNUSED_UV = (-1.0, -1.0)

def uv_used(val):
    return val[0] > UNUSED_UV[0] and val[1] >  UNUSED_UV[1]

class Submesh():
    def __init__(self, idx):
        self.line_idx = idx
        self.backmesh = False
        self.texcoords = {} # int -> (float, float)
        self.cabs = []
