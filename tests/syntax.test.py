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

# Syntax test: compile all Python files in the addon and verify no imports
# or bpy.ops calls reference deleted modules.

import os
import py_compile
import re
import sys

addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

errors = []
compiled = 0

# Collect all .py files in the addon
py_files = []
for root, dirs, files in os.walk(addon_dir):
    # Skip tests directory, build artifacts, .git
    if '.git' in root or 'build' in root or os.sep + 'tests' in root:
        continue
    for f in files:
        if f.endswith('.py'):
            py_files.append(os.path.join(root, f))

for py_file in py_files:
    try:
        py_compile.compile(py_file, doraise=True)
        compiled += 1
    except py_compile.PyCompileError as e:
        errors.append(str(e))

# Check for references to deleted modules
deleted_modules = [
    'mmd_tools_local',
    'google_trans_new',
    'extern_tools',
    'tools.supporter',
    'tools.copy_protection',
    'tools.eyetracking',
    'tools.credits',
    'tools.atlas',
    'tools.importer',
    'tools.fbx_patch',
    'tools.armature',
    'ui.supporter',
    'ui.copy_protection',
    'ui.eye_tracking',
    'ui.credits',
    'ui.bone_root',
    'ui.settings_updates',
]

# Removed operator categories (from deleted modules). These bpy.ops
# categories no longer exist and any call to them will fail at runtime.
removed_operator_categories = [
    'cats_importer',
    'cats_supporter',
    'cats_eyetracking',
    'cats_credits',
    'cats_atlas',
    'cats_copy_protection',
]

for py_file in py_files:
    with open(py_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    for mod in deleted_modules:
        # (?!\w) so 'tools.armature' doesn't match 'tools.armature_custom'
        pattern = r'(import|from)\s+' + re.escape(mod) + r'(?!\w)'
        if re.search(pattern, content):
            # Allow comments
            for line in content.split('\n'):
                if re.search(pattern, line) and not line.strip().startswith('#'):
                    errors.append('Forbidden import in {}: {}'.format(py_file, line.strip()))
    for cat in removed_operator_categories:
        if 'bpy.ops.' + cat in content:
            for line in content.split('\n'):
                if 'bpy.ops.' + cat in line and not line.strip().startswith('#'):
                    errors.append('Reference to removed operator category in {}: {}'.format(py_file, line.strip()))

if errors:
    print('SYNTAX TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Ran syntax test')
    print('Compiled {} files successfully'.format(compiled))
    print('Test PASSED')
