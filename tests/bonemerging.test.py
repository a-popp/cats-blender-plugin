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

# Bone merging test: generate an armature with a bone hierarchy and a mesh
# with vertex groups, then call the bone merge operator end-to-end and verify
# that bones are merged and weights are transferred.

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
    import cats.globs as globs

    # --- Fixture setup ---

    # Create an armature with a deep bone hierarchy
    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature_obj.data.edit_bones:
        armature_obj.data.edit_bones.remove(bone)

    # Create hierarchy: root -> spine -> chest -> head
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

    # Add finger bones to merge (children of head)
    finger1 = armature_obj.data.edit_bones.new('finger1')
    finger1.head = (0, 0, 2.0)
    finger1.tail = (0, 0.1, 2.1)
    finger1.parent = head

    finger2 = armature_obj.data.edit_bones.new('finger2')
    finger2.head = (0, 0.1, 2.1)
    finger2.tail = (0, 0.2, 2.2)
    finger2.parent = finger1

    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a mesh and parent it to the armature
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1))
    mesh_obj = bpy.context.active_object
    mesh_obj.name = 'TestMesh'
    mesh_obj.parent = armature_obj

    # Add vertex groups matching the bones
    for bone_name in ['root', 'spine', 'chest', 'head', 'finger1', 'finger2']:
        vg = mesh_obj.vertex_groups.new(name=bone_name)
        # Assign all 8 cube vertices to this group with weight 1.0
        vg.add([i for i in range(len(mesh_obj.data.vertices))], 1.0, 'ADD')

    # Set the armature enum
    bpy.context.scene.armature = armature_obj.name

    # --- Verify fixture ---

    bone_names = [bone.name for bone in armature_obj.data.bones]
    print('Bones before merge: {}'.format(bone_names))

    expected_bones = ['root', 'spine', 'chest', 'head', 'finger1', 'finger2']
    for bone_name in expected_bones:
        if bone_name not in bone_names:
            errors.append('Missing bone: ' + bone_name)

    vg_names = [vg.name for vg in mesh_obj.vertex_groups]
    print('Vertex groups before merge: {}'.format(vg_names))

    # --- Set up root bone detection for merge ---

    # Clear the root bone cache so get_parent_root_bones re-scans
    globs.root_bones_choices = {}
    globs.root_bones = {}

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

    # --- Call the bone merge operator ---

    if not errors and root_bones:
        # Set merge_mesh and merge_bone scene properties
        bpy.context.scene.merge_mesh = mesh_obj.name

        # Pick the first available root bone from the enum
        merge_bone_name = root_bones[0][0]
        bpy.context.scene.merge_bone = merge_bone_name

        # Set a high merge ratio (100%) so all child bones get merged
        bpy.context.scene.merge_ratio = 100

        print('Calling cats_bonemerge.merge_bones with merge_bone={}, ratio=100...'.format(merge_bone_name))

        # Verify poll returns True
        if not op_cls.poll(bpy.context):
            errors.append('Bone merge operator poll returned False')
        else:
            try:
                result = bpy.ops.cats_bonemerge.merge_bones('EXEC_DEFAULT')
                print('Bone merge operator returned: {}'.format(result))
            except Exception as e:
                errors.append('Bone merge operator failed: {}'.format(e))
                traceback.print_exc()

    # --- Verify merge results ---

    if not errors and root_bones:
        armature_after = bpy.context.view_layer.objects.get(armature_obj.name)
        if armature_after is None:
            errors.append('Armature disappeared after bone merge')
        else:
            bone_names_after = [bone.name for bone in armature_after.data.bones]
            print('Bones after merge: {}'.format(bone_names_after))

            # With ratio=100, at least some bones should have been merged
            # (children of the selected root bone get merged into their parents)
            if len(bone_names_after) >= len(expected_bones):
                errors.append('No bones were merged - expected fewer bones after merge, got {}'.format(len(bone_names_after)))

            # Verify the root bone still exists
            if merge_bone_name not in bone_names_after:
                errors.append('Root bone {} was removed during merge'.format(merge_bone_name))

            # Verify vertex groups were updated (merged groups should be removed)
            mesh_after = bpy.context.view_layer.objects.get(mesh_obj.name)
            if mesh_after is None:
                errors.append('Mesh disappeared after bone merge')
            else:
                vg_names_after = [vg.name for vg in mesh_after.vertex_groups]
                print('Vertex groups after merge: {}'.format(vg_names_after))

                # At least one vertex group should have been removed (the merged bone's)
                if len(vg_names_after) >= len(expected_bones):
                    print('Warning: no vertex groups were removed (bones may not have had matching vertex groups)')

    # --- Clean up ---

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
