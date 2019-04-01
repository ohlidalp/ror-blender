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

import bpy

"""
    A representation of Rigs of Rods softbody physics actor (aka 'truck')
    Class names are chosen to be consistent with RoR source.
    
    PRESETS:
    Truckfile format uses directives 'set_node_defaults' and 'set_beam_defaults' to set parameters for following node/beam lines.
    This addon refers to the data as 'presets' because they can be (re)assigned and modified freely using UI.
    However, classes are named '*Defaults' for consistency with RoR sources.

    Author: Petr Ohlidal 2019
"""


class RoR_RigDef(bpy.types.PropertyGroup):
    """ A RoR softbody physics actor - can be anything from a soda can to a space shuttle """ 

    @classmethod
    def register(cls):
        cls.beam_presets = bpy.props.CollectionProperty(type=RoR_BeamDefaults, name="Beam presets", description="Truckfile: `set_beam_defaults`")
        cls.active_beam_preset_index = bpy.props.IntProperty()

        bpy.types.Object.rig_def = bpy.props.PointerProperty(type=cls, name="RoR Rig definition", description="")
        print('Done reg. RoR_RigDef')

    @classmethod
    def unregister(cls):
        del bpy.types.Object.rig_def


class RoR_BeamDefaults(bpy.types.PropertyGroup):
    """ A preset for physical parameters of softbody edge (aka 'beam' in RoR jargon) """

    @classmethod
    def register(cls):
        print('registering RoR_BeamDefaults')
        cls.args_line = bpy.props.StringProperty(name="Arguments", description="Text line with arguments")
        print('done registering RoR_BeamDefaults')
