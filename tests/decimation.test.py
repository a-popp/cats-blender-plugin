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

# Decimation test: generate an armature with a subdivided grid mesh, then run
# cats_decimation.auto_decimate end-to-end in SMART mode and verify the poly
# count dropped. Also checks the decimation presets.

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

    bpy.ops.mesh.primitive_grid_add(x_subdivisions=10, y_subdivisions=10, size=1)
    mesh = bpy.context.active_object
    mesh.name = 'TestMesh'
    mesh.parent = armature_obj

    bpy.context.scene.armature = armature_obj.name
    polys_before = len(mesh.data.polygons)
    print('Polys before decimation: {}'.format(polys_before))

    if not hasattr(bpy.types, 'CATS_DECIMATION_OT_auto_decimate'):
        errors.append('Operator cats_decimation.auto_decimate not registered')

    # --- Presets ---

    bpy.ops.cats_decimation.preset_quest('EXEC_DEFAULT')
    if bpy.context.scene.max_tris != 5000:
        errors.append('preset_quest did not set max_tris to 5000')
    bpy.ops.cats_decimation.preset_good('EXEC_DEFAULT')
    if bpy.context.scene.max_tris != 70000:
        errors.append('preset_good did not set max_tris to 70000')
    bpy.ops.cats_decimation.preset_excellent('EXEC_DEFAULT')
    if bpy.context.scene.max_tris != 32000:
        errors.append('preset_excellent did not set max_tris to 32000')

    # --- Auto decimate (SMART) ---

    bpy.context.scene.decimation_mode = 'SMART'
    bpy.context.scene.max_tris = 20

    result = bpy.ops.cats_decimation.auto_decimate('EXEC_DEFAULT')
    print('auto_decimate returned: {}'.format(result))
    if result != {'FINISHED'}:
        errors.append('auto_decimate did not finish: {}'.format(result))

    from cats.tools import common as Common
    meshes = Common.get_meshes_objects(check=False)
    if len(meshes) != 1:
        errors.append('Expected 1 armature mesh after join, got {}'.format(len(meshes)))
    else:
        polys_after = len(meshes[0].data.polygons)
        print('Polys after decimation: {}'.format(polys_after))
        if polys_after >= polys_before * 2:
            errors.append('Decimation did not reduce polygon count')
        if meshes[0].name != 'Body':
            errors.append('Joined mesh not renamed to Body: {!r}'.format(meshes[0].name))

    # --- Clean up ---

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

except Exception:
    traceback.print_exc()
    errors.append('Decimation test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('DECIMATION TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
