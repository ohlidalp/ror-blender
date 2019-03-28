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

bl_info = {
    "name": "Rigs of Rods Tools",
    "author": "Ulteq, only_a_ptr",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "category": "RoR",
    }

if "bpy" in locals():  # Handle reload of Blender addon
    import importlib
    importlib.reload(truck_import)
    importlib.reload(truck_export)
else:
    from . import truck_import
    from . import truck_export

import bpy
import os
import bmesh
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

def register():
    bpy.app.debug = True
    bpy.utils.register_class(truck_import.import_op)
    bpy.utils.register_class(truck_export.export_op)
    bpy.types.TOPBAR_MT_file_import.append(truck_import.import_menu_func)
    bpy.types.TOPBAR_MT_file_export.append(truck_export.export_menu_func)

def unregister():
    bpy.utils.unregister_class(truck_import.import_op)
    bpy.utils.unregister_class(truck_export.export_op)
    bpy.types.TOPBAR_MT_file_import.remove(truck_import.import_menu_func)
    bpy.types.TOPBAR_MT_file_export.remove(truck_export.export_menu_func)

if __name__ == "__main__":
    register()
