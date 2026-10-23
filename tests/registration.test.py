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

# Registration test: verify the addon can register and unregister cleanly
# on Blender 5.2, and that key operators and panels are present.

import sys
import traceback

errors = []

try:
    import cats
    cats.register()
    print('Registration succeeded')
except Exception:
    traceback.print_exc()
    errors.append('Registration failed')

# Verify key panels are registered
import bpy

expected_panels = [
    'VIEW3D_PT_armature_v3',
    'VIEW3D_PT_manual_v3',
    'VIEW3D_PT_custom_v3',
    'VIEW3D_PT_decimation_v3',
    'VIEW3D_PT_viseme_v3',
    'VIEW3D_PT_optimize_v3',
    'VIEW3D_PT_catsbake',
]

for panel_id in expected_panels:
    cls = getattr(bpy.types, panel_id, None)
    if cls is None:
        errors.append('Panel not registered: ' + panel_id)
    else:
        print('Found panel: ' + panel_id)

# Verify key operators are registered
expected_operators = [
    'cats_export.export_model',
    'cats_export.display_error',
    'cats_manual.start_pose_mode',
    'cats_manual.stop_pose_mode',
    'cats_manual.pose_to_rest',
    'cats_manual.pose_to_shape',
    'cats_translate.shapekeys',
    'cats_translate.objects',
    'cats_translate.all',
    'cats_viseme.create',
    'cats_bonemerge.merge_bones',
]

for op_id in expected_operators:
    # Blender convention: category.name -> CATEGORY_OT_name
    parts = op_id.split('.')
    type_name = parts[0].upper() + '_OT_' + parts[1]
    cls = getattr(bpy.types, type_name, None)
    if cls is None:
        errors.append('Operator not registered: ' + op_id + ' (expected type: ' + type_name + ')')
    else:
        print('Found operator: ' + op_id)

# Verify scene properties exist
expected_props = [
    'armature',
    'decimation_mode',
    'mesh_name_viseme',
    'mouth_a',
    'mouth_o',
    'mouth_ch',
    'merge_ratio',
    'merge_mesh',
    'merge_bone',
    'optimize_mode',
    'embed_textures',
    'ui_lang',
]

for prop in expected_props:
    if not hasattr(bpy.context.scene, prop):
        errors.append('Scene property missing: ' + prop)
    else:
        print('Found scene property: ' + prop)

# Verify removed properties are NOT present
removed_props = [
    'eye_mode',
    'mesh_name_eye',
    'eye_left',
    'eye_right',
    'show_mmd_tabs',
    'use_custom_mmd_tools',
    'use_google_only',
]

for prop in removed_props:
    if hasattr(bpy.context.scene, prop):
        errors.append('Removed scene property still present: ' + prop)

# Verify operator labels are translated (not raw CSV keys). A circular
# import at module init previously left these as untranslated keys.
expected_labels = {
    'CATS_TRANSLATE_OT_shapekeys': 'Translate Shape Keys',
    'CATS_TRANSLATE_OT_bones': 'Translate Bones',
    'CATS_SETTINGS_OT_revert': 'Revert Settings',
}
for type_name, label in expected_labels.items():
    cls = getattr(bpy.types, type_name, None)
    if cls is None:
        errors.append('Operator not registered for label check: ' + type_name)
    elif cls.bl_label != label:
        errors.append('Operator {} has untranslated bl_label: {!r}'.format(type_name, cls.bl_label))

# Now unregister and verify clean unregistration
try:
    cats.unregister()
    print('Unregistration succeeded')
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

# Verify panels are gone after unregister
for panel_id in expected_panels:
    cls = getattr(bpy.types, panel_id, None)
    if cls is not None:
        errors.append('Panel still registered after unregister: ' + panel_id)

# Verify scene properties are removed after unregister
for prop in expected_props + ['pose_to_shapekey_name']:
    if hasattr(bpy.context.scene, prop):
        errors.append('Scene property leaked after unregister: ' + prop)

if errors:
    print('REGISTRATION TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
