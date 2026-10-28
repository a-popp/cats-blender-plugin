# MIT License
#
# Copyright (c) 2017 GiveMeAllYourCats
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy

from .main import ToolPanel
from ..tools import common as Common
from ..tools import viseme as Viseme

from ..tools.register import register_wrap
from ..tools.translations import t


@register_wrap
class VisemePanel(ToolPanel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_viseme_v3'
    bl_label = t('VisemePanel.label')
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        mesh_count = len(Common.get_meshes_objects(check=False))
        if mesh_count == 0:
            row = col.row(align=True)
            row.scale_y = 1.1
            row.label(text=t('VisemePanel.error.noMesh'), icon='ERROR')
            col.separator()
        elif mesh_count > 1:
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(context.scene, 'mesh_name_viseme', icon='MESH_DATA')
            col.separator()

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(context.scene, 'mouth_a', icon='SHAPEKEY_DATA')
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(context.scene, 'mouth_o', icon='SHAPEKEY_DATA')
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(context.scene, 'mouth_ch', icon='SHAPEKEY_DATA')

        col.separator()
        row = col.row(align=True)
        row.prop(context.scene, 'shape_intensity')

        col.separator()
        row = col.row(align=True)
        row.operator(Viseme.AutoVisemeButton.bl_idname, icon='TRIA_RIGHT')
