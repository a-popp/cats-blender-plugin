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

# Bake test: verify the bake preset operators run end-to-end and set the
# expected scene properties. The actual bake requires a saved .blend file
# and Cycles, so only preset autodetection is exercised here.

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

    # --- Fixture setup ---

    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    bpy.ops.mesh.primitive_cube_add(size=0.5)
    mesh = bpy.context.active_object
    mesh.name = 'TestMesh'
    mesh.parent = armature_obj

    mat = bpy.data.materials.new(name='TestMat')
    mat.use_nodes = True
    mesh.data.materials.append(mat)

    bpy.context.scene.armature = armature_obj.name

    if not hasattr(bpy.types, 'CATS_BAKE_OT_preset_desktop'):
        errors.append('Operator cats_bake.preset_desktop not registered')
    if not hasattr(bpy.types, 'CATS_BAKE_OT_preset_quest'):
        errors.append('Operator cats_bake.preset_quest not registered')
    if not hasattr(bpy.types, 'CATS_BAKE_OT_bake'):
        errors.append('Operator cats_bake.bake not registered')

    # --- Desktop preset ---

    result = bpy.ops.cats_bake.preset_desktop('EXEC_DEFAULT')
    print('preset_desktop returned: {}'.format(result))
    scene = bpy.context.scene
    if scene.bake_resolution != 2048:
        errors.append('preset_desktop bake_resolution: expected 2048, got {}'.format(scene.bake_resolution))
    if scene.bake_max_tris != 32000:
        errors.append('preset_desktop bake_max_tris: expected 32000, got {}'.format(scene.bake_max_tris))
    if scene.bake_pass_questdiffuse:
        errors.append('preset_desktop should disable questdiffuse pass')

    # --- Quest preset ---

    result = bpy.ops.cats_bake.preset_quest('EXEC_DEFAULT')
    print('preset_quest returned: {}'.format(result))
    if scene.bake_resolution != 1024:
        errors.append('preset_quest bake_resolution: expected 1024, got {}'.format(scene.bake_resolution))
    if scene.bake_max_tris != 7500:
        errors.append('preset_quest bake_max_tris: expected 7500, got {}'.format(scene.bake_max_tris))
    if not scene.bake_pass_questdiffuse:
        errors.append('preset_quest should enable questdiffuse pass')

    # --- Clean up ---

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.data.materials.remove(mat)

except Exception:
    traceback.print_exc()
    errors.append('Bake test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('BAKE TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
