# 12-bit Rainbow for VS Code

[![Marketplace](https://img.shields.io/visual-studio-marketplace/v/pato.twelve-bit-rainbow?label=marketplace)](https://marketplace.visualstudio.com/items?itemName=pato.twelve-bit-rainbow)
[![Open VSX](https://img.shields.io/open-vsx/v/pato/twelve-bit-rainbow?label=open%20vsx)](https://open-vsx.org/extension/pato/twelve-bit-rainbow)
[![CI](https://github.com/rmpato/12-bit-rainbow/actions/workflows/ci.yml/badge.svg)](https://github.com/rmpato/12-bit-rainbow/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A dark theme for VS Code, ported straight from the [Ghostty](https://ghostty.org) terminal theme
of the same name. Near-black background, saturated accents, and a palette that stays consistent
between your editor and your terminal.

If you already use **12-bit Rainbow** in Ghostty, this makes VS Code match it — including the
integrated terminal, which is mapped color-for-color to the original ANSI palette.

---

## Install

**In your editor.** `Cmd+Shift+X` (`Ctrl+Shift+X`), search **12-bit Rainbow**, click Install.

**From the command line.**

```sh
code --install-extension pato.twelve-bit-rainbow
```

Cursor, VSCodium and Gitpod install from [Open VSX](https://open-vsx.org/extension/pato/twelve-bit-rainbow)
rather than Microsoft's marketplace. The theme is published to both, so the same search works there.

**Then turn it on.** Press `Cmd+K` then `Cmd+T` (`Ctrl+K Ctrl+T` on Windows/Linux) and pick
**12-bit Rainbow** from the list.

<details>
<summary>Installing without a marketplace</summary>

Download the `.vsix` from the [latest release](https://github.com/rmpato/12-bit-rainbow/releases/latest):

```sh
code --install-extension 12-bit-rainbow.vsix
```

Or copy the repository into your editor's extensions directory:

```sh
git clone https://github.com/rmpato/12-bit-rainbow.git
cp -R 12-bit-rainbow ~/.vscode/extensions/12-bit-rainbow
```

| Editor | Extensions directory |
|---|---|
| VS Code | `~/.vscode/extensions/` |
| VS Code Insiders | `~/.vscode-insiders/extensions/` |
| Cursor | `~/.cursor/extensions/` |
| VSCodium | `~/.vscode-oss/extensions/` |

On Windows the path is `%USERPROFILE%\.vscode\extensions\`. Restart the editor afterwards — a full
quit-and-reopen is most reliable; `Cmd+Shift+P` → *Developer: Reload Window* usually works too.

</details>

If the theme isn't in the list, see [Troubleshooting](#troubleshooting).

---

## What you get

- **Editor and UI** — sidebar, tabs, status bar, menus, notifications, diffs, and peek views are
  all themed, not just the code.
- **Integrated terminal** — all 16 ANSI colors match Ghostty exactly, so terminal output looks
  identical in both apps.
- **Semantic highlighting** — enabled, so languages with a language server (TypeScript, Rust, Go,
  Python, …) get more precise colors than regex-based highlighting alone.
- **Rainbow brackets** — nested bracket pairs cycle through six palette hues.
- **Git and diff colors** — added/modified/deleted states in the gutter, file tree, and minimap.

### The palette

Every color below comes from the original Ghostty theme file. Nothing was invented.

| Role | Color | | Role | Color | |
|---|---|---|---|---|---|
| background | `#040404` | ⬛ | foreground | `#feffff` | ⬜ |
| black | `#000000` | ⬛ | bright black | `#685656` | 🟫 |
| red | `#a03050` | 🟥 | bright red | `#c06060` | 🟥 |
| green | `#40d080` | 🟩 | bright green | `#90d050` | 🟩 |
| yellow | `#e09040` | 🟧 | bright yellow | `#e0d000` | 🟨 |
| blue | `#3060b0` | 🟦 | bright blue | `#00b0c0` | 🟦 |
| magenta | `#603090` | 🟪 | bright magenta | `#801070` | 🟪 |
| cyan | `#0090c0` | 🟦 | bright cyan | `#20b0c0` | 🟦 |
| white | `#dbded8` | ⬜ | bright white | `#ffffff` | ⬜ |
| cursor | `#e0d000` | 🟨 | selection | `#606060` | ⬛ |

The one addition: three near-black shades derived from the background (`#0a0908`, `#131110`,
`#1d1919`) separate the sidebar, inputs, and borders from the editor. A single flat `#040404`
everywhere leaves the UI with no visible edges.

### How code gets colored

| Token | Color |
|---|---|
| comments | bright black, *italic* |
| strings | green — escapes and regex in bright green |
| numbers, constants, parameters | orange (`#e09040`) |
| functions, methods, CAPS constants | bright yellow |
| keywords, HTML tags | bright red |
| types, classes, operators | bright cyan |
| properties, object keys, JSON/YAML keys | blue (`#00b0c0`) |
| decorators, `this` / `self` | magenta |

---

## Making it yours

You don't need to fork the theme to adjust it. Add overrides to your own VS Code `settings.json`
(`Cmd+Shift+P` → *Preferences: Open User Settings (JSON)*):

```jsonc
{
  // Change any UI color
  "workbench.colorCustomizations": {
    "[12-bit Rainbow]": {
      "editor.background": "#000000",
      "editorCursor.foreground": "#40d080"
    }
  },

  // Change any syntax color
  "editor.tokenColorCustomizations": {
    "[12-bit Rainbow]": {
      "comments": "#7a6868",
      "textMateRules": [
        {
          "scope": "keyword.control",
          "settings": { "foreground": "#a03050", "fontStyle": "bold" }
        }
      ]
    }
  }
}
```

To find the scope name of whatever your cursor is on, run *Developer: Inspect Editor Tokens and
Scopes* from the command palette.

**Don't like the italics?** Set `"fontStyle": ""` for the `comment` scope using the block above.

---

## Troubleshooting

**The theme doesn't appear in the picker.** Confirm the files landed in the right place — you
should see a `package.json` directly inside the extension folder, not nested one level deeper:

```sh
ls ~/.vscode/extensions/12-bit-rainbow
# package.json  README.md  themes/
```

A common mistake is `cp -R 12-bit-rainbow ~/.vscode/extensions/12-bit-rainbow` when the target
directory already exists — that nests it as `.../12-bit-rainbow/12-bit-rainbow`. Remove the folder
and copy again.

**Colors look off after switching.** Old `workbench.colorCustomizations` from a previous theme can
leak through if they aren't scoped to a theme name. Check your user settings for un-scoped
overrides.

**Terminal colors don't match Ghostty.** Some shell prompts (Powerlevel10k, Starship) hardcode hex
colors instead of using ANSI slots. That's the prompt's doing, not the theme's.

---

## Working on the theme

```sh
git clone https://github.com/rmpato/12-bit-rainbow.git
cd 12-bit-rainbow
code .
```

Press `F5` to launch an Extension Development Host — a second VS Code window with the theme loaded.
Edit `themes/12-bit-rainbow-color-theme.json` and the changes apply live in that window, no reload
needed.

The file has three sections:

- `colors` — the editor chrome. Key names are documented in the
  [VS Code theme color reference](https://code.visualstudio.com/api/references/theme-color).
- `tokenColors` — TextMate scopes, the classic regex-based syntax rules.
- `semanticTokenColors` — language-server-driven colors, which take priority when available.

Before opening a pull request:

```sh
npm install
npm run validate    # manifest + theme: malformed hex, unknown fontStyle, missing paths
npm run package     # validates, then builds a .vsix
npx vsce ls         # exactly what would ship
```

`npm run validate` catches the class of mistake that packages cleanly and then fails silently for
whoever installed it — VS Code ignores a malformed colour value and falls back to the default
theme's, which is how one stray panel ends up the wrong blue.

If you change the palette, redraw the icon and commit it:

```sh
npm run icon        # regenerates assets/icon.png from the theme file
```

CI fails if the committed icon is not what the generator would produce, so the artwork cannot drift
away from the theme it advertises.

Pull requests welcome — especially for languages whose highlighting looks flat. Include a before
and after screenshot if you can.

## Releasing

Versions follow semver, described in [CHANGELOG.md](CHANGELOG.md). To ship one:

1. Move the `Unreleased` entries in `CHANGELOG.md` under the new version.
2. `npm version minor` (or `patch` / `major`) — this writes `package.json` and creates the tag.
3. `git push --follow-tags`.

The `v*` tag triggers the release workflow: it validates, checks the tag matches the manifest
version, packages, publishes to both marketplaces, and attaches the `.vsix` to a GitHub Release.

Two repository secrets control publishing, and each one is optional — a missing token skips that
marketplace instead of failing the release:

| Secret | Where it comes from |
|---|---|
| `VSCE_PAT` | An Azure DevOps personal access token with **Marketplace → Manage** |
| `OVSX_PAT` | An [Open VSX](https://open-vsx.org) access token |

`workflow_dispatch` runs the same job with publishing off, which is the way to test the pipeline
without spending a version number.

---

## Credits

The palette is from the **12-bit Rainbow** theme bundled with
[Ghostty](https://github.com/ghostty-org/ghostty), which sources its theme collection from
[iTerm2-Color-Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes). This repository is only
the VS Code port.

## License

MIT — see [LICENSE](LICENSE).
