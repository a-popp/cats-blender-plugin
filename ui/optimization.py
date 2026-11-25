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
from ..tools import material as Material
from ..tools import bonemerge as Bonemerge
from ..tools import rootbone as Rootbone

from ..tools.register import register_wrap
from ..tools.translations import t


@register_wrap
class OptimizePanel(ToolPanel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_optimize_v3'
    bl_label = t('OptimizePanel.label')
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.prop(context.scene, 'optimize_mode', expand=True)

        if context.scene.optimize_mode == 'MATERIAL':

            col = box.column(align=True)
            row = col.row(align=True)
            row.scale_y = 1.1
            row.operator(Material.CombineMaterialsButton.bl_idname, icon='MATERIAL')

            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.operator(Material.ConvertAllToPngButton.bl_idname, icon='IMAGE_RGB_ALPHA')

        elif context.scene.optimize_mode == 'BONEMERGING':
            if len(Common.get_meshes_objects(check=False)) > 1:
                row = box.row(align=True)
                row.prop(context.scene, 'merge_mesh')
            row = box.row(align=True)
            row.prop(context.scene, 'merge_bone')
            row = box.row(align=True)
            row.prop(context.scene, 'merge_ratio')
            row = box.row(align=True)
            col.separator()
            row.operator(Rootbone.RefreshRootButton.bl_idname, icon='FILE_REFRESH')
            row.operator(Bonemerge.BoneMergeButton.bl_idname, icon='AUTOMERGE_ON')

            col.separator()
            row = box.row(align=True)
            row.prop(context.scene, 'root_bone')
            row = box.row(align=True)
            row.operator(Rootbone.RootButton.bl_idname, icon='BONE_DATA')
