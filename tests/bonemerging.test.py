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

# Bone merging test: generate an armature with bones, then test bone merge setup.

import sys
import traceback

errors = []

try:
    import cats
    cats.register()
except Exception:
    traceback.print_exc()
    errors.append('Registration failed')

try:
    import bpy
    from cats.tools import common as Common
    from cats.tools import rootbone as Rootbone

    # Generate a simple armature with a hierarchy of bones
    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    # Enter edit mode to add bones
    bpy.ops.object.mode_set(mode='EDIT')

    # Clear existing bones
    for bone in armature_obj.data.edit_bones:
        armature_obj.data.edit_bones.remove(bone)

    # Create a simple bone hierarchy: root -> spine -> chest -> head
    root = armature_obj.data.edit_bones.new('root')
    root.head = (0, 0, 0)
    root.tail = (0, 0, 0.5)

    spine = armature_obj.data.edit_bones.new('spine')
    spine.head = (0, 0, 0.5)
    spine.tail = (0, 0, 1.0)
    spine.parent = root

    chest = armature_obj.data.edit_bones.new('chest')
    chest.head = (0, 0, 1.0)
    chest.tail = (0, 0, 1.5)
    chest.parent = spine

    head = armature_obj.data.edit_bones.new('head')
    head.head = (0, 0, 1.5)
    head.tail = (0, 0, 2.0)
    head.parent = chest

    # Add some finger bones to merge
    finger1 = armature_obj.data.edit_bones.new('finger1')
    finger1.head = (0, 0, 2.0)
    finger1.tail = (0, 0.1, 2.1)
    finger1.parent = head

    finger2 = armature_obj.data.edit_bones.new('finger2')
    finger2.head = (0, 0.1, 2.1)
    finger2.tail = (0, 0.2, 2.2)
    finger2.parent = finger1

    bpy.ops.object.mode_set(mode='OBJECT')

    # Verify bones were created
    bone_names = [bone.name for bone in armature_obj.data.bones]
    print('Bones: {}'.format(bone_names))

    expected_bones = ['root', 'spine', 'chest', 'head', 'finger1', 'finger2']
    for bone_name in expected_bones:
        if bone_name not in bone_names:
            errors.append('Missing bone: ' + bone_name)

    # Test root bone detection
    root_bones = Rootbone.get_parent_root_bones(None, None)
    print('Root bones enum items: {}'.format(root_bones))

    # Verify the bone merge operator exists
    op_cls = getattr(bpy.types, 'CATS_BONEMERGE_OT_merge_bones', None)
    if op_cls is None:
        errors.append('Bone merge operator not found')
    else:
        print('Bone merge operator found')

    # Verify refresh root button exists
    refresh_cls = getattr(bpy.types, 'CATS_ROOT_OT_refresh_root_list', None)
    if refresh_cls is None:
        errors.append('Refresh root button operator not found')
    else:
        print('Refresh root button operator found')

    # Clean up
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

except Exception:
    traceback.print_exc()
    errors.append('Bone merging test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('BONE MERGING TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
