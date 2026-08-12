# Changelog

The marketplace renders this file on the extension's Changelog tab, so it is
written for people deciding whether to update — not for the commit log.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
versions follow [semver](https://semver.org). For a theme that means:

- **major** — a change to the palette itself, or anything that makes the theme
  look meaningfully different from what someone chose.
- **minor** — new language or UI coverage, colours where there were none.
- **patch** — a fix to a single wrong or missing colour.

## [Unreleased]

### Added

- Packaging for distribution: extension icon, gallery banner, and the
  repository, homepage and issue links the marketplace listing shows.
- `npm run validate` — checks the manifest and theme for the mistakes that only
  surface after publishing (malformed hex values, unknown `fontStyle`s, a
  contributed path that points at nothing).
- CI on every pull request: validate, confirm the icon matches its generator,
  and package a VSIX.
- A release workflow on `v*` tags: publishes to the Visual Studio Marketplace
  and Open VSX, and attaches the `.vsix` to a GitHub Release.
- Availability on **Open VSX**, so VSCodium, Cursor and Gitpod can install the
  theme rather than only side-load it.

## [1.0.0] - 2026-08-10

### Added

- Initial port of the Ghostty **12-bit Rainbow** terminal theme to VS Code.
- 316 workbench colours covering the editor, sidebar, panels, terminal, git
  decorations, diffs and notifications.
- 36 TextMate token rules and 27 semantic token colours.
- Integrated terminal mapped colour-for-colour to the original ANSI palette.

[unreleased]: https://github.com/rmpato/12-bit-rainbow/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/rmpato/12-bit-rainbow/releases/tag/v1.0.0
