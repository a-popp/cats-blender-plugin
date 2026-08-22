# ADR 0004: Drop Fix Model for v1.0.0

## Status

Accepted

## Context

The Fix Model feature (`tools/armature.py`) was a core Cats function
that performed automated model cleanup: bone removal, twist bone
fixing, material fixing, rigidbody/joint removal, and mesh joining.

On Blender 5.2, Fix Model was broken because it depended on
`mmd_tools_local` for morph support and shader operations. The MMD
shader code used obsolete node-tree interface APIs that fail on
Blender 5.2.

## Decision

Drop Fix Model for v1.0.0. Remove `tools/armature.py` and all
references to it. The Model panel is reworked around supported
operations (export, pose mode, pose-to-rest).

Individual manual operations from the Model Options panel (bone
cleanup, weight merging, material fixing, etc.) remain available.

## Consequences

- No one-click "Fix Model" button.
- Users must perform individual cleanup operations manually.
- A future version may reintroduce an automated model fix that does
  not depend on MMD tools.
