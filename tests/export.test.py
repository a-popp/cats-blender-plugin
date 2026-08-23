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

# Export test: generate a simple armature+mesh, export via native FBX,
# verify the file is created. Tests Blender 5.2 native FBX exporter
# without the removed fbx_patch monkey-patching. Also exercises the
# CATS export operator (cats_export.export_model) end-to-end with
# action='NO_CHECK' to verify the operator path works without
# referencing removed modules.

import sys
import os
import tempfile
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
    from cats.tools import export as Export

    # Generate a simple armature with a mesh
    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    # Add a cube mesh
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 1))
    mesh_obj = bpy.context.active_object
    mesh_obj.name = 'TestMesh'

    # Parent mesh to armature with automatic weights
    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    armature_obj.select_set(True)
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    # Verify export operator exists
    op_cls = getattr(bpy.types, 'CATS_EXPORT_OT_export_model', None)
    if op_cls is None:
        errors.append('Export model operator not found')
    else:
        print('Export model operator found')

    # Verify error display operator exists
    err_cls = getattr(bpy.types, 'CATS_EXPORT_OT_display_error', None)
    if err_cls is None:
        errors.append('Error display operator not found')
    else:
        print('Error display operator found')

    # Test native FBX export (without the removed fbx_patch)
    fbx_path = os.path.join(tempfile.gettempdir(), 'cats_test_export.fbx')
    if os.path.exists(fbx_path):
        os.remove(fbx_path)

    try:
        bpy.ops.export_scene.fbx(
            filepath=fbx_path,
            object_types={'EMPTY', 'ARMATURE', 'MESH', 'OTHER'},
            use_mesh_modifiers=False,
            add_leaf_bones=False,
            bake_anim=False,
            apply_scale_options='FBX_SCALE_ALL',
            path_mode='AUTO',
            embed_textures=True,
            use_triangles=False,
            mesh_smooth_type='OFF'
        )
        print('FBX export operator completed')
    except Exception as e:
        errors.append('FBX export failed: {}'.format(e))
        traceback.print_exc()

    # Verify the FBX file was created
    if not os.path.exists(fbx_path):
        errors.append('FBX file was not created at: ' + fbx_path)
    else:
        file_size = os.path.getsize(fbx_path)
        print('FBX file created: {} ({} bytes)'.format(fbx_path, file_size))
        if file_size < 100:
            errors.append('FBX file is suspiciously small: {} bytes'.format(file_size))
        # Clean up
        os.remove(fbx_path)

    # Test the CATS export operator end-to-end (action='NO_CHECK' skips
    # the warning dialog path, which requires a GUI and cannot run in
    # background mode). This verifies the operator calls the native FBX
    # exporter without referencing removed modules like cats_importer.
    cats_fbx_path = os.path.join(tempfile.gettempdir(), 'cats_test_export_operator.fbx')
    if os.path.exists(cats_fbx_path):
        os.remove(cats_fbx_path)

    try:
        result = bpy.ops.cats_export.export_model(
            'EXEC_DEFAULT',
            action='NO_CHECK',
            filepath=cats_fbx_path
        )
        print('CATS export operator completed: {}'.format(result))
    except Exception as e:
        errors.append('CATS export operator failed: {}'.format(e))
        traceback.print_exc()

    if not os.path.exists(cats_fbx_path):
        errors.append('CATS export operator did not create FBX file at: ' + cats_fbx_path)
    else:
        file_size = os.path.getsize(cats_fbx_path)
        print('CATS export FBX file created: {} ({} bytes)'.format(cats_fbx_path, file_size))
        if file_size < 100:
            errors.append('CATS export FBX file is suspiciously small: {} bytes'.format(file_size))
        os.remove(cats_fbx_path)

    # Clean up scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

except Exception:
    traceback.print_exc()
    errors.append('Export test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('EXPORT TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
