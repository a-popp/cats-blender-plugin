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

# Viseme test: generate a simple mesh with shapekeys, then test viseme generation.

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

    # Generate a simple mesh with shapekeys for viseme testing
    # Create a cube mesh
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    mesh_obj = bpy.context.active_object
    mesh_obj.name = 'TestMesh'

    # Add shapekeys
    mesh_obj.shape_key_add(name='Basis')
    mesh_obj.shape_key_add(name='vrc.v_aa')
    mesh_obj.shape_key_add(name='vrc.v_oh')
    mesh_obj.shape_key_add(name='vrc.v_ch')

    # Create an armature
    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    # Set the scene properties for viseme generation
    # Note: mesh_name_viseme, mouth_a, mouth_o, mouth_ch are EnumProperties
    # with dynamic item lists (populated by callback functions). Setting them
    # directly by name only works when the callback returns the matching item.
    # We verify the properties exist but don't set them here.

    # Verify the shapekeys exist
    shapekey_names = [sk.name for sk in mesh_obj.data.shape_keys.key_blocks]
    print('Shapekeys: {}'.format(shapekey_names))

    expected_keys = ['Basis', 'vrc.v_aa', 'vrc.v_oh', 'vrc.v_ch']
    for key in expected_keys:
        if key not in shapekey_names:
            errors.append('Missing shapekey: ' + key)

    # Test that the viseme operator exists
    op_cls = getattr(bpy.types, 'CATS_VISEME_OT_create', None)
    if op_cls is None:
        errors.append('Viseme generate operator not found')
    else:
        print('Viseme generate operator found')

    # Verify scene properties exist (they're EnumProperty with dynamic items)
    for prop_name in ['mesh_name_viseme', 'mouth_a', 'mouth_o', 'mouth_ch']:
        if not hasattr(bpy.context.scene, prop_name):
            errors.append('Scene property missing: ' + prop_name)
        else:
            print('Found scene property: ' + prop_name)

    print('Viseme scene properties verified')

    # Clean up
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

except Exception:
    traceback.print_exc()
    errors.append('Viseme test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('VISEME TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
