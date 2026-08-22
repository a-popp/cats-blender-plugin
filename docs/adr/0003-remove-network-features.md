# ADR 0003: Remove All Network Features

## Status

Accepted

## Context

The original Cats Blender Plugin included several network-dependent
features:

- Google Translate integration via `google_trans_new`
- Supporter list downloads via `urllib.request`
- GitHub commit-based update checking
- Background updater threads
- UI translation downloads from Google Sheets
- External help links via `webbrowser`

These features required internet access, relied on third-party
services that could change or ban users, and violated the Blender
Extensions Platform guidelines discouraging uncontrolled network
access.

## Decision

Remove all network-dependent functionality:

- Remove `extern_tools/google_trans_new`.
- Remove Google Translate calls, cache generation, and
  `dictionary_google.json` handling from `tools/translate.py`.
- Remove `tools/supporter.py` and supporter UI.
- Remove update-check logic and background threads.
- Remove `DownloadTranslations` operator and `urllib` usage from
  `tools/translations.py`.
- Remove `requests` dependency.
- Keep only offline dictionary translation using
  `resources/dictionary.json`.
- Remove network permission declarations from the manifest.

## Consequences

- Translation is limited to the bundled offline dictionary. Names not
  in the dictionary will not be translated.
- No auto-update or update-check functionality.
- No supporter/news panel.
- No UI translation downloads (translators must edit the CSV directly).
- The extension works fully offline and requires no network
  permissions.
