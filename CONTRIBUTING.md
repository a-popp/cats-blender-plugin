# Contributing to Cats Blender Plugin

Thank you for your interest in contributing! This document covers the
basics of setting up a development environment and submitting changes.

## Development Setup

1. **Blender 5.2 LTS** must be installed.
2. Clone this repository.
3. Install the extension from disk in Blender:
   - Edit > Preferences > Extensions > Install from Disk
   - Select the repository folder (containing `blender_manifest.toml`)

## Before Submitting Changes

Run these checks:

```bash
# Compile check
python -m compileall -q .

# Validate manifest
blender --background --factory-startup --command extension validate .

# Run all tests
python tests/run.py -b blender -t "*" -c true -v true
```

All tests must pass. If a test is genuinely not applicable to your
change, document why rather than skipping it silently.

## Coding Conventions

- **Blender 5.2 only.** No version branches for older Blender.
- **No network access.** All features must work offline.
- **Relative imports.** Use `from . import` and `from .. import`.
- **No `sys.path` manipulation.**
- **No `bl_info`.** Metadata is in `blender_manifest.toml`.
- **MIT license.** All files must have the MIT license header.
- Follow existing code style in the repository.

## Adding a New Feature

1. Create operator(s) in `tools/`.
2. Create UI panel(s) in `ui/` if needed.
3. Add scene properties in `extensions.py` if needed.
4. Add the module to `tools/__init__.py` or `ui/__init__.py`.
5. Write a test in `tests/` with generated fixtures.
6. Update the README if user-facing.
7. Run all tests and verify they pass.

## Adding a New Test

1. Create `tests/<name>.test.py`.
2. Generate fixtures programmatically inside the test script.
3. Use explicit assertions — no false positives.
4. Register and unregister the addon in the test.
5. Exit with code 1 on failure, 0 on success.
6. Add the test to the CI workflow if it should run automatically.

## ADRs

Architecture decisions are documented in `docs/adr/`. If your change
introduces a significant architectural shift, create a new ADR
following the existing format.

## Commit Messages

- Focus on "why" not "what".
- Keep the subject line concise.
- Reference issues if applicable.
