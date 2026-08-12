#!/usr/bin/env node
/*
 * Checks the things that only break after publishing.
 *
 * `vsce package` will happily build a VSIX whose theme file is unparseable,
 * whose colour values are malformed, or whose declared path points at nothing —
 * none of that is validated at package time, and all of it surfaces as "the
 * theme does not appear in the list" for whoever installed it.
 *
 *     npm run validate
 *
 * No dependencies, so it runs before `npm install` has a chance to matter.
 */

import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const problems = [];
const notes = [];

function fail(message) {
    problems.push(message);
}

function readJson(relative) {
    const path = resolve(root, relative);
    if (!existsSync(path)) {
        fail(`${relative} does not exist`);
        return null;
    }
    try {
        return JSON.parse(readFileSync(path, "utf8"));
    } catch (error) {
        fail(`${relative} is not valid JSON: ${error.message}`);
        return null;
    }
}

const manifest = readJson("package.json");

if (manifest) {
    /* Fields the marketplace listing looks empty or broken without. */
    for (const field of ["name", "displayName", "description", "version", "publisher", "license", "icon"]) {
        if (!manifest[field]) fail(`package.json is missing "${field}"`);
    }

    if (!/^\d+\.\d+\.\d+$/.test(manifest.version ?? "")) {
        fail(`version "${manifest.version}" is not x.y.z — the marketplace rejects anything else`);
    }

    if (manifest.icon && !existsSync(resolve(root, manifest.icon))) {
        fail(`icon "${manifest.icon}" does not exist — run \`npm run icon\``);
    }

    if (!manifest.repository?.url) fail("package.json is missing repository.url");

    const themes = manifest.contributes?.themes ?? [];
    if (themes.length === 0) fail("package.json contributes no themes");

    for (const entry of themes) {
        if (!entry.label) fail("a contributed theme has no label");
        if (!["vs", "vs-dark", "hc-black", "hc-light"].includes(entry.uiTheme)) {
            fail(`theme "${entry.label}" has an invalid uiTheme: ${entry.uiTheme}`);
        }

        const theme = readJson(entry.path);
        if (!theme) continue;

        if (!theme.name) fail(`${entry.path} has no "name"`);
        if (!["dark", "light"].includes(theme.type)) {
            fail(`${entry.path} has type "${theme.type}" — expected "dark" or "light"`);
        }

        checkColours(entry.path, theme);
    }
}

/*
 * Every value in `colors` must be #rgb, #rgba, #rrggbb or #rrggbbaa. VS Code
 * silently ignores a malformed one and falls back to the default theme's value
 * for that key, which is how a theme ends up with one stray blue panel.
 */
function checkColours(path, theme) {
    const hex = /^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/;

    for (const [key, value] of Object.entries(theme.colors ?? {})) {
        if (typeof value !== "string" || !hex.test(value)) {
            fail(`${path}: colors["${key}"] is not a hex colour (${JSON.stringify(value)})`);
        }
    }

    for (const [index, rule] of (theme.tokenColors ?? []).entries()) {
        const where = `${path}: tokenColors[${index}]`;
        if (!rule.settings) {
            fail(`${where} has no settings`);
            continue;
        }
        const { foreground, fontStyle } = rule.settings;
        if (foreground !== undefined && !hex.test(foreground)) {
            fail(`${where}.settings.foreground is not a hex colour (${JSON.stringify(foreground)})`);
        }
        /* "" is valid and means "no style"; anything else must be from the set. */
        if (fontStyle !== undefined && fontStyle !== "") {
            const allowed = ["italic", "bold", "underline", "strikethrough"];
            const unknown = fontStyle.split(/\s+/).filter((part) => !allowed.includes(part));
            if (unknown.length) fail(`${where}.settings.fontStyle has unknown value(s): ${unknown.join(", ")}`);
        }
    }

    const count = Object.keys(theme.colors ?? {}).length;
    notes.push(`${path}: ${count} workbench colours, ${(theme.tokenColors ?? []).length} token rules`);
}

for (const note of notes) console.log(`  ${note}`);

if (problems.length) {
    console.error(`\n✗ ${problems.length} problem${problems.length === 1 ? "" : "s"}:\n`);
    for (const problem of problems) console.error(`  - ${problem}`);
    process.exit(1);
}

console.log("\n✓ theme and manifest look publishable");
