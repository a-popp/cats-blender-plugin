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
from .main import layout_split
from ..tools import translate as Translate
from ..tools import settings as Settings
from ..tools import armature_manual as Armature_manual
from ..tools.register import register_wrap
from ..tools.translations import t


@register_wrap
class ManualPanel(ToolPanel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_manual_v3'
    bl_label = t('ManualPanel.label')
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        button_height = 1

        col = box.column(align=True)
        row = layout_split(col, factor=0.32, align=True)
        row.scale_y = button_height
        row.label(text="Separate by:", icon='MESH_DATA')
        row.operator(Armature_manual.SeparateByMaterials.bl_idname, text=t('ManualPanel.SeparateByMaterials.label'))
        row.operator(Armature_manual.SeparateByLooseParts.bl_idname, text=t('ManualPanel.SeparateByLooseParts.label'))
        row.operator(Armature_manual.SeparateByShapekeys.bl_idname, text=t('ManualPanel.SeparateByShapekeys.label'))

        row = layout_split(col, factor=0.4, align=True)
        row.scale_y = button_height
        row.label(text=t('ManualPanel.joinMeshes'), icon='AUTOMERGE_ON')
        row.operator(Armature_manual.JoinMeshes.bl_idname, text=t('ManualPanel.JoinMeshes.label'))
        row.operator(Armature_manual.JoinMeshesSelected.bl_idname, text=t('ManualPanel.JoinMeshesSelected.label'))

        row = layout_split(col, factor=0.4, align=True)
        row.scale_y = button_height
        row.label(text=t('ManualPanel.mergeWeights'), icon='BONE_DATA')
        row.operator(Armature_manual.MergeWeights.bl_idname, text=t('ManualPanel.MergeWeights.label'))
        row.operator(Armature_manual.MergeWeightsToActive.bl_idname, text=t('ManualPanel.MergeWeightsToActive.label'))

        row = col.row(align=True)
        row.scale_y = 0.75
        row.prop(context.scene, 'keep_merged_bones')
        row = col.row(align=True)
        row.scale_y = 0.75
        row.prop(context.scene, 'merge_visible_meshes_only')

        # Translate
        col.separator()
        row = col.row(align=True)
        row.label(text=t('ManualPanel.translate'), icon='FILE_REFRESH')

        split = layout_split(col, factor=0.27, align=True)

        row = split.row(align=True)
        row.scale_y = 2
        row.operator(Translate.TranslateAllButton.bl_idname, text=t('ManualPanel.TranslateAllButton.label'), icon=globs.ICON_ALL)

        row = split.column(align=True)
        row.operator(Translate.TranslateShapekeyButton.bl_idname, text=t('ManualPanel.TranslateShapekeyButton.label'), icon='SHAPEKEY_DATA')
        row.operator(Translate.TranslateObjectsButton.bl_idname, text=t('ManualPanel.TranslateObjectsButton.label'), icon='MESH_DATA')

        row = split.column(align=True)
        row.operator(Translate.TranslateBonesButton.bl_idname, text=t('ManualPanel.TranslateBonesButton.label'), icon='BONE_DATA')
        row.operator(Translate.TranslateMaterialsButton.bl_idname, text=t('ManualPanel.TranslateMaterialsButton.label'), icon='MATERIAL')

        col.separator()
        row = col.row(align=True)
        row.scale_y = 0.85

        if not context.scene.show_more_options:
            row.prop(context.scene, 'show_more_options', icon=globs.ICON_ADD, emboss=True, expand=False, toggle=False, event=False)
        else:
            row.prop(context.scene, 'show_more_options', icon=globs.ICON_REMOVE, emboss=True, expand=False, toggle=False, event=False)

            col.separator()
            row = layout_split(col, factor=0.24, align=True)
            row.scale_y = button_height
            row.label(text=t('ManualPanel.delete'), icon='X')
            row2 = layout_split(row, factor=0.61, align=True)
            row2.operator(Armature_manual.RemoveZeroWeightBones.bl_idname, text=t('ManualPanel.RemoveZeroWeightBones.label'))
            row2.operator(Armature_manual.RemoveConstraints.bl_idname, text=t('ManualPanel.RemoveConstraints'))

            row = layout_split(col, factor=0.24, align=True)
            row.scale_y = button_height
            row.label(text="")
            row.operator(Armature_manual.RemoveZeroWeightGroups.bl_idname, text=t('ManualPanel.RemoveZeroWeightGroups'))

            row = col.row(align=True)
            row.scale_y = 0.75
            row.prop(context.scene, 'keep_upper_chest')
            row = col.row(align=True)
            row.scale_y = 0.75
            row.prop(context.scene, 'keep_end_bones')
            row = col.row(align=True)
            row.scale_y = 0.75
            row.prop(context.scene, 'remove_rigidbodies_joints')

            col.separator()
            row = col.row(align=True)
            row.scale_y = button_height
            row.operator(Armature_manual.DuplicateBonesButton.bl_idname, icon='GROUP_BONE')
            row = col.row(align=True)
            row.scale_y = button_height
            row.operator(Armature_manual.ConnectBonesButton.bl_idname, icon='CONSTRAINT_BONE')

            col.separator()
            row = layout_split(col, factor=0.27, align=True)
            row.scale_y = button_height
            row.label(text=t('ManualPanel.normals'), icon='SNAP_NORMAL')
            row.operator(Armature_manual.RecalculateNormals.bl_idname, text=t('ManualPanel.RecalculateNormals.label'))
            row.operator(Armature_manual.FlipNormals.bl_idname, text=t('ManualPanel.FlipNormals.label'))

            row = col.row(align=True)
            row.scale_y = 1
            subcol = layout_split(row, factor=0, align=True)
            subcol.scale_y = button_height
            subcol.operator(Armature_manual.ApplyTransformations.bl_idname, icon='OUTLINER_DATA_ARMATURE')
            subcol = layout_split(row, factor=0, align=True)
            subcol.scale_y = button_height
            subcol.operator(Armature_manual.ApplyAllTransformations.bl_idname, text="", icon=globs.ICON_ALL)

            row = col.row(align=True)
            row.scale_y = button_height
            row.operator(Armature_manual.RemoveDoubles.bl_idname, icon='X')
            row = col.row(align=True)
            row.scale_y = button_height
            row.operator(Armature_manual.RemoveDoublesNormal.bl_idname, icon='X')

            col.separator()
            row = layout_split(col, factor=0.6, align=True)
            row.scale_y = button_height
            row.label(text=t('ManualPanel.fbtFix'), icon='ARMATURE_DATA')
            row2 = layout_split(row, factor=0.35, align=True)
            row2.operator(Armature_manual.FixFBTButton.bl_idname, text=t('ManualPanel.FixFBTButton.label'))
            row2.operator(Armature_manual.RemoveFBTButton.bl_idname, text=t('ManualPanel.RemoveFBTButton.label'))

            row = col.row(align=True)
            row.scale_y = button_height
            row.operator(Armature_manual.FixVRMShapesButton.bl_idname, icon='SHAPEKEY_DATA')

        # Settings
        col.separator()
        row = col.row(align=True)
        row.label(text=t('ManualPanel.settings'), icon='PREFERENCES')
        row = col.row(align=True)
        row.prop(context.scene, 'embed_textures')
        row = col.row(align=True)
        row.prop(context.scene, 'ui_lang')
        row = col.row(align=True)
        row.prop(context.scene, 'debug_translations')
        row = col.row(align=True)
        row.operator(Settings.RevertChangesButton.bl_idname, icon='FILE_REFRESH')
        row.operator(Settings.DebugTranslations.bl_idname, icon='TOOL_SETTINGS')
