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

# Author: Ulteq (https://github.com/ulteq)

import bpy
import bmesh
from bpy_extras.io_utils import ExportHelper
from . import truck_fileformat

def export_menu_func(self, context):
    self.layout.operator(ROR_OT_truck_export.bl_idname, text="Truck (.truck)")

class ROR_OT_truck_export(bpy.types.Operator, ExportHelper):
    bl_idname = "export_truck.truck"
    bl_label = "Export RoR Truck"
    filename_ext = ""
    filter_glob: bpy.props.StringProperty(
            default="*.truck;*.trailer;*.load;*.car;*.boat;*.airplane;*.train;*.machine;*.fixed",
            options={'HIDDEN'},
            )
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        nodes = []
        beams = []
        submeshes = []

        for obj in context.selected_objects[:1]:
            if obj.type != 'MESH':
                continue

            current_mode = bpy.context.object.mode
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.mode_set(mode="EDIT")
            bm = bmesh.from_edit_mesh(obj.data)

            group_names = {group.index : group.name for group in obj.vertex_groups}
            node_digits = len(str(len(obj.data.vertices) - 1))

            format_string = '{:'+str(node_digits)+'d}, {: 8.3f}, {: 8.3f}, {: 8.3f}'
            presets_key = bm.verts.layers.int.get("presets")
            options_key = bm.verts.layers.string.get("options")
            bm.verts.ensure_lookup_table()
            for v, bv in zip(obj.data.vertices, bm.verts):
                preset_idx = -1
                if presets_key:
                    preset_idx = bv[presets_key];
                options = ''
                if options_key:
                    options = bv[options_key].decode()
                if not options:
                    options = 'n'
                groups = [group_names[g.group] for g in v.groups]
                nodes.append([format_string.format(v.index, v.co[1], v.co[2], v.co[0]), options, groups, preset_idx])

            format_string = '{:'+str(node_digits)+'d}, {:'+str(node_digits)+'d}'
            presets_key = bm.edges.layers.int.get("presets")
            options_key = bm.edges.layers.string.get("options")
            bm.edges.ensure_lookup_table()
            for e, be in zip(obj.data.edges, bm.edges):
                preset_idx = -1
                if presets_key:
                    preset_idx = be[presets_key]
                options = ''
                if options_key:
                    options = be[options_key].decode()
                if not options:
                    options = 'v'
                ids = sorted([[g.group for g in obj.data.vertices[e.vertices[i]].groups] for i in [0, 1]])
                vg1, vg2 = [[group_names[g] for g in ids[i]] for i in [0, 1]]
                groups = vg1 if vg1 == vg2 else [', '.join(vg1)] + [">"] + [', '.join(vg2)]
                beams.append([ids, groups, format_string.format(e.vertices[0], e.vertices[1]), options, preset_idx])

            # Truckfile section 'submesh'
            # faces with UVs defined (see `truck_fileformat.INVALID_UV`) are assigned to respective submeshes
            # faces without UVs (if present) are put in dedicated submesh at the end
            options_key = bm.faces.layers.string.get("options")
            claimed_key = bm.faces.layers.int.new("claimed")
            bm.faces.ensure_lookup_table()
            bm.verts.index_update()
            for uv_name, uv_key in bm.loops.layers.uv.items():
                print("DBG export: processing uv layer {} -> {}".format(uv_name, uv_key))
                name_tok = uv_name.split(' ')
                if name_tok and 'submesh' in name_tok[0]:
                    submesh = truck_fileformat.Submesh(0)
                    submesh.line_idx = int(name_tok[1]) if len(name_tok) > 1 else 0
                    submesh.backmesh = 'backmesh' in name_tok[2] if len(name_tok) > 2 else False
                    print("> DBG export: created submesh, line:{}, backmesh:{}".format(submesh.line_idx, submesh.backmesh))
                    for bf in bm.faces:
                        if (
                                len(bf.verts) == 3 and
                                truck_fileformat.uv_used(bf.loops[0][uv_key].uv) and
                                truck_fileformat.uv_used(bf.loops[1][uv_key].uv) and
                                truck_fileformat.uv_used(bf.loops[2][uv_key].uv)
                            ):
                            bf[claimed_key] = 1
                            print("> > DBG export: face {} claimed by uv-layer {}".format([bf.verts[0].index, bf.verts[1].index, bf.verts[2].index], uv_key))
                            for i in range(0, 2):
                                submesh.texcoords[bf.verts[i].index] = bf.loops[i][uv_key].uv
                            options = ''
                            if options_key:
                                options = bf[options_key].decode()
                            if not options:
                                options = 'c'
                            submesh.cabs.append([bf.verts[0].index, bf.verts[1].index, bf.verts[2].index, options])
                    submeshes.append(submesh)
                    print("> DBG export: added submesh with {} texcoords and {} cabs".format(len(submesh.texcoords), len(submesh.cabs)))

            submesh_no_uv = truck_fileformat.Submesh(0)
            for bf in bm.faces:
                if bf[claimed_key] == 0:
                    options = ''
                    if options_key:
                        options = bf[options_key].decode()
                    if not options:
                        options = 'c'
                    submesh_no_uv.cabs.append([bf.verts[0].index, bf.verts[1].index, bf.verts[2].index, options])
            if submesh_no_uv.cabs:
                submeshes.append(submesh_no_uv)

            bpy.ops.object.mode_set(mode=current_mode)
            bm.free()

        indices = [0, 0, 0]
        truck = obj.ror_truck
        truckfile = []
        for entry in truck.truckfile_lines:
            truckfile.append(entry.line)

        with open(self.filepath, 'w') as f:
            for line in truckfile[:truck.truckfile_name_pos]:
                print (line, file=f)

            print(obj.name, file=f)

            for line in truckfile[truck.truckfile_name_pos:truck.truckfile_nodes_pos]:
                print (line, file=f)

            print("nodes", file=f)
            node_preset_idx = -1 # -1 means 'not set'
            vertex_groups = []
            for n in sorted(nodes):
                if n[-1] != node_preset_idx:
                    node_preset_idx = n[-1]
                    if node_preset_idx == -1:
                        print('set_node_defaults -1, -1, -1, -1', file=f) # reset all to builtin values
                    else:
                        print (truck.node_presets[node_preset_idx].args_line, file=f)
                if n[-2] != vertex_groups:
                    vertex_groups = n[-2]
                    print (";grp:", ', '.join(vertex_groups), file=f)
                print (*n[:-2], sep=', ', file=f)

            lines = truckfile[truck.truckfile_nodes_pos:truck.truckfile_beams_pos]
            if not lines:
                lines = ['']
            for line in lines:
                print (line, file=f)

            print("beams", file=f)
            beam_preset_idx = -1
            edge_groups = []
            for b in sorted(beams):
                if b[-1] != beam_preset_idx:
                    beam_preset_idx = b[-1]
                    if beam_preset_idx == -1:
                        print('set_beam_defaults -1, -1, -1, -1', file=f) # reset all to builtin values
                    else:
                        print (truck.beam_presets[beam_preset_idx].args_line, file=f)
                if b[1] != edge_groups:
                    edge_groups = b[1]
                    print (";grp:", *edge_groups, file=f)
                print (*b[2:-1], sep=', ', file=f)

            cab_format_string = '{:'+str(node_digits)+'d}, {:'+str(node_digits)+'d}, {:'+str(node_digits)+'d}'
            uv_format_string = '{:'+str(node_digits)+'d}, {}, {}'
            prev_line_idx = truck.truckfile_beams_pos
            for s in submeshes:
                print("DBG write: submesh with {} texcoords and {} cabs".format(len(s.texcoords), len(s.cabs)))
                # Scroll down to position
                lines = truckfile[prev_line_idx:s.line_idx]
                print("> DBG write: printing {} lines, range: [{} : {}]".format(len(lines), prev_line_idx, s.line_idx))
                if not lines:
                    lines = ['']
                for line in lines:
                    print (line, file=f)
                prev_line_idx = s.line_idx
                # Print data
                print("submesh", file=f)
                if s.backmesh:
                    print("backmesh", file=f)
                if s.texcoords:
                    print("texcoords", file=f)
                    for t_node, t_uv in s.texcoords.items():
                        print(uv_format_string.format(t_node, t_uv[0], t_uv[1]), file=f)
                print("cab", file=f)
                for c in s.cabs:
                    nodes_str = cab_format_string.format(c[0], c[1], c[2])
                    print(*[nodes_str, c[3]], sep=', ', file=f)

            for line in truckfile[truck.truckfile_submesh_pos:]:
                print (line, file=f)

        return {'FINISHED'}
