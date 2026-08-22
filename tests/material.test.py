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

# Material test: generate meshes with materials, test material combine operations.

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

    # Generate a mesh with multiple materials
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    mesh_obj = bpy.context.active_object
    mesh_obj.name = 'TestMesh'

    # Add materials
    mat1 = bpy.data.materials.new('Material1')
    mat1.use_nodes = True
    mesh_obj.data.materials.append(mat1)

    mat2 = bpy.data.materials.new('Material2')
    mat2.use_nodes = True
    mesh_obj.data.materials.append(mat2)

    # Verify materials
    mat_names = [slot.material.name for slot in mesh_obj.material_slots if slot.material]
    print('Materials: {}'.format(mat_names))

    if len(mat_names) != 2:
        errors.append('Expected 2 materials, got {}'.format(len(mat_names)))
    if 'Material1' not in mat_names:
        errors.append('Material1 missing')
    if 'Material2' not in mat_names:
        errors.append('Material2 missing')

    # Verify material combine operator exists
    op_cls = getattr(bpy.types, 'CATS_MATERIAL_OT_combine_mats', None)
    if op_cls is None:
        errors.append('Combine materials operator not found')
    else:
        print('Combine materials operator found')

    # Verify convert to PNG operator exists
    png_cls = getattr(bpy.types, 'CATS_MATERIAL_OT_convert_all_to_png', None)
    if png_cls is None:
        errors.append('Convert to PNG operator not found')
    else:
        print('Convert to PNG operator found')

    # Clean up
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
