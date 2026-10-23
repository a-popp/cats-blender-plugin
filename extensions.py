from .tools import common as Common
from .tools import rootbone as Rootbone
from .tools import settings as Settings
from .tools import translations as Translations
from .tools.translations import t

from bpy.types import Scene
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty

_registered_scene_props = []


def register():
    unregister()
    existing_props = set(Scene.bl_rna.properties.keys())

    Scene.armature = EnumProperty(
        name=t('Scene.armature.label'),
        description=t('Scene.armature.desc'),
        items=Common.get_armature_list
    )

    Scene.keep_upper_chest = BoolProperty(
        name=t('Scene.keep_upper_chest.label'),
        description=t('Scene.keep_upper_chest.desc'),
        default=True
    )

    Scene.keep_end_bones = BoolProperty(
        name=t('Scene.keep_end_bones.label'),
        description=t('Scene.keep_end_bones.desc'),
        default=False
    )

    Scene.remove_rigidbodies_joints = BoolProperty(
        name=t('Scene.remove_rigidbodies_joints.label'),
        description=t('Scene.remove_rigidbodies_joints.desc'),
        default=True
    )

    # Manual
    Scene.keep_merged_bones = BoolProperty(
        name='Keep Merged Bones',
        description='Select this to keep the bones after merging them to their parents or to the active bone',
        default=False
    )

    Scene.merge_visible_meshes_only = BoolProperty(
        name='Merge Visible Meshes Only',
        description='Select this to only merge the weights of the visible meshes',
        default=False
    )

    Scene.show_more_options = BoolProperty(
        name=t('Scene.show_more_options.label'),
        description=t('Scene.show_more_options.desc'),
        default=False
    )

    # Custom Avatar Creation
    Scene.merge_mode = EnumProperty(
        name=t('Scene.merge_mode.label'),
        description=t('Scene.merge_mode.desc'),
        items=[
            ("ARMATURE", t('Scene.merge_mode.armature.label'), t('Scene.merge_mode.armature.desc')),
            ("MESH", t('Scene.merge_mode.mesh.label'), t('Scene.merge_mode.mesh.desc'))
        ]
    )

    Scene.merge_armature_into = EnumProperty(
        name=t('Scene.merge_armature_into.label'),
        description=t('Scene.merge_armature_into.desc'),
        items=Common.get_armature_list
    )

    Scene.merge_armature = EnumProperty(
        name=t('Scene.merge_armature.label'),
        description=t('Scene.merge_armature.desc'),
        items=Common.get_armature_merge_list
    )

    Scene.attach_to_bone = EnumProperty(
        name=t('Scene.attach_to_bone.label'),
        description=t('Scene.attach_to_bone.desc'),
        items=Common.get_bones_merge
    )

    Scene.attach_mesh = EnumProperty(
        name=t('Scene.attach_mesh.label'),
        description=t('Scene.attach_mesh.desc'),
        items=Common.get_top_meshes
    )

    Scene.merge_same_bones = BoolProperty(
        name=t('Scene.merge_same_bones.label'),
        description=t('Scene.merge_same_bones.desc'),
        default=False
    )

    Scene.apply_transforms = BoolProperty(
        name=t('Scene.apply_transforms.label'),
        description=t('Scene.apply_transforms.desc'),
        default=False
    )

    Scene.merge_armatures_join_meshes = BoolProperty(
        name=t('Scene.merge_armatures_join_meshes.label'),
        description=t('Scene.merge_armatures_join_meshes.desc'),
        default=True
    )

    Scene.merge_armatures_remove_zero_weight_bones = BoolProperty(
        name=t('Scene.merge_armatures_remove_zero_weight_bones.label'),
        description=t('Scene.merge_armatures_remove_zero_weight_bones.desc'),
        default=True
    )

    # Decimation
    Scene.decimation_mode = EnumProperty(
        name=t('Scene.decimation_mode.label'),
        description=t('Scene.decimation_mode.desc'),
        items=[
            ("SMART", t('Scene.decimation_mode.smart.label'), t('Scene.decimation_mode.smart.desc')),
            ("SAFE", t('Scene.decimation_mode.safe.label'), t('Scene.decimation_mode.safe.desc')),
            ("HALF", t('Scene.decimation_mode.half.label'), t('Scene.decimation_mode.half.desc')),
            ("FULL", t('Scene.decimation_mode.full.label'), t('Scene.decimation_mode.full.desc')),
            ("CUSTOM", t('Scene.decimation_mode.custom.label'), t('Scene.decimation_mode.custom.desc'))
        ],
        default='SMART'
    )

    Scene.decimation_animation_weighting = BoolProperty(
        name=t('Scene.decimation_animation_weighting.label'),
        description=t('Scene.decimation_animation_weighting.desc'),
        default=False
    )

    Scene.decimation_animation_weighting_factor = FloatProperty(
        name=t('Scene.decimation_animation_weighting_factor.label'),
        description=t('Scene.decimation_animation_weighting_factor.desc'),
        default=0.25,
        min=0,
        max=1,
        step=0.05,
        precision=2,
        subtype='FACTOR'
    )

    Scene.bake_animation_weighting = BoolProperty(
        name=t('Scene.decimation_animation_weighting.label'),
        description=t('Scene.decimation_animation_weighting.desc'),
        default=False
    )

    Scene.bake_animation_weighting_factor = FloatProperty(
        name=t('Scene.decimation_animation_weighting_factor.label'),
        description=t('Scene.decimation_animation_weighting_factor.desc'),
        default=0.25,
        min=0,
        max=1,
        step=0.05,
        precision=2,
        subtype='FACTOR'
    )

    Scene.bake_max_tris = IntProperty(
        name=t('Scene.max_tris.label'),
        description=t('Scene.max_tris.desc'),
        default=7500,
        min=1,
        max=70000
    )

    Scene.bake_remove_doubles = BoolProperty(
        name=t('Scene.decimation_remove_doubles.label'),
        description=t('Scene.decimation_remove_doubles.desc'),
        default=True
    )

    Scene.bake_optimize_static = BoolProperty(
        name="Optimize Static Shapekeys",
        description="Seperate vertices unaffected by shape keys into their own mesh. This adds a drawcall, but comes with a significant GPU cost savings, especially on mobile.",
        default=True
    )

    Scene.bake_cleanup_shapekeys = BoolProperty(
        name="Cleanup Shapekeys",
        description="Remove backup shapekeys in the final result, e.g. 'Key1 - Reverted' or 'blink_old'",
        default=True
    )

    Scene.bake_create_disable_shapekeys = BoolProperty(
        name="Create 'Disable' Shapekeys",
        description="Create 'Disable' shapekeys for all but the largest mesh, that cause it to shrink to nothing. Lets you keep toggleable props, without the need for additional meshes.",
        default=False
    )

    # Bake
    Scene.bake_resolution = IntProperty(
        name=t('Scene.bake_resolution.label'),
        description=t('Scene.bake_resolution.desc'),
        default=2048,
        min=128,
        max=8192
    )

    Scene.bake_use_decimation = BoolProperty(
        name=t('Scene.bake_use_decimation.label'),
        description=t('Scene.bake_use_decimation.desc'),
        default=True
    )

    Scene.bake_generate_uvmap = BoolProperty(
        name=t('Scene.bake_generate_uvmap.label'),
        description=t('Scene.bake_generate_uvmap.desc'),
        default=True
    )

    Scene.bake_uv_overlap_correction = EnumProperty(
        name=t('Scene.bake_uv_overlap_correction.label'),
        description=t('Scene.bake_uv_overlap_correction.desc'),
        items=[
            ("NONE", t("Scene.bake_uv_overlap_correction.none.label"), t("Scene.bake_uv_overlap_correction.none.desc")),
            ("UNMIRROR", t("Scene.bake_uv_overlap_correction.unmirror.label"), t("Scene.bake_uv_overlap_correction.unmirror.desc")),
            ("REPROJECT", t("Scene.bake_uv_overlap_correction.reproject.label"), t("Scene.bake_uv_overlap_correction.reproject.desc")),
            ("MANUAL", "Manual", "Bake will take island information from any UVMap named 'Target' from your meshes, else it will default to the render-active one. Decimation works better when there's only one giant island per loose mesh!")
        ],
        default="UNMIRROR"
    )

    Scene.bake_device = EnumProperty(
        name='Bake Device',
        description='Device to bake on. GPU gives a significant speedup, but can cause issues depending on your graphics drivers.',
        default='GPU',
        items=[
            ('CPU', 'CPU', 'Perform bakes on CPU (Safe)'),
            ('GPU', 'GPU', 'Perform bakes on GPU (Fast)')
        ]
    )

    Scene.bake_prioritize_face = BoolProperty(
        name=t('Scene.bake_prioritize_face.label'),
        description=t('Scene.bake_prioritize_face.desc'),
        default=False
    )

    Scene.bake_face_scale = FloatProperty(
        name=t('Scene.bake_face_scale.label'),
        description=t('Scene.bake_face_scale.desc'),
        default=2.0,
        min=0.5,
        max=4.0,
        step=0.25,
        precision=2,
        subtype='FACTOR'
    )

    Scene.bake_quick_compare = BoolProperty(
        name=t('Scene.bake_quick_compare.label'),
        description=t('Scene.bake_quick_compare.desc'),
        default=True
    )

    Scene.bake_illuminate_eyes = BoolProperty(
        name=t('Scene.bake_illuminate_eyes.label'),
        description=t('Scene.bake_illuminate_eyes.desc'),
        default=True
    )

    Scene.bake_pass_smoothness = BoolProperty(
        name=t('Scene.bake_pass_smoothness.label'),
        description=t('Scene.bake_pass_smoothness.desc'),
        default=True
    )

    Scene.bake_pass_diffuse = BoolProperty(
        name=t('Scene.bake_pass_diffuse.label'),
        description=t('Scene.bake_pass_diffuse.desc'),
        default=True
    )

    Scene.bake_diffuse_vertex_colors = BoolProperty(
        name="Bake to vertex colors",
        description="Rebake to vertex colors after initial bake. Avoids an entire extra texture, if your colors are simple enough. Incorperates AO.",
        default=False
    )

    Scene.bake_preserve_seams = BoolProperty(
        name=t('Scene.bake_preserve_seams.label'),
        description=t('Scene.bake_preserve_seams.desc'),
        default=False
    )

    Scene.bake_pass_normal = BoolProperty(
        name=t('Scene.bake_pass_normal.label'),
        description=t('Scene.bake_pass_normal.desc'),
        default=True
    )

    Scene.bake_normal_apply_trans = BoolProperty(
        name=t('Scene.bake_normal_apply_trans.label'),
        description=t('Scene.bake_normal_apply_trans.desc'),
        default=True
    )

    Scene.bake_apply_keys = BoolProperty(
        name="Apply current shapekey mix",
        description="When selected, currently active shape keys will be applied to the basis. This is extremely beneficial to performance if your avatar is intended to 'default' to one shapekey mix, as having active shapekeys all the time is expensive. Keys ending in '_bake' are always applied to the basis and removed completely, regardless of this option.",
        default=False
    )

    Scene.bake_ignore_hidden = BoolProperty(
        name="Ignore hidden objects",
        description="Ignore currently hidden objects when copying",
        default=True
    )

    Scene.bake_pass_ao = BoolProperty(
        name=t('Scene.bake_pass_ao.label'),
        description=t('Scene.bake_pass_ao.desc'),
        default=False
    )

    Scene.bake_pass_questdiffuse = BoolProperty(
        name=t('Scene.bake_pass_questdiffuse.label'),
        description=t('Scene.bake_pass_questdiffuse.desc'),
        default=True
    )

    Scene.bake_pass_emit = BoolProperty(
        name=t('Scene.bake_pass_emit.label'),
        description=t('Scene.bake_pass_emit.desc'),
        default=False
    )

    Scene.bake_emit_indirect = BoolProperty(
        name="Bake projected light",
        description="Bake the effect of emission on nearby surfaces. Results in much more realistic lighting effects, but can animate less well.",
        default=False
    )

    Scene.bake_emit_exclude_eyes = BoolProperty(
        name="Exclude eyes",
        description="Bakes the effect of any eye glow onto surrounding objects, but not vice-versa. Improves animation when eyes are moving around..",
        default=True
    )

    Scene.bake_diffuse_alpha_pack = EnumProperty(
        name=t('Scene.bake_diffuse_alpha_pack.label'),
        description=t('Scene.bake_diffuse_alpha_pack.desc'),
        items=[
            ("NONE", t("Scene.bake_diffuse_alpha_pack.none.label"), t("Scene.bake_diffuse_alpha_pack.none.desc")),
            ("TRANSPARENCY", t("Scene.bake_diffuse_alpha_pack.transparency.label"), t("Scene.bake_diffuse_alpha_pack.transparency.desc")),
            ("SMOOTHNESS", t("Scene.bake_diffuse_alpha_pack.smoothness.label"), t("Scene.bake_diffuse_alpha_pack.smoothness.desc")),
        ],
        default="NONE"
    )

    Scene.bake_metallic_alpha_pack = EnumProperty(
        name=t('Scene.bake_metallic_alpha_pack.label'),
        description=t('Scene.bake_metallic_alpha_pack.desc'),
        items=[
            ("NONE", t("Scene.bake_metallic_alpha_pack.none.label"), t("Scene.bake_metallic_alpha_pack.none.desc")),
            ("SMOOTHNESS", t("Scene.bake_metallic_alpha_pack.smoothness.label"), t("Scene.bake_metallic_alpha_pack.smoothness.desc"))
        ],
        default="NONE"
    )

    Scene.bake_pass_alpha = BoolProperty(
        name=t('Scene.bake_pass_alpha.label'),
        description=t('Scene.bake_pass_alpha.desc'),
        default=False
    )

    Scene.bake_pass_metallic = BoolProperty(
        name=t('Scene.bake_pass_metallic.label'),
        description=t('Scene.bake_pass_metallic.desc'),
        default=False
    )

    Scene.bake_questdiffuse_opacity = FloatProperty(
        name=t('Scene.bake_questdiffuse_opacity.label'),
        description=t('Scene.bake_questdiffuse_opacity.desc'),
        default=0.75,
        min=0.0,
        max=1.0,
        step=0.05,
        precision=2,
        subtype='FACTOR'
    )

    Scene.selection_mode = EnumProperty(
        name=t('Scene.selection_mode.label'),
        description=t('Scene.selection_mode.desc'),
        items=[
            ("SHAPES", t('Scene.selection_mode.shapekeys.label'), t('Scene.selection_mode.shapekeys.desc')),
            ("MESHES", t('Scene.selection_mode.meshes.label'), t('Scene.selection_mode.meshes.desc'))
        ]
    )

    Scene.add_shape_key = EnumProperty(
        name=t('Scene.add_shape_key.label'),
        description=t('Scene.add_shape_key.desc'),
        items=Common.get_shapekeys_decimation
    )

    Scene.add_mesh = EnumProperty(
        name=t('Scene.add_mesh.label'),
        description=t('Scene.add_mesh.desc'),
        items=Common.get_meshes_decimation
    )

    Scene.decimate_fingers = BoolProperty(
        name=t('Scene.decimate_fingers.label'),
        description=t('Scene.decimate_fingers.desc')
    )

    Scene.decimation_remove_doubles = BoolProperty(
        name=t('Scene.decimation_remove_doubles.label'),
        description=t('Scene.decimation_remove_doubles.desc'),
        default=True
    )

    Scene.max_tris = IntProperty(
        name=t('Scene.max_tris.label'),
        description=t('Scene.max_tris.desc'),
        default=70000,
        min=1,
        max=500000
    )

    # Visemes
    Scene.mesh_name_viseme = EnumProperty(
        name=t('Scene.mesh_name_viseme.label'),
        description=t('Scene.mesh_name_viseme.desc'),
        items=Common.get_meshes
    )

    Scene.mouth_a = EnumProperty(
        name=t('Scene.mouth_a.label'),
        description=t('Scene.mouth_a.desc'),
        items=Common.get_shapekeys_mouth_ah,
    )

    Scene.mouth_o = EnumProperty(
        name=t('Scene.mouth_o.label'),
        description=t('Scene.mouth_o.desc'),
        items=Common.get_shapekeys_mouth_oh,
    )

    Scene.mouth_ch = EnumProperty(
        name=t('Scene.mouth_ch.label'),
        description=t('Scene.mouth_ch.desc'),
        items=Common.get_shapekeys_mouth_ch,
    )

    Scene.shape_intensity = FloatProperty(
        name=t('Scene.shape_intensity.label'),
        description=t('Scene.shape_intensity.desc'),
        default=1.0,
        min=0.0,
        max=10.0,
        step=0.1,
        precision=2,
        subtype='FACTOR'
    )

    # Bone Parenting
    Scene.root_bone = EnumProperty(
        name=t('Scene.root_bone.label'),
        description=t('Scene.root_bone.desc'),
        items=Rootbone.get_parent_root_bones,
    )

    # Optimize
    Scene.optimize_mode = EnumProperty(
        name=t('Scene.optimize_mode.label'),
        description=t('Scene.optimize_mode.desc'),
        items=[
            ("MATERIAL", t('Scene.optimize_mode.material.label'), t('Scene.optimize_mode.material.desc')),
            ("BONEMERGING", t('Scene.optimize_mode.bonemerging.label'), t('Scene.optimize_mode.bonemerging.desc')),
        ]
    )

    # Bone Merging
    Scene.merge_ratio = FloatProperty(
        name=t('Scene.merge_ratio.label'),
        description=t('Scene.merge_ratio.desc'),
        default=50,
        min=1,
        max=100,
        step=1,
        precision=0,
        subtype='PERCENTAGE'
    )

    Scene.merge_mesh = EnumProperty(
        name=t('Scene.merge_mesh.label'),
        description=t('Scene.merge_mesh.desc'),
        items=Common.get_meshes
    )

    Scene.merge_bone = EnumProperty(
        name=t('Scene.merge_bone.label'),
        description=t('Scene.merge_bone.desc'),
        items=Rootbone.get_parent_root_bones,
    )

    # Settings
    Scene.embed_textures = BoolProperty(
        name=t('Scene.embed_textures.label'),
        description=t('Scene.embed_textures.desc'),
        default=False,
        update=Settings.update_settings
    )
    Scene.ui_lang = EnumProperty(
        name=t('Scene.ui_lang.label'),
        description=t('Scene.ui_lang.desc'),
        items=Translations.get_languages_list,
        update=Translations.update_ui
    )
    Scene.debug_translations = BoolProperty(
        name=t('Scene.debug_translations.label'),
        description=t('Scene.debug_translations.desc'),
        default=False
    )

    Scene.pose_to_shapekey_name = StringProperty(name="Pose Name")

    _registered_scene_props[:] = [
        name for name in Scene.bl_rna.properties.keys() if name not in existing_props
    ]


def unregister():
    for name in _registered_scene_props:
        delattr(Scene, name)
    del _registered_scene_props[:]
