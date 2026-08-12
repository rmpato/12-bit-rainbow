# TODO

What is left before this theme is properly published, and what would make it
better afterwards. Not shipped in the `.vsix` — this is a repository document.

Order matters in the first section: nothing below it can happen until those are
done.

---

## Blocking publication

- [ ] **Confirm the `pato` publisher ID exists on the Visual Studio Marketplace.**
      `package.json` has claimed `"publisher": "pato"` since the first commit,
      but the ID has never been verified against a real account. Create or check
      it at <https://marketplace.visualstudio.com/manage>.

      If the ID has to change, four things change together — miss one and the
      badges 404 or the install command points at nothing:

      | Where | What |
      |---|---|
      | `package.json` | `publisher` |
      | `README.md` | both badge URLs, and `code --install-extension <id>` |
      | `.github/workflows/release.yml` | the two marketplace links in the release body |
      | Open VSX | the namespace must be created separately, and match |

- [ ] **Create the Open VSX namespace.** Separate registry, separate account,
      and the namespace is claimed rather than assumed:
      `npx ovsx create-namespace pato -p <token>`. Without it the publish step
      fails even with a valid token.

- [ ] **Add the two repository secrets.** Until these exist the release workflow
      packages and attaches the `.vsix` but publishes nowhere — a skip, not a
      failure, so a first release cannot break on a missing secret.

      | Secret | Where it comes from |
      |---|---|
      | `VSCE_PAT` | Azure DevOps PAT, **Marketplace → Manage** scope, all accessible organisations |
      | `OVSX_PAT` | <https://open-vsx.org> → profile → Access Tokens |

- [ ] **Dry-run the release workflow** before tagging anything. Actions → Release
      → *Run workflow*, leaving `dry_run` checked. It packages and validates
      without spending a version number.

- [ ] **Cut `v1.0.0`.** `npm version patch` (or `minor`), then
      `git push --follow-tags`. Move the `Unreleased` block in `CHANGELOG.md`
      under the new heading first — the marketplace renders that file, so it is
      read by people deciding whether to install.

## Highest value once it is live

- [ ] **Screenshots.** The single biggest gap. A theme is chosen with the eyes
      and the listing currently offers a table of hex codes. Wanted:

      - A wide editor shot with the sidebar, tabs and status bar visible.
      - Two or three language close-ups — one curly-brace language, one
        indentation-based, one markup or config file.
      - The integrated terminal beside Ghostty, since matching them is the
        entire premise and nothing else on the page demonstrates it.

      Marketplace READMEs cannot use relative image paths. Commit the files and
      link them at their absolute
      `https://raw.githubusercontent.com/rmpato/12-bit-rainbow/main/...` URL, and
      keep them out of the `.vsix` via `.vscodeignore`.

- [ ] **Light variant?** Open question, not a commitment. The 12-bit rainbow was
      designed for charts on white, so the hues have the contrast for it — but a
      light theme is a second palette to maintain, and the premise of this one is
      matching a near-black terminal. Decide deliberately rather than by drift.

## Coverage worth checking

Every one of these is "open a real file in the theme and look", not a code
change until something is visibly wrong.

- [ ] Markdown, YAML, TOML and JSON with comments — config files get read more
      than they get syntax-highlighted well.
- [ ] Go, Rust and Python via their language servers, where semantic tokens take
      priority over the TextMate rules and can disagree with them.
- [ ] Diff and merge-conflict views. Three-way merge is the most colour-dependent
      screen in the editor and the easiest to leave unthemed.
- [ ] Notebooks, if you use them. Cell chrome has its own colour keys that are
      not covered by the editor ones.
- [ ] Accessibility: run the foreground/background pairs through a contrast
      checker. `#685656` comments on `#040404` is the one most likely to fail
      WCAG AA, and it is the token that appears on almost every line.

## Maintenance

- [ ] Decide whether `engines.vscode` should stay at `^1.70.0`. It is generous —
      July 2022 — and costs nothing today, but any new theme key added since then
      cannot be used while it stands.
- [ ] Add a screenshot-regeneration note to the release checklist once the
      screenshots exist, so a palette change does not leave the listing showing
      colours the extension no longer has.

---

*Anything checked here belongs in `CHANGELOG.md` too, if a user would notice it.*
