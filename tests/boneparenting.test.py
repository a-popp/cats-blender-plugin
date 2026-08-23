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

# Bone parenting test: generate an armature with a group of similar sibling
# bones, then call the root bone creation operator end-to-end and verify a
# new root bone is created and the siblings are reparented to it.

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

    # Create an armature with a group of similar sibling bones.
    # get_parent_root_bones groups bones by name similarity (>=70% match)
    # and requires >= 2 bones in a group. The function ignores bones whose
    # names contain certain substrings (finger, chest, leg, arm, spine, etc.).
    # We use "Tail_01" and "Tail_02" as children of "Pelvis" — "tail" is not
    # in the ignore list, and the names are similar enough to be grouped.
    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature_obj.data.edit_bones:
        armature_obj.data.edit_bones.remove(bone)

    # Pelvis bone (parent)
    pelvis = armature_obj.data.edit_bones.new('Pelvis')
    pelvis.head = (0, 0, 0)
    pelvis.tail = (0, 0, 0.5)

    # Two similar sibling bones (will be grouped by get_parent_root_bones)
    tail_01 = armature_obj.data.edit_bones.new('Tail_01')
    tail_01.head = (0.1, 0, 0)
    tail_01.tail = (0.1, 0, -0.5)
    tail_01.parent = pelvis

    tail_02 = armature_obj.data.edit_bones.new('Tail_02')
    tail_02.head = (-0.1, 0, 0)
    tail_02.tail = (-0.1, 0, -0.5)
    tail_02.parent = pelvis

    bpy.ops.object.mode_set(mode='OBJECT')

    # Set the armature enum
    bpy.context.scene.armature = armature_obj.name

    # --- Verify fixture ---

    bones = armature_obj.data.bones
    bone_names = [b.name for b in bones]
    print('Bones before root creation: {}'.format(bone_names))

    for bone_name in ['Pelvis', 'Tail_01', 'Tail_02']:
        if bone_name not in bones:
            errors.append('Missing bone: ' + bone_name)

    # Verify parenting
    if bones['Tail_01'].parent != bones['Pelvis']:
        errors.append('Tail_01 parent is not Pelvis')
    if bones['Tail_02'].parent != bones['Pelvis']:
        errors.append('Tail_02 parent is not Pelvis')

    print('Bone hierarchy verified: Pelvis -> Tail_01, Tail_02')

    # --- Detect root bone groups ---

    # Clear cache so get_parent_root_bones re-scans
    globs.root_bones_choices = {}
    globs.root_bones = {}

    root_bones = Rootbone.get_parent_root_bones(None, None)
    print('Root bones enum items: {}'.format(root_bones))

    if not root_bones:
        errors.append('No root bone groups detected - expected Tail_01/Tail_02 to be grouped')
    else:
        # Verify the group contains our bones
        first_group_name = root_bones[0][0]
        if first_group_name not in globs.root_bones:
            errors.append('Root bone group {} not found in globs.root_bones'.format(first_group_name))
        else:
            group_bones = globs.root_bones[first_group_name]
            print('Root bone group {}: {}'.format(first_group_name, group_bones))
            if len(group_bones) < 2:
                errors.append('Root bone group has fewer than 2 bones: {}'.format(group_bones))

    # Verify the root bone creation operator exists
    op_cls = getattr(bpy.types, 'CATS_ROOT_OT_create_root', None)
    if op_cls is None:
        errors.append('Root bone creation operator not found')
    else:
        print('Root bone creation operator found')

    # Verify refresh root button exists
    refresh_cls = getattr(bpy.types, 'CATS_ROOT_OT_refresh_root_list', None)
    if refresh_cls is None:
        errors.append('Refresh root button operator not found')
    else:
        print('Refresh root button operator found')

    # --- Call the root bone creation operator ---

    if not errors and root_bones:
        root_bone_name = root_bones[0][0]
        bpy.context.scene.root_bone = root_bone_name

        print('Calling cats_root.create_root with root_bone={}...'.format(root_bone_name))

        if not op_cls.poll(bpy.context):
            errors.append('Root bone operator poll returned False')
        else:
            bone_count_before = len(armature_obj.data.bones)
            try:
                result = bpy.ops.cats_root.create_root('EXEC_DEFAULT')
                print('Root bone operator returned: {}'.format(result))
            except Exception as e:
                errors.append('Root bone operator failed: {}'.format(e))
                traceback.print_exc()

    # --- Verify root bone creation results ---

    if not errors and root_bones:
        armature_after = bpy.context.view_layer.objects.get(armature_obj.name)
        if armature_after is None:
            errors.append('Armature disappeared after root bone creation')
        else:
            bone_names_after = [b.name for b in armature_after.data.bones]
            print('Bones after root creation: {}'.format(bone_names_after))

            # A new root bone should have been created (name starts with 'Root_')
            new_root_bones = [name for name in bone_names_after if name.startswith('Root_')]
            if not new_root_bones:
                errors.append('No new root bone was created (expected a bone starting with "Root_")')
            else:
                new_root_name = new_root_bones[0]
                print('New root bone created: {}'.format(new_root_name))

                # Verify the new root bone is a child of Pelvis
                new_root_bone = armature_after.data.bones.get(new_root_name)
                if new_root_bone is None:
                    errors.append('New root bone {} not found in armature'.format(new_root_name))
                elif new_root_bone.parent is None:
                    errors.append('New root bone has no parent (expected parent: Pelvis)')
                elif new_root_bone.parent.name != 'Pelvis':
                    errors.append('New root bone parent is {} (expected Pelvis)'.format(new_root_bone.parent.name))
                else:
                    print('New root bone parented to Pelvis: OK')

                # Verify the grouped bones are now children of the new root bone
                group_bones = globs.root_bones.get(root_bone_name, [])
                for bone_name in group_bones:
                    bone = armature_after.data.bones.get(bone_name)
                    if bone is None:
                        errors.append('Bone {} disappeared after root creation'.format(bone_name))
                    elif bone.parent is None:
                        errors.append('Bone {} has no parent after root creation'.format(bone_name))
                    elif bone.parent.name != new_root_name:
                        errors.append('Bone {} parent is {} (expected {})'.format(bone_name, bone.parent.name, new_root_name))
                    else:
                        print('Bone {} reparented to {}: OK'.format(bone_name, new_root_name))

    # --- Clean up ---

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
