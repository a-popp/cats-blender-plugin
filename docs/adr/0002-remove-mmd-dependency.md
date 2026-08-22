# ADR 0002: Remove Bundled MMD Tools

## Status

Accepted

## Context

The original Cats Blender Plugin bundled `mmd_tools_local`, a fork of
the MMD Tools add-on. This was used for MMD model import, morph
support, shader handling, and panel integration.

The bundled MMD code was Blender 2.80-era and failed on Blender 5.2
due to obsolete node-tree interface APIs (`shader.inputs`,
`shader.outputs`) and missing shader outputs. Porting it would require
a significant rewrite of the entire MMD stack.

The MMD dependency also complicated registration, settings, and UI
code with toggle logic for MMD tabs.

## Decision

Remove `extern_tools/mmd_tools_local` entirely and remove all
references to it from:

- `__init__.py` (import, registration, reload, unregistration)
- `tools/common.py` (imports, `toggle_mmd_tabs`)
- `tools/translate.py` (`mmd_translations` import)
- `tools/settings.py` (MMD-related settings)
- `extensions.py` (`show_mmd_tabs`, `use_custom_mmd_tools`)
- UI modules

## Consequences

- MMD model import is no longer supported.
- MMD-specific panels are removed.
- The codebase is simpler and no longer carries unmaintained vendored
  code.
- Translation's `fix_jp_chars` now uses an inline character mapping
  instead of `mmd_tools_local.translations`.
