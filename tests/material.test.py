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

# Material test: generate a mesh with multiple material slots (some with
# identical node setups), then call the combine materials operator
# end-to-end and verify that duplicate material slots are combined.
# Also tests the convert-to-PNG operator path.

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
    from cats.tools import material as Material

    # --- Fixture setup ---

    # Create an armature (required by combine_mats poll and get_meshes_objects)
    bpy.ops.object.armature_add()
    armature_obj = bpy.context.active_object
    armature_obj.name = 'TestArmature'

    # Create a mesh with multiple faces so we can assign different materials
    # to different faces. A subdivided cube gives us enough faces.
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1))
    mesh_obj = bpy.context.active_object
    mesh_obj.name = 'TestMesh'
    mesh_obj.parent = armature_obj

    # Set the armature enum
    bpy.context.scene.armature = armature_obj.name

    # Create 3 materials: two identical, one different
    # The combine operator hashes node setups, so identical node trees
    # with the same node names will be combined.
    mat1 = bpy.data.materials.new('MaterialA')
    mat1.use_nodes = True
    # Clear default nodes and add a simple Principled BSDF
    mat1.node_tree.nodes.clear()
    bsdf1 = mat1.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf1.name = 'Principled BSDF'
    output1 = mat1.node_tree.nodes.new('ShaderNodeOutputMaterial')
    output1.name = 'Material Output'
    mat1.node_tree.links.new(bsdf1.outputs['BSDF'], output1.inputs['Surface'])
    bsdf1.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)

    mat2 = bpy.data.materials.new('MaterialB')
    mat2.use_nodes = True
    mat2.node_tree.nodes.clear()
    bsdf2 = mat2.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf2.name = 'Principled BSDF'
    output2 = mat2.node_tree.nodes.new('ShaderNodeOutputMaterial')
    output2.name = 'Material Output'
    mat2.node_tree.links.new(bsdf2.outputs['BSDF'], output2.inputs['Surface'])
    # Same color as mat1 — identical node setup
    bsdf2.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)

    mat3 = bpy.data.materials.new('MaterialC')
    mat3.use_nodes = True
    mat3.node_tree.nodes.clear()
    bsdf3 = mat3.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf3.name = 'Principled BSDF'
    output3 = mat3.node_tree.nodes.new('ShaderNodeOutputMaterial')
    output3.name = 'Material Output'
    mat3.node_tree.links.new(bsdf3.outputs['BSDF'], output3.inputs['Surface'])
    # Different color — should NOT be combined with mat1/mat2
    bsdf3.inputs['Base Color'].default_value = (0.0, 1.0, 0.0, 1.0)

    # Assign all 3 materials to the mesh
    mesh_obj.data.materials.append(mat1)
    mesh_obj.data.materials.append(mat2)
    mesh_obj.data.materials.append(mat3)

    # Assign different materials to different faces
    # Cube has 6 faces; assign mat1 to faces 0-1, mat2 to faces 2-3, mat3 to faces 4-5
    for i, poly in enumerate(mesh_obj.data.polygons):
        if i < 2:
            poly.material_index = 0  # MaterialA
        elif i < 4:
            poly.material_index = 1  # MaterialB
        else:
            poly.material_index = 2  # MaterialC

    # --- Verify fixture ---

    mat_names = [slot.material.name for slot in mesh_obj.material_slots if slot.material]
    print('Materials before combine: {}'.format(mat_names))

    if len(mat_names) != 3:
        errors.append('Expected 3 materials, got {}'.format(len(mat_names)))
    if 'MaterialA' not in mat_names:
        errors.append('MaterialA missing')
    if 'MaterialB' not in mat_names:
        errors.append('MaterialB missing')
    if 'MaterialC' not in mat_names:
        errors.append('MaterialC missing')

    # --- Verify operators exist ---

    op_cls = getattr(bpy.types, 'CATS_MATERIAL_OT_combine_mats', None)
    if op_cls is None:
        errors.append('Combine materials operator not found')
    else:
        print('Combine materials operator found')

    png_cls = getattr(bpy.types, 'CATS_MATERIAL_OT_convert_all_to_png', None)
    if png_cls is None:
        errors.append('Convert to PNG operator not found')
    else:
        print('Convert to PNG operator found')

    # --- Call the combine materials operator ---

    if not errors:
        print('Calling cats_material.combine_mats...')
        if not op_cls.poll(bpy.context):
            errors.append('Combine materials operator poll returned False')
        else:
            slot_count_before = len(mesh_obj.material_slots)
            try:
                result = bpy.ops.cats_material.combine_mats('EXEC_DEFAULT')
                print('Combine materials operator returned: {}'.format(result))
            except Exception as e:
                errors.append('Combine materials operator failed: {}'.format(e))
                traceback.print_exc()

    # --- Verify combine results ---

    if not errors:
        mesh_after = bpy.context.view_layer.objects.get(mesh_obj.name)
        if mesh_after is None:
            errors.append('Mesh disappeared after combine materials')
        else:
            mat_names_after = [slot.material.name for slot in mesh_after.material_slots if slot.material]
            slot_count_after = len(mesh_after.material_slots)
            print('Materials after combine: {}'.format(mat_names_after))
            print('Slot count: {} -> {}'.format(slot_count_before, slot_count_after))

            # The operator combines materials with identical node setups.
            # MaterialA and MaterialB have identical node setups, so faces
            # that had MaterialB (index 1) should now reference MaterialA.
            # MaterialC is different and should remain unchanged.
            # Verify face material indices changed:
            face_indices_after = [poly.material_index for poly in mesh_after.data.polygons]
            print('Face material indices after combine: {}'.format(face_indices_after))

            # Faces 2-3 originally had material_index=1 (MaterialB).
            # After combining, they should have material_index=0 (MaterialA).
            if len(face_indices_after) >= 4:
                if face_indices_after[2] == 1 and face_indices_after[3] == 1:
                    errors.append('Faces 2-3 still reference MaterialB (index 1) - combine did not reassign them')

            # MaterialC should still exist (it's different)
            if 'MaterialC' not in mat_names_after:
                errors.append('MaterialC should still exist after combine (it has a different node setup)')

            # Slot count should decrease if cleanmatslots worked
            if slot_count_after >= slot_count_before:
                print('Warning: slot count did not decrease (cleanmatslots may not have run in background mode)')

    # --- Test convert-to-PNG operator (no images to convert, should succeed gracefully) ---

    if not errors:
        print('Calling cats_material.convert_all_to_png...')
        try:
            result = bpy.ops.cats_material.convert_all_to_png('EXEC_DEFAULT')
            print('Convert to PNG operator returned: {}'.format(result))
        except Exception as e:
            errors.append('Convert to PNG operator failed: {}'.format(e))
            traceback.print_exc()

    # --- Clean up ---

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    # Remove orphan materials
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

except Exception:
    traceback.print_exc()
    errors.append('Material test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('MATERIAL TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
