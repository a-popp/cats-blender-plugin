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

# Code author: GiveMeAllYourCats
# Edits by: GiveMeAllYourCats, Hotox, & ZenithVal

dev_branch = False

import sys

from . import globs

# Check if cats is reloading or started fresh
if "bpy" not in locals():
    import bpy
    is_reloading = False
else:
    is_reloading = True

# Load or reload all cats modules
if not is_reloading:
    from . import tools
    from . import ui
    from . import extensions
else:
    import importlib
    importlib.reload(tools)
    importlib.reload(ui)
    importlib.reload(extensions)

from .tools import translations
from .tools.translations import t


def check_unsupported_blender_versions():
    # Don't allow Blender versions older than 5.2
    if bpy.app.version < (5, 2, 0):
        unregister()
        sys.tracebacklimit = 0
        raise ImportError(t('Main.error.unsupportedVersion'))


def set_cats_version_string():
    # Version is now managed by blender_manifest.toml
    version_str = '1.0.0'
    if dev_branch:
        version_str += '-dev'
    return version_str


def register():
    print("\n### Loading CATS...")

    # Check for unsupported Blender versions
    check_unsupported_blender_versions()

    # Set cats version string
    version_str = set_cats_version_string()

    # Set some global settings, first allowed use of globs
    globs.dev_branch = dev_branch
    globs.version_str = version_str

    # Load settings
    try:
        tools.settings.load_settings()
    except OSError as error:
        # Settings are stored in the extension's user directory. If that can't
        # be read or written the add-on can't start; print the reason because
        # the traceback is suppressed below.
        print('Could not load the CATS settings file:', error)
        sys.tracebacklimit = 0
        raise ImportError(t('Main.error.restartAndEnable_alt'))

    # Register all classes
    count = 0
    tools.register.order_classes()
    for cls in tools.register.__bl_classes:
        try:
            bpy.utils.register_class(cls)
            count += 1
        except ValueError:
            pass
    if count < len(tools.register.__bl_classes):
        print('Skipped', len(tools.register.__bl_classes) - count, 'CATS classes.')

    # Register Scene types
    extensions.register()

    # Load the dictionaries and check if they are found.
    globs.dict_found = tools.translate.load_translations()

    # Set preferred Blender options
    tools.common.get_user_preferences().filepaths.use_file_compression = True
    bpy.context.window_manager.addon_support = {'OFFICIAL', 'COMMUNITY'}

    # Add shapekey button to shapekey menu
    bpy.types.MESH_MT_shape_key_context_menu.append(tools.shapekey.addToShapekeyMenu)

    # Apply the settings after a short time, because you can't change checkboxes during register process
    tools.settings.start_apply_settings_timer()

    print("### Loaded CATS successfully!\n")


def unregister():
    print("### Unloading CATS...")

    # Unload all classes in reverse order
    count = 0
    for cls in reversed(tools.register.__bl_ordered_classes):
        try:
            bpy.utils.unregister_class(cls)
            count += 1
        except ValueError:
            pass
        except RuntimeError:
            pass
    print('Unregistered', count, 'CATS classes.')

    # Remove shapekey button from shapekey menu
    try:
        bpy.types.MESH_MT_shape_key_context_menu.remove(tools.shapekey.addToShapekeyMenu)
    except AttributeError:
        print('shapekey button was not registered')
        pass

    # Remove Scene properties
    extensions.unregister()

    print("### Unloaded CATS successfully!\n")


if __name__ == '__main__':
    register()
