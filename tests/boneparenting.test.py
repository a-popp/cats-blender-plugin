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

# Bone parenting test: generate an armature, test bone parent operations.

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

    # Generate armature with parented bones
    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    bpy.ops.object.mode_set(mode='EDIT')

    # Clear default bone
    for bone in armature_obj.data.edit_bones:
        armature_obj.data.edit_bones.remove(bone)

    # Create bones with parenting
    root = armature_obj.data.edit_bones.new('root')
    root.head = (0, 0, 0)
    root.tail = (0, 0, 1)

    child1 = armature_obj.data.edit_bones.new('child1')
    child1.head = (0, 0, 1)
    child1.tail = (0, 0, 2)
    child1.parent = root

    child2 = armature_obj.data.edit_bones.new('child2')
    child2.head = (0, 0, 2)
    child2.tail = (0, 0, 3)
    child2.parent = child1

    bpy.ops.object.mode_set(mode='OBJECT')

    # Verify bone hierarchy
    bones = armature_obj.data.bones
    if 'root' not in bones:
        errors.append('root bone missing')
    if 'child1' not in bones:
        errors.append('child1 bone missing')
    if 'child2' not in bones:
        errors.append('child2 bone missing')

    # Verify parenting
    if bones['child1'].parent != bones['root']:
        errors.append('child1 parent is not root')
    if bones['child2'].parent != bones['child1']:
        errors.append('child2 parent is not child1')

    print('Bone hierarchy verified: root -> child1 -> child2')

    # Test root bone detection
    root_bones = Rootbone.get_parent_root_bones(None, None)
    print('Root bones: {}'.format(root_bones))

    # Clean up
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

except Exception:
    traceback.print_exc()
    errors.append('Bone parenting test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('BONE PARENTING TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
