# ADR 0006: Use Generated Test Fixtures

## Status

Accepted

## Context

The original test suite depended on `.blend` fixture files stored in
`tests/armatures/`. Some of these were downloaded from legacy Dropbox
links, making the full suite non-reproducible without network access.
The fixtures were also tied to legacy model formats and MMD-specific
features.

## Decision

Replace external fixture files with **programmatically generated
fixtures**:

- Each test script creates its own armature/mesh/material fixtures
  using `bpy.ops` calls.
- No external downloads or `.blend` files are required.
- The test runner (`tests/run.py`) no longer downloads fixtures.
- Tests are deterministic and run fully offline.

## Consequences

- Tests are self-contained and reproducible.
- No network access required for testing.
- Tests can run in CI without fixture management.
- Fixture complexity is limited to what can be generated
  programmatically (sufficient for operator/registration/smoke tests).
