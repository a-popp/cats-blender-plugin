# Cats Blender Plugin

A stripped-down Blender 5.2 extension for VRChat avatar editing and optimization.

This is a modernized fork of the original Cats Blender Plugin, rebuilt as a
Blender Extensions Platform add-on targeting **Blender 5.2 LTS** only.

## Supported Features

- **Model panel**: Export via native FBX, pose mode controls, pose-to-rest.
- **Model Options**: Mesh separation/joining, weight merging, offline
  dictionary translation, bone cleanup, normals, transforms, FBT helpers.
- **Visemes**: Generate viseme shape keys from A, O, and CH shape keys.
- **Decimation**: Smart, safe, half, full, and custom decimation modes.
- **Custom**: Merge armatures and attach meshes.
- **Bake**: Desktop and Quest texture/mesh baking.
- **Optimization**: Bone merging and root-bone tools (no Atlas tab).
- **Shape Key to Basis**: Mesh shape-key context-menu operation.

## Removed / Unsupported Legacy Features

The following features were removed in v1.0.0 and are no longer supported:

- Bundled MMD tools (`mmd_tools_local`)
- Google Translate and all network-dependent translation
- Supporter/news downloads and update checking
- Importer UI and importer implementation
- Copy protection
- Eye tracking
- Atlas / Material Combiner integration
- Fix Model (broken on Blender 5.2, depends on MMD tools)
- `tools/fbx_patch.py` (obsolete GPL exporter monkey-patch)
- Auto-updater

Translation is now **offline dictionary-only** using
`resources/dictionary.json`.

FBX export uses **Blender's native exporter** without monkey-patching.

## Requirements

- **Blender 5.2.0 LTS** (only supported version)
- No internet connection required

## Installation

### Via Blender Extensions Platform

1. Download the extension package (`cats_blender_plugin-1.0.0.zip`).
2. In Blender, go to **Edit > Preferences > Extensions**.
3. Click the dropdown arrow next to "Install" and select
   **Install from Disk**.
4. Select the downloaded `.zip` file.
5. Enable the extension.

### From Source (Development)

1. Clone or download this repository.
2. In Blender, go to **Edit > Preferences > Extensions**.
3. Install from Disk and select the repository folder (containing
   `blender_manifest.toml`).
4. Enable the extension.

## Development

### Repository Layout

```
cats-blender-plugin/
  blender_manifest.toml   # Extension manifest (Blender Extensions Platform)
  __init__.py              # Add-on entry point: register/unregister
  extensions.py            # Scene property definitions
  globs.py                 # Global state and icon constants
  tools/                   # Core operators and business logic
    export.py              # Native FBX export
    translate.py           # Offline dictionary translation
    viseme.py              # Viseme generation
    decimation.py          # Decimation operators
    bonemerge.py           # Bone merging
    rootbone.py            # Root-bone tools
    bake.py                # Bake operators
    material.py            # Material utilities
    armature_manual.py     # Manual armature operations
    armature_custom.py     # Custom armature merging
    armature_bones.py      # Bone name dictionaries
    common.py              # Shared utilities
    settings.py            # Settings persistence
    shapekey.py            # Shape key to basis
    translations.py        # UI translation system
    register.py            # Class registration helpers
  ui/                      # Blender sidebar panels
    main.py                # ToolPanel base class
    armature.py            # Model panel
    manual.py              # Model Options panel
    custom.py              # Custom panel
    decimation.py          # Decimation panel
    visemes.py             # Visemes panel
    optimization.py        # Optimization panel
    bake.py                # Bake panel
  resources/               # Dictionaries, translations, BakeFixer
  tests/                   # Test suite (generated fixtures, no network)
  .github/workflows/       # GitHub Actions CI
```

### Build the Extension Package

```bash
blender --background --factory-startup --command extension build --source-dir . --output-dir build/
```

### Validate the Manifest

```bash
blender --background --factory-startup --command extension validate .
```

### Run Tests

```bash
python tests/run.py -b <path-to-blender> -t "*" -c true -v true
```

Individual tests:

```bash
python tests/run.py -b <path-to-blender> -t "syntax" -c true -v true
python tests/run.py -b <path-to-blender> -t "registration" -c true -v true
python tests/run.py -b <path-to-blender> -t "translate" -c true -v true
python tests/run.py -b <path-to-blender> -t "viseme" -c true -v true
python tests/run.py -b <path-to-blender> -t "bonemerging" -c true -v true
python tests/run.py -b <path-to-blender> -t "boneparenting" -c true -v true
python tests/run.py -b <path-to-blender> -t "material" -c true -v true
python tests/run.py -b <path-to-blender> -t "export" -c true -v true
python tests/run.py -b <path-to-blender> -t "joinmeshes" -c true -v true
python tests/run.py -b <path-to-blender> -t "settings" -c true -v true
python tests/run.py -b <path-to-blender> -t "decimation" -c true -v true
python tests/run.py -b <path-to-blender> -t "bake" -c true -v true
```

Tests use **programmatically generated fixtures** (no external downloads).

### CI

GitHub Actions runs on every push and pull request:

- Python compilation check
- Forbidden import check (no deleted module references)
- Extension manifest validation
- Extension package build
- Full test suite on Blender 5.2

## Architecture

### Registration

The add-on uses a custom `@register_wrap` decorator
(`tools/register.py`) that collects Blender classes and handles
annotation conversion. Classes are ordered by dependency and registered
in `__init__.py`.

Scene properties are defined in `extensions.py` and registered after
the operator/panel classes.

### Translation

Offline dictionary translation loads `resources/dictionary.json` at
startup. The `translate()` function performs substring replacement
using the dictionary. Half-width to full-width Japanese character
conversion is handled by `fix_jp_chars()`.

No network access is required or attempted.

### Export

FBX export uses Blender's native `bpy.ops.export_scene.fbx` operator
without any monkey-patching. Pre-export warnings (triangle count,
material count, mesh count, broken shape keys, missing textures) are
shown via a dialog operator.

### Settings

Settings are persisted to a JSON file. The file location uses
`bpy.utils.extension_path_user()` when available (Blender 4.2+),
falling back to the resources directory for legacy installs.

## License

MIT License. See individual file headers for details.

## Credits

- Original Cats Blender Plugin by GiveMeAllYourCats
- Edits by GiveMeAllYourCats, Hotox, & ZenithVal
