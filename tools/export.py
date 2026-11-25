# MIT License

# Copyright (c) 2017 GiveMeAllYourCats

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy

from . import common as Common
from . import settings as Settings
from . import armature_manual
from .register import register_wrap
from .translations import t
from .. import globs


# Export checks
_meshes_count = 0
_tris_count = 0
_mat_list = []
_broken_shapes = []
_textures_found = False

# Bumped these because some of these are done on the unity side a lot of the time. (Mat/Mesh Merging)
max_mats = 999
max_tris = 300000
max_meshes_light = 999
max_meshes_hard = 999


@register_wrap
class ExportModel(bpy.types.Operator):
    bl_idname = 'cats_export.export_model'
    bl_label = t('ExportModel.label')
    bl_description = t('ExportModel.desc')
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    action = bpy.props.EnumProperty(
        items=(('CHECK', '', 'Please Ignore'),
               ('NO_CHECK', '', 'Please Ignore')))

    filepath = bpy.props.StringProperty()

    def execute(self, context):
        meshes = Common.get_meshes_objects()

        # Check for warnings
        if not self.action == 'NO_CHECK':
            global _meshes_count, _tris_count, _mat_list, _broken_shapes, _textures_found

            # Reset export checks
            _meshes_count = 0
            _tris_count = 0
            _mat_list = []
            _broken_shapes = []
            _textures_found = False

            # Check for export warnings
            for mesh in meshes:
                # Check mesh count
                _meshes_count += 1

                # Check tris count
                _tris_count += len(mesh.data.polygons)

                # Check material count and whether the materials use image textures
                for mat_slot in mesh.material_slots:
                    if mat_slot and mat_slot.material and mat_slot.material.users:
                        if mat_slot.material.name not in _mat_list:
                            _mat_list.append(mat_slot.material.name)
                        if not _textures_found and mat_slot.material.use_nodes:
                            for node in mat_slot.material.node_tree.nodes:
                                if node.type == 'TEX_IMAGE' and node.image:
                                    _textures_found = True
                                    break

                if Common.has_shapekeys(mesh):
                    # Check if there are broken shapekeys
                    for shapekey in mesh.data.shape_keys.key_blocks[1:]:
                        vert_count = 0
                        for vert in shapekey.data:
                            vert_count += 1
                            for coord in vert.co:
                                if coord >= 10000:
                                    _broken_shapes.append(shapekey.name)
                                    vert_count = 1000
                                    break
                            # Only check the first 1000 vertices of this shapekey
                            if vert_count == 1000:
                                break

            # Check if a warning should be shown
            if _meshes_count > max_meshes_light \
                    or _tris_count > max_tris \
                    or len(_mat_list) > max_mats \
                    or len(_broken_shapes) > 0 \
                    or not _textures_found and Settings.get_embed_textures():
                bpy.ops.cats_export.display_error('INVOKE_DEFAULT')
                return {'FINISHED'}

        # Check if textures are found and if they should be embedded
        path_mode = 'AUTO'
        if _textures_found and Settings.get_embed_textures():
            path_mode = 'COPY'

        # Open export window
        try:
            if self.filepath:
                bpy.ops.export_scene.fbx('EXEC_DEFAULT',
                                         filepath=self.filepath,
                                         object_types={'EMPTY', 'ARMATURE', 'MESH', 'OTHER'},
                                         use_mesh_modifiers=False,
                                         add_leaf_bones=False,
                                         bake_anim=False,
                                         apply_scale_options='FBX_SCALE_ALL',
                                         path_mode=path_mode,
                                         embed_textures=True,
                                         use_triangles=False,
                                         mesh_smooth_type='OFF')
            else:
                bpy.ops.export_scene.fbx('INVOKE_DEFAULT',
                                         object_types={'EMPTY', 'ARMATURE', 'MESH', 'OTHER'},
                                         use_mesh_modifiers=False,
                                         add_leaf_bones=False,
                                         bake_anim=False,
                                         apply_scale_options='FBX_SCALE_ALL',
                                         path_mode=path_mode,
                                         embed_textures=True,
                                         use_triangles=False,
                                         mesh_smooth_type='OFF')
        except (TypeError, ValueError):
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT')
        except AttributeError:
            self.report({'ERROR'}, t('ExportModel.error.notEnabled'))

        return {'FINISHED'}


@register_wrap
class ErrorDisplay(bpy.types.Operator):
    bl_idname = "cats_export.display_error"
    bl_label = t('ErrorDisplay.label')
    bl_options = {'INTERNAL'}

    tris_count = 0
    mat_list = []
    mat_count = 0
    meshes_count = 0
    broken_shapes = []
    textures_found = False

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        global _meshes_count, _tris_count, _mat_list, _broken_shapes, _textures_found
        self.meshes_count = _meshes_count
        self.tris_count = _tris_count
        self.mat_list = _mat_list
        self.mat_count = len(_mat_list)
        self.broken_shapes = _broken_shapes
        self.textures_found = _textures_found

        dpi_value = Common.get_user_preferences().system.dpi
        return context.window_manager.invoke_props_dialog(self, width=int(dpi_value * 6))

    def check(self, context):
        # Important for changing options
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        if self.tris_count > max_tris:
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.polygons1'), icon='ERROR')
            col.separator()

            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.polygons2', number=str(self.tris_count)))
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.polygons3'))
            col.separator()
            col.separator()
            col.separator()

        if self.mat_count > max_mats:
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.materials1'), icon='INFO')
            col.separator()

            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.materials2', number=str(self.mat_count)))
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.materials3'))
            col.separator()
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.materials4'))
            col.separator()
            col.separator()
            col.separator()

        if self.meshes_count > max_meshes_light:
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.meshes1'), icon='ERROR')
            col.separator()

            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.meshes2', number=str(self.meshes_count)))
            col.separator()
            row = col.row(align=True)
            row.scale_y = 0.75
            if self.meshes_count <= max_meshes_hard:
                row.label(text=t('ErrorDisplay.meshes3'))
            else:
                row.label(text=t('ErrorDisplay.meshes3_alt'))
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.meshes4'))
            col.separator()
            row = col.row(align=True)
            row.scale_y = 1
            row.operator(armature_manual.JoinMeshes.bl_idname, text=t('ErrorDisplay.JoinMeshes.label'), icon='AUTOMERGE_ON')
            col.separator()
            col.separator()
            col.separator()

        if self.broken_shapes:
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.brokenShapekeys1'), icon='ERROR')
            col.separator()

            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.brokenShapekeys2', number=str(len(self.broken_shapes))))
            col.separator()

            for shapekey in self.broken_shapes:
                row = col.row(align=True)
                row.scale_y = 0.75
                row.label(text="  - " + shapekey)

            col.separator()
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.brokenShapekeys3'))
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.brokenShapekeys4'))
            col.separator()
            col.separator()
            col.separator()

        if not self.textures_found and Settings.get_embed_textures():
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.textures1'), icon='ERROR')
            col.separator()

            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.textures2'))
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.textures3'))
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ErrorDisplay.textures4'))
            col.separator()
            col.separator()
            col.separator()

        row = col.row(align=True)
        row.operator(ExportModel.bl_idname, text=t('ErrorDisplay.continue'), icon=globs.ICON_EXPORT).action = 'NO_CHECK'
