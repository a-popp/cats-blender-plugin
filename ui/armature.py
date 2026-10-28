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

from .. import globs
from .main import ToolPanel
from ..tools import common as Common
from ..tools import export as Export
from ..tools import armature_manual as Armature_manual
from ..tools.register import register_wrap
from ..tools.translations import t


@register_wrap
class ArmaturePanel(ToolPanel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_armature_v3'
    bl_label = t('ArmaturePanel.label')

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        col = box.column(align=True)

        if not globs.dict_found:
            col.separator()
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ArmaturePanel.warn.noDict1'), icon='INFO')
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ArmaturePanel.warn.noDict2'), icon='BLANK1')
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text=t('ArmaturePanel.warn.noDict3'), icon='BLANK1')
            col.separator()
            col.separator()

        arm_count = len(Common.get_armature_objects())
        if arm_count == 0:
            split = col.row(align=True)
            row = split.row(align=True)
            row.scale_y = 1.7
            row.label(text=t('ArmaturePanel.noModel'), icon='INFO')
            return
        else:
            split = col.row(align=True)
            row = split.row(align=True)
            row.scale_y = 1.4
            row.operator(Export.ExportModel.bl_idname, icon='ARMATURE_DATA').action = 'CHECK'

        if arm_count > 1:
            col.separator()
            col.separator()
            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(context.scene, 'armature', icon='ARMATURE_DATA')

        col.separator()
        col.separator()

        armature_obj = Common.get_armature()
        if not armature_obj or armature_obj.mode != 'POSE':
            split = col.row(align=True)
            row = split.row(align=True)
            row.scale_y = 1.1
            row.operator(Armature_manual.StartPoseMode.bl_idname, icon='POSE_HLT')
            row = split.row(align=True)
            row.alignment = 'RIGHT'
            row.scale_y = 1.1
            row.operator(Armature_manual.StartPoseModeNoReset.bl_idname, text="", icon='POSE_HLT')
        else:
            split = col.row(align=True)
            row = split.row(align=True)
            row.scale_y = 1.1
            row.operator(Armature_manual.StopPoseMode.bl_idname, icon=globs.ICON_POSE_MODE)
            row = split.row(align=True)
            row.alignment = 'RIGHT'
            row.scale_y = 1.1
            row.operator(Armature_manual.StopPoseModeNoReset.bl_idname, text='', icon=globs.ICON_POSE_MODE)
            row = col.row(align=True)
            row.scale_y = 0.9
            row.operator(Armature_manual.PoseToShape.bl_idname, icon='SHAPEKEY_DATA')
            row = col.row(align=True)
            row.scale_y = 0.9
            row.operator(Armature_manual.PoseToRest.bl_idname, icon='POSE_HLT')
