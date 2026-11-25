# AGENTS.md

Guidance for AI agents and contributors working on this repository.

## Project Status

This is a modernized Blender 5.2 extension (v1.0.0) derived from the
original Cats Blender Plugin. The codebase has been stripped of legacy
features and rebuilt around a smaller, maintainable core.

## Key Constraints

- **Blender 5.2 LTS only.** Do not add version branches for older Blender.
- **No network access.** All features must work offline. Do not add
  `requests`, `urllib`, `webbrowser`, or any network-dependent code.
- **No MMD tools.** Do not reintroduce `mmd_tools_local` or any MMD-
  specific functionality.
- **No `bl_info`.** Use `blender_manifest.toml` for metadata.
- **Relative imports.** Use `from . import` and `from .. import` style.
  Do not manipulate `sys.path`.
- **Extension packaging.** The package must validate and build with
  Blender's `extension validate` and `extension build` commands.

## Build & Test Commands

```bash
# Compile check
python -m compileall -q .

# Validate manifest
blender --background --factory-startup --command extension validate .

# Rebuild extension zip (validate + build, writes build/*.zip)
python scripts/build.py

# Build extension package directly
blender --background --factory-startup --command extension build --source-dir . --output-dir build/

# Run all tests
python tests/run.py -b blender -t "*" -c true -v true

# Run specific test
python tests/run.py -b blender -t "registration" -c true -v true
```

## Test Conventions

- Tests are in `tests/*.test.py`.
- Tests use **programmatically generated fixtures** (created in-script
  via `bpy.ops`). No external `.blend` files or downloads.
- Tests must have **explicit assertions** and must not report false
  success.
- The test runner loads the addon via `importlib.util.spec_from_file_location`
  as module `cats`.

## Removed Modules (Do Not Reintroduce)

- `extern_tools/mmd_tools_local`
- `extern_tools/google_trans_new`
- `tools/supporter.py`
- `tools/copy_protection.py`
- `tools/eyetracking.py`
- `tools/credits.py`
- `tools/atlas.py`
- `tools/importer.py`
- `tools/fbx_patch.py`
- `tools/armature.py` (Fix Model)
- `ui/supporter.py`, `ui/copy_protection.py`, `ui/eye_tracking.py`,
  `ui/credits.py`, `ui/bone_root.py`, `ui/settings_updates.py`

## Architecture Notes

- `__init__.py`: Entry point. Registers/unregisters all classes.
- `extensions.py`: Scene property definitions (was `extentions.py`).
- `tools/register.py`: `@register_wrap` decorator and class ordering.
- `tools/translations.py`: UI translation system (CSV-based, offline).
- `tools/translate.py`: Bone/shapekey name translation (dictionary-based,
  offline).
- `tools/export.py`: Native FBX export (extracted from former importer).
- `tools/settings.py`: Settings persistence via
  `bpy.utils.extension_path_user()`.

## Common Pitfalls

- **Circular imports**: `tools/translations.py` must not import
  `tools/settings.py` at module level (causes circular import via
  `translate.py`). Use lazy imports inside functions instead.
- **Operator type names**: Blender registers operators as
  `CATEGORY_OT_name` (category uppercased, name as-is). E.g.
  `cats_manual.start_pose_mode` -> `CATS_MANUAL_OT_start_pose_mode`.
- **Extension writable path**: Do not write to the extension install
  directory. Use `bpy.utils.extension_path_user(__package__, ...)`.
