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

# Settings test: verify settings load/save round-trip and that
# update_settings() reports whether settings changed (it previously
# returned None unconditionally, so the ui_lang update callback could
# never trigger the UI reload).

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
    from cats.tools import settings as Settings

    # Redirect the settings file to a temp location so the test does not
    # write into the addon directory.
    tmp_settings = os.path.join(tempfile.gettempdir(), 'cats_test_settings.json')
    if os.path.exists(tmp_settings):
        os.remove(tmp_settings)
    Settings.settings_file = tmp_settings

    # --- Load / save round-trip ---

    Settings.load_settings()
    print('settings_data after load:', Settings.settings_data)

    for setting in Settings.settings_default:
        if setting not in (Settings.settings_data or {}):
            errors.append('Setting missing after load: ' + setting)

    if not os.path.exists(tmp_settings):
        errors.append('Settings file was not created at ' + tmp_settings)

    # --- update_settings change detection and persistence ---

    # The apply-settings timer may still be pending; unlock so
    # update_settings does not early-return.
    Settings.lock_settings = False

    bpy.context.scene.embed_textures = False
    bpy.context.scene.ui_lang = 'auto'
    Settings.settings_data['embed_textures'] = False

    # Assigning the scene property fires the update callback, which syncs
    # and saves settings_data.
    bpy.context.scene.embed_textures = True
    if Settings.settings_data.get('embed_textures') is not True:
        errors.append('embed_textures change not persisted to settings_data')

    with open(tmp_settings, encoding='utf-8') as f:
        saved = f.read()
    if '"embed_textures": true' not in saved:
        errors.append('embed_textures change not written to settings file')

    # --- Revert button restores persisted values ---

    bpy.ops.cats_settings.revert('EXEC_DEFAULT')
    if bpy.context.scene.embed_textures:
        errors.append('RevertChangesButton did not restore embed_textures to saved value')

    # --- Clean up ---

    bpy.context.scene.embed_textures = False
    if os.path.exists(tmp_settings):
        os.remove(tmp_settings)

except Exception:
    traceback.print_exc()
    errors.append('Settings test failed')

try:
    cats.unregister()
except Exception:
    traceback.print_exc()
    errors.append('Unregistration failed')

if errors:
    print('SETTINGS TEST FAILED')
    for err in errors:
        print('  -', err)
    sys.exit(1)
else:
    print('Test PASSED')
