# ADR 0001: Migrate to Blender Extensions Platform

## Status

Accepted

## Context

The original Cats Blender Plugin was a legacy Blender add-on using
`bl_info` metadata, manual `sys.path` manipulation, and absolute
imports. Blender 4.2+ introduced the Extensions Platform as the
preferred distribution mechanism, and Blender 5.2 continues this
direction.

The legacy packaging approach is incompatible with the Extensions
Platform and discourages practices like `sys.path` modification and
auto-updaters.

## Decision

Migrate to full Blender Extensions Platform packaging:

- Add `blender_manifest.toml` with extension metadata.
- Remove `bl_info` from `__init__.py`.
- Use relative imports throughout.
- Eliminate manual `sys.path` manipulation.
- Use `bpy.utils.extension_path_user()` for writable storage.
- Target Blender 5.2.0 LTS as the minimum and only supported version.

## Consequences

- The add-on can only be installed via the Extensions Platform (or
  installed from disk for development).
- No backward compatibility with Blender < 5.2.
- Settings are stored in the extension user path, not the install
  directory.
- The package can be validated and built with Blender's extension
  command-line tooling.
