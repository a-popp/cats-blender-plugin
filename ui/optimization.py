import bpy

from .. import globs
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
