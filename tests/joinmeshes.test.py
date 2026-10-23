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

# Join meshes test: generate an armature with two parented meshes, then call
# Common.join_meshes() end-to-end and verify a single 'Body' mesh remains.
# This exercises reset_context_scenes(), which previously crashed on removed
# eye-tracking Scene properties (head, eye_left, eye_right, mesh_name_eye).

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

    # --- Fixture setup ---

    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0.5))
    mesh1 = bpy.context.active_object
    mesh1.name = 'MeshA'
    mesh1.parent = armature_obj

    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(1, 0, 0.5))
    mesh2 = bpy.context.active_object
    mesh2.name = 'MeshB'
    mesh2.parent = armature_obj

    bpy.context.scene.armature = armature_obj.name

    # --- reset_context_scenes on a populated scene (regression: used to hit
    # Scene.head / Scene.eye_left / Scene.mesh_name_eye which no longer exist) ---

    try:
        Common.reset_context_scenes()
        print('reset_context_scenes: OK')
    except Exception as e:
        errors.append('reset_context_scenes failed: {}: {}'.format(type(e).__name__, e))
        traceback.print_exc()

    # Verify enum defaults were populated
    if bpy.context.scene.mesh_name_viseme != 'MeshA':
        errors.append('mesh_name_viseme default not set to first mesh, got {!r}'.format(bpy.context.scene.mesh_name_viseme))
    if bpy.context.scene.merge_mesh != 'MeshA':
        errors.append('merge_mesh default not set to first mesh, got {!r}'.format(bpy.context.scene.merge_mesh))

    # --- join_meshes end-to-end ---

    if not errors:
        try:
            joined = Common.join_meshes()
            print('join_meshes returned:', joined)
        except Exception as e:
            errors.append('join_meshes failed: {}: {}'.format(type(e).__name__, e))
            traceback.print_exc()

    if not errors:
        remaining = [o for o in Common.get_meshes_objects(check=False)]
        print('Meshes after join: {}'.format([o.name for o in remaining]))
        if len(remaining) != 1:
            errors.append('Expected exactly 1 mesh after join, got {}'.format(len(remaining)))
        elif remaining[0].name != 'Body':
            errors.append('Joined mesh should be named Body, got {!r}'.format(remaining[0].name))

    # --- Clean up ---

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

except Exception:
    traceback.print_exc()
    errors.append('Join meshes test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('JOIN MESHES TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
