# ADR 0005: Use Native FBX Exporter

## Status

Accepted

## Context

The original Cats Blender Plugin included `tools/fbx_patch.py`, which
monkey-patched Blender's FBX exporter to modify export behavior. This
code was GPL-licensed, used obsolete `to_mesh` API behavior, and
patched internal Blender functions that could change between versions.

The export functionality was embedded in `tools/importer.py` (1,116
lines) alongside importer code.

## Decision

- Remove `tools/fbx_patch.py` entirely.
- Extract export functionality from `tools/importer.py` into a new
  `tools/export.py` module.
- Use Blender's native `bpy.ops.export_scene.fbx` operator without
  any monkey-patching.
- Test native export behavior on Blender 5.2.
- Delete `tools/importer.py` after extraction.

## Consequences

- Export uses Blender's unmodified FBX exporter.
- No GPL-licensed monkey-patch code in the codebase.
- Export behavior may differ slightly from the patched version.
- The export module is focused and maintainable.
