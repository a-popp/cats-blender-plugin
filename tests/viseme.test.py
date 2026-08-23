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

# Viseme test: generate a mesh with mouth shapekeys parented to an armature,
# then call the viseme operator end-to-end and verify all 15 VRChat viseme
# shape keys are created. This exercises the full operator path including
# shape key mixing, renaming, sorting, and cleanup.

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

    # Create an armature with a single root bone
    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    # Clear the default bone and add a simple root bone
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature_obj.data.edit_bones:
        armature_obj.data.edit_bones.remove(bone)
    root = armature_obj.data.edit_bones.new('root')
    root.head = (0, 0, 0)
    root.tail = (0, 0, 1)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a mesh with shapekeys for mouth poses
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    mesh_obj = bpy.context.active_object
    mesh_obj.name = 'TestMesh'

    # Add Basis and three mouth shapekeys with actual vertex displacement
    # so that from_mix=True produces meaningful results
    mesh_obj.shape_key_add(name='Basis')
    sk_a = mesh_obj.shape_key_add(name='MouthA')
    sk_a.data[0].co.z += 0.1
    sk_o = mesh_obj.shape_key_add(name='MouthO')
    sk_o.data[0].co.z += 0.2
    sk_ch = mesh_obj.shape_key_add(name='MouthCh')
    sk_ch.data[0].co.z += 0.15

    # Parent mesh to armature so get_meshes_objects(mode=0) finds it.
    # A direct parent assignment is sufficient — we don't need weight
    # painting for the viseme operator to work.
    mesh_obj.parent = armature_obj

    # --- Set scene properties ---

    # Set the armature enum first — get_armature_list callback will
    # return the armature we created.
    bpy.context.scene.armature = armature_obj.name

    # Set mesh_name_viseme — get_meshes callback (mode=0) will find
    # the mesh because it's parented to the armature.
    bpy.context.scene.mesh_name_viseme = mesh_obj.name

    # Set mouth shapekey enums — get_shapekeys_mouth_* callbacks will
    # return all shapekeys from the selected mesh.
    bpy.context.scene.mouth_a = 'MouthA'
    bpy.context.scene.mouth_o = 'MouthO'
    bpy.context.scene.mouth_ch = 'MouthCh'

    # --- Verify fixture ---

    shapekey_names = [sk.name for sk in mesh_obj.data.shape_keys.key_blocks]
    print('Pre-viseme shapekeys: {}'.format(shapekey_names))

    expected_source_keys = ['Basis', 'MouthA', 'MouthO', 'MouthCh']
    for key in expected_source_keys:
        if key not in shapekey_names:
            errors.append('Missing source shapekey: ' + key)

    # Verify the viseme operator exists
    op_cls = getattr(bpy.types, 'CATS_VISEME_OT_create', None)
    if op_cls is None:
        errors.append('Viseme generate operator not found')
    else:
        print('Viseme generate operator found')

    # Verify scene properties exist
    for prop_name in ['mesh_name_viseme', 'mouth_a', 'mouth_o', 'mouth_ch']:
        if not hasattr(bpy.context.scene, prop_name):
            errors.append('Scene property missing: ' + prop_name)
        else:
            print('Found scene property: ' + prop_name)

    # --- Call the viseme operator end-to-end ---

    if not errors:
        print('Calling cats_viseme.create operator...')
        try:
            result = bpy.ops.cats_viseme.create('EXEC_DEFAULT')
            print('Viseme operator returned: {}'.format(result))
        except Exception as e:
            errors.append('Viseme operator failed: {}'.format(e))
            traceback.print_exc()

    # --- Verify viseme shape keys were created ---

    if not errors:
        # The operator may rename the armature to 'Armature' via
        # fix_armature_names(), but the mesh name should be unchanged.
        mesh_after = bpy.context.view_layer.objects.get(mesh_obj.name)
        if mesh_after is None:
            errors.append('Mesh object disappeared after viseme operation')
        else:
            shapekey_names_after = [sk.name for sk in mesh_after.data.shape_keys.key_blocks]
            print('Post-viseme shapekeys: {}'.format(shapekey_names_after))

            expected_visemes = [
                'vrc.v_aa', 'vrc.v_ch', 'vrc.v_dd', 'vrc.v_e', 'vrc.v_ff',
                'vrc.v_ih', 'vrc.v_kk', 'vrc.v_nn', 'vrc.v_oh', 'vrc.v_ou',
                'vrc.v_pp', 'vrc.v_rr', 'vrc.v_sil', 'vrc.v_ss', 'vrc.v_th',
            ]

            missing_visemes = []
            for viseme in expected_visemes:
                if viseme not in shapekey_names_after:
                    missing_visemes.append(viseme)

            if missing_visemes:
                errors.append('Missing viseme shape keys: {}'.format(missing_visemes))
            else:
                print('All {} viseme shape keys created successfully'.format(len(expected_visemes)))

            # Verify the source shapekeys were restored (renamed back from _old)
            for source_key in ['MouthA', 'MouthO', 'MouthCh']:
                if source_key not in shapekey_names_after:
                    errors.append('Source shapekey not restored: ' + source_key)

    # --- Clean up ---

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
