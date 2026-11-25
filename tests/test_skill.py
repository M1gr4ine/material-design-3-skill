"""Integrity, CLI, HCT theme, CSS token sync, and spring physics tests."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import component  # noqa: E402
import theme  # noqa: E402


def run_cli(entry, argv: list[str]) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        entry(argv)
    return buf.getvalue()


def expect_cli_error(test: unittest.TestCase, entry, argv: list[str]) -> None:
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        with test.assertRaises(SystemExit) as ctx:
            entry(argv)
    test.assertEqual(ctx.exception.code, 2)


class SkillIntegrityTests(unittest.TestCase):
    def test_skill_frontmatter_meets_agentskills_spec(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md must start with YAML frontmatter")
        fm = match.group(1)
        name_m = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
        self.assertIsNotNone(name_m)
        name = name_m.group(1)
        self.assertLessEqual(len(name), 64)
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertIn("Material Design 3", fm)
        self.assertIn("M3 Expressive", fm)
        self.assertIn("license:", fm)
        self.assertIn("compatibility:", fm)

    def test_zero_broken_relative_markdown_links(self) -> None:
        md_files = [ROOT / "SKILL.md", ROOT / "README.md", *sorted((ROOT / "references").glob("*.md"))]
        broken: list[tuple[str, str]] = []
        for md in md_files:
            content = md.read_text(encoding="utf-8")
            for link in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
                href = link.group(1)
                if href.startswith(("http://", "https://", "#")):
                    continue
                if not (md.parent / href).resolve().exists():
                    broken.append((str(md.relative_to(ROOT)), href))
        self.assertEqual(broken, [])

    def test_all_component_tokens_resolve_cleanly(self) -> None:
        token_files = sorted((ROOT / "assets" / "tokens").glob("*.json"))
        self.assertEqual(len(token_files), 36)
        catalog = component.SystemCatalog()
        all_tokens = catalog.all_component_tokens()
        self.assertEqual(len(all_tokens), 5091)

        opts = component.ResolveOptions()
        unresolved: list[str] = []

        def check_aliases(val: object) -> None:
            if isinstance(val, str) and val.startswith("md."):
                found, resolved = catalog.lookup_system(val, opts)
                if found:
                    self.assertIsNotNone(resolved)
                elif val not in all_tokens:
                    unresolved.append(val)
            elif isinstance(val, dict):
                for sub in val.values():
                    check_aliases(sub)
            elif isinstance(val, list):
                for sub in val:
                    check_aliases(sub)

        for value in all_tokens.values():
            check_aliases(value)
        self.assertEqual(unresolved, [])

    def test_tokens_css_matches_official_json_snapshots(self) -> None:
        css = (ROOT / "assets" / "tokens.css").read_text(encoding="utf-8")
        colors = json.loads((ROOT / "assets" / "baseline-colors.json").read_text(encoding="utf-8"))
        metrics = json.loads((ROOT / "assets" / "metrics.json").read_text(encoding="utf-8"))["tokens"]
        typescale = json.loads((ROOT / "assets" / "type-scale.json").read_text(encoding="utf-8"))

        root_block = re.search(r":root\s*\{(.*?)\n\}", css, re.DOTALL)
        dark_block = re.search(r'\[data-theme="dark"\]\s*\{(.*?)\n\}', css, re.DOTALL)
        light_block = re.search(r'\[data-theme="light"\]\s*\{(.*?)\n\}', css, re.DOTALL)
        self.assertIsNotNone(root_block)
        self.assertIsNotNone(dark_block)
        self.assertIsNotNone(light_block)

        for role, hex_val in colors["light"].items():
            var = "--" + role.replace(".", "-")
            self.assertIn(f"{var}: {hex_val};", root_block.group(1))
            self.assertIn(f"{var}: {hex_val};", light_block.group(1))
        for role, hex_val in colors["dark"].items():
            var = "--" + role.replace(".", "-")
            self.assertIn(f"{var}: {hex_val};", dark_block.group(1))

        for key, spec in metrics.items():
            var = "--" + key.replace(".", "-")
            if key.startswith("md.sys.measurement.space"):
                self.assertIn(f"{var}: {spec['length']['value']}px;", root_block.group(1))
            elif key.startswith("md.sys.state."):
                expected = f"{spec['opacity']}" if "opacity" in spec else f"{spec['length']['value']}px"
                self.assertIn(f"{var}: {expected};", root_block.group(1))
            elif key.startswith("md.sys.shape.corner.") and key.count(".") == 4:
                shape = spec["shape"]
                expected = "9999px" if shape["family"] == "SHAPE_FAMILY_CIRCULAR" else f"{shape.get('defaultSize', {}).get('value', 0)}px"
                self.assertIn(f"{var}: {expected};", root_block.group(1))

        for style_key, style in typescale["styles"].items():
            var = "--" + style_key.replace(".", "-")
            size_rem = f"{round(style['size'] / 16.0, 4):g}rem"
            lh_rem = f"{round(style['line-height'] / 16.0, 4):g}rem"
            track = f"{style['tracking']}px" if style["tracking"] != 0 else "0"
            self.assertIn(f"{var}-size: {size_rem};", root_block.group(1))
            self.assertIn(f"{var}-line-height: {lh_rem};", root_block.group(1))
            self.assertIn(f"{var}-weight: {style['weight']};", root_block.group(1))
            self.assertIn(f"{var}-tracking: {track};", root_block.group(1))

    def test_motion_css_matches_official_json_snapshot(self) -> None:
        css = (ROOT / "assets" / "motion.css").read_text(encoding="utf-8")
        motion = json.loads((ROOT / "assets" / "motion.json").read_text(encoding="utf-8"))
        blocks = {
            "expressive": re.search(r':root,\s*\[data-m3-motion="expressive"\]\s*\{(.*?)\n\}', css, re.DOTALL),
            "standard": re.search(r'\[data-m3-motion="standard"\]\s*\{(.*?)\n\}', css, re.DOTALL),
        }
        for scheme, match in blocks.items():
            self.assertIsNotNone(match, f"Missing motion.css block for {scheme}")
            body = match.group(1)
            for token_name, spec in motion["schemes"][scheme].items():
                slot = token_name.removeprefix("md.sys.motion.spring.").replace(".", "-")
                web = spec["web"]
                curve = ", ".join(str(v) for v in web["cubicBezier"])
                self.assertIn(f"--m3-{slot}-duration: {web['durationMs']}ms;", body)
                self.assertIn(f"--m3-{slot}-curve: cubic-bezier({curve});", body)


class ComponentCliTests(unittest.TestCase):
    def test_list_and_alias_resolution(self) -> None:
        listing = run_cli(component.main, [])
        self.assertEqual(len(listing.strip().splitlines()), 36)
        slugs = sorted(p.stem for p in component.TOKENS_DIR.glob("*.json"))
        cases = {
            "button": "buttons",
            "按钮": "buttons",
            "menu": "menus",
            "弹窗": "dialogs",
            "modal": "dialogs",
            "toast": "snackbar",
            "搜索条": "search",
            "navigation rail": "navigation-rail",
            "text_field": "text-fields",
            "tab": "tabs",
            "progress-indicator": "progress-indicators",  # singular heuristic (not in ALIASES)
            "dividers": "divider",  # plural-of-singular heuristic
            "floating": "floating-action-button",  # unique substring match
        }
        for query, expected in cases.items():
            slug, _ = component.resolve_slug(query, slugs)
            self.assertEqual(slug, expected, f"Failed query: {query}")

        ambig_slug, ambig_matches = component.resolve_slug("bar", slugs)
        self.assertIsNone(ambig_slug)
        self.assertGreater(len(ambig_matches), 1)
        miss_slug, miss_matches = component.resolve_slug("nonexistent-widget", slugs)
        self.assertIsNone(miss_slug)
        self.assertEqual(miss_matches, [])

    def test_token_resolve_bycontext_motion_global_and_cli_guards(self) -> None:
        resolved_light = json.loads(
            run_cli(component.main, ["search", "--token", "search-bar.container.color", "--resolve", "--theme", "light"])
        )
        self.assertEqual(resolved_light["md.comp.search-bar.container.color"]["value"], "#ece6f0")

        resolved_dark = json.loads(
            run_cli(component.main, ["search", "--token", "search-bar.container.color", "--resolve", "--theme", "dark"])
        )
        self.assertEqual(resolved_dark["md.comp.search-bar.container.color"]["value"], "#2b2930")

        resolved_both = json.loads(
            run_cli(component.main, ["search", "--token", "search-bar.container.color", "--resolve"])
        )
        self.assertEqual(
            resolved_both["md.comp.search-bar.container.color"]["value"],
            {"light": "#ece6f0", "dark": "#2b2930"},
        )

        composite = json.loads(
            run_cli(component.main, ["search", "--token", "search-bar.input-text.type", "--resolve"])
        )
        size_node = composite["md.comp.search-bar.input-text.type"]["type"]["fontSizeTokenName"]
        self.assertEqual(size_node["resolved"]["value"], 16)

        by_ctx = json.loads(
            run_cli(component.main, ["progress-indicators", "--token", "four-color.active-indicator.one.color", "--resolve", "--theme", "dark"])
        )
        ctx_entry = by_ctx["md.comp.circular-progress-indicator.four-color.active-indicator.one.color"]["byContext"]
        self.assertEqual(ctx_entry["Audience=3P"]["value"], "#d0bcff")

        scalar_motion = json.loads(
            run_cli(component.main, ["button-groups", "--token", "standard.large.pressed.item.width.motion.spring.dampening", "--resolve", "--motion", "standard"])
        )
        first_scalar = next(iter(scalar_motion.values()))
        self.assertEqual(first_scalar["value"], 0.9)

        global_resolved = json.loads(
            run_cli(component.main, ["--token", "floating.standard.container.color", "--resolve", "--theme", "light"])
        )
        self.assertEqual(
            global_resolved["toolbars"]["md.comp.toolbar.floating.standard.container.color"]["value"],
            "#f3edf7",
        )

        sys_both = json.loads(run_cli(component.main, ["--sys", "fast.spatial"]))
        self.assertEqual(sys_both["md.sys.motion.spring.fast.spatial"]["expressive"]["dampingRatio"], 0.6)
        self.assertEqual(sys_both["md.sys.motion.spring.fast.spatial"]["standard"]["dampingRatio"], 0.9)

        # CLI invalid combinations must fail loudly instead of silently ignoring flags.
        expect_cli_error(self, component.main, ["search", "--sys", "fast.spatial"])
        expect_cli_error(self, component.main, ["--sys", "fast.spatial", "--token", "height"])
        expect_cli_error(self, component.main, ["--sys", "fast.spatial", "--resolve"])
        expect_cli_error(self, component.main, ["search", "--resolve"])


class ThemeGeneratorTests(unittest.TestCase):
    def test_hct_roundtrip_golden_and_baseline_proximity(self) -> None:
        for hex_color in ("#6750a4", "#1a73e8", "#006874", "#e53935", "#ffeb3b", "#000000", "#ffffff", "#808080"):
            rgb = theme.parse_hex(hex_color)
            hct = theme.rgb_to_hct(rgb)
            rebuilt = theme.hct_to_rgb(hct.hue, hct.chroma, hct.tone)
            for orig_c, new_c in zip(rgb, rebuilt):
                self.assertLessEqual(abs(orig_c - new_c), 2, f"Drift too large for {hex_color}: {rgb} vs {rebuilt}")

        # Golden HCT check on official M3 baseline primary #6750a4 (kills symmetric error mutants).
        seed_hct = theme.rgb_to_hct(theme.parse_hex("#6750a4"))
        self.assertAlmostEqual(seed_hct.hue, 299.0, delta=1.0)
        self.assertAlmostEqual(seed_hct.chroma, 47.9, delta=1.0)
        self.assertAlmostEqual(seed_hct.tone, 40.1, delta=0.5)

        baseline = json.loads(theme.BASELINE_PATH.read_text(encoding="utf-8"))
        fidelity = theme.generate_theme("#6750a4", variant="fidelity", contrast="standard")
        for mode, role in (("light", "md.sys.color.primary"), ("dark", "md.sys.color.surface"), ("light", "md.sys.color.secondary")):
            got_rgb = theme.parse_hex(fidelity[mode][role])
            exp_rgb = theme.parse_hex(baseline[mode][role])
            for g, e in zip(got_rgb, exp_rgb):
                self.assertLessEqual(abs(g - e), 3, f"Baseline mismatch for {mode} {role}: {got_rgb} vs {exp_rgb}")

    def test_role_parity_variant_distinctness_and_validation(self) -> None:
        baseline = json.loads(theme.BASELINE_PATH.read_text(encoding="utf-8"))
        tonal = theme.generate_theme("#1A73E8", variant="tonal-spot", contrast="standard")
        expressive = theme.generate_theme("#1A73E8", variant="expressive", contrast="standard")
        vibrant = theme.generate_theme("#1A73E8", variant="vibrant", contrast="standard")
        mono = theme.generate_theme("#1A73E8", variant="monochrome", contrast="standard")

        self.assertEqual(set(tonal["light"].keys()), set(baseline["light"].keys()))
        self.assertEqual(set(tonal["dark"].keys()), set(baseline["dark"].keys()))

        tonal_p = theme.rgb_to_hct(theme.parse_hex(tonal["light"]["md.sys.color.primary"]))
        exp_p = theme.rgb_to_hct(theme.parse_hex(expressive["light"]["md.sys.color.primary"]))
        vib_p = theme.rgb_to_hct(theme.parse_hex(vibrant["light"]["md.sys.color.primary"]))
        mono_p = theme.rgb_to_hct(theme.parse_hex(mono["light"]["md.sys.color.primary"]))

        mono_rgb = theme.parse_hex(mono["light"]["md.sys.color.primary"])
        self.assertEqual(mono_rgb[0], mono_rgb[1])
        self.assertEqual(mono_rgb[1], mono_rgb[2])
        self.assertLess(mono_p.chroma, 2.0)
        self.assertGreater(vib_p.chroma, tonal_p.chroma + 10.0)
        hue_diff = (exp_p.hue - tonal_p.hue) % 360.0
        self.assertAlmostEqual(hue_diff, 240.0, delta=3.0)

        with self.assertRaises(ValueError):
            theme.generate_theme("#1A73E8", variant="unknown-variant")
        with self.assertRaises(ValueError):
            theme.generate_theme("#1A73E8", contrast="ultra")

    def test_wcag_aa_and_monotonic_contrast_across_hues(self) -> None:
        seeds = [
            theme.format_hex(theme.hct_to_rgb(hue, 48.0, 50.0))
            for hue in range(0, 360, 30)
        ]
        for seed in seeds:
            for variant in theme.VARIANTS:
                for contrast in theme.CONTRAST_OVERRIDES:
                    generated = theme.generate_theme(seed, variant=variant, contrast=contrast)
                    rows, failures = theme.audit_theme(generated)
                    self.assertEqual(failures, 0, f"WCAG failure for seed={seed} variant={variant} contrast={contrast}")
                    if contrast == "high":
                        for row in rows:
                            if row["min"] >= 4.5:
                                self.assertGreaterEqual(row["ratio"], 7.0, f"High contrast AAA miss: {row}")

        std = theme.generate_theme("#1A73E8", contrast="standard")
        med = theme.generate_theme("#1A73E8", contrast="medium")
        high = theme.generate_theme("#1A73E8", contrast="high")
        for mode in ("light", "dark"):
            for fg, bg in (("md.sys.color.on-primary", "md.sys.color.primary"),
                           ("md.sys.color.on-surface-variant", "md.sys.color.surface"),
                           ("md.sys.color.outline", "md.sys.color.surface")):
                r_std = theme.contrast_ratio(std[mode][fg], std[mode][bg])
                r_med = theme.contrast_ratio(med[mode][fg], med[mode][bg])
                r_high = theme.contrast_ratio(high[mode][fg], high[mode][bg])
                self.assertLess(r_std, r_med)
                self.assertLess(r_med, r_high)

    def test_all_output_formats_audit_and_pair_thresholds(self) -> None:
        css = run_cli(theme.main, ["--seed", "#1A73E8", "--format", "css"])
        self.assertIn("--md-sys-color-primary:", css)
        self.assertIn("@media (prefers-color-scheme: dark)", css)
        self.assertIn('[data-theme="dark"]', css)
        self.assertIn('[data-theme="light"]', css)

        raw_json = json.loads(run_cli(theme.main, ["--seed", "#1A73E8", "--format", "json"]))
        self.assertEqual(raw_json["seed"], "#1a73e8")
        self.assertEqual(len(raw_json["light"]), 50)
        self.assertEqual(len(raw_json["dark"]), 50)

        tw = run_cli(theme.main, ["--seed", "#1A73E8", "--format", "tailwind"])
        self.assertIn("@theme inline {", tw)
        self.assertIn("--color-md-primary: var(--md-sys-color-primary);", tw)

        compose = run_cli(theme.main, ["--seed", "#1A73E8", "--format", "compose"])
        self.assertIn("lightColorScheme(", compose)
        self.assertIn("darkColorScheme(", compose)
        self.assertIn("inverseOnSurface = Color(", compose)

        flutter = run_cli(theme.main, ["--seed", "#1A73E8", "--format", "flutter"])
        self.assertIn("const lightColorScheme = ColorScheme(", flutter)
        self.assertIn("const darkColorScheme = ColorScheme(", flutter)
        self.assertIn("onInverseSurface: Color(", flutter)
        self.assertIn("shadow: Color(", flutter)
        self.assertNotIn("  background:", flutter)
        self.assertNotIn("  surfaceVariant:", flutter)

        # Baseline audit CLI passes; low-contrast theme fails audit.
        audit_out = run_cli(theme.main, ["--audit"])
        self.assertIn("[PASS]", audit_out)
        broken = theme.generate_theme("#1A73E8")
        broken["light"]["md.sys.color.on-primary"] = broken["light"]["md.sys.color.primary"]
        _, fail_count = theme.audit_theme(broken)
        self.assertGreater(fail_count, 0)

        # Pair contrast threshold boundaries.
        fail_pair = json.loads(run_cli(theme.main, ["--pair", "#999999", "#ffffff"]))
        self.assertFalse(fail_pair["aa_large_or_ui"])
        self.assertFalse(fail_pair["aa_normal_text"])
        self.assertFalse(fail_pair["aaa_normal_text"])

        large_only = json.loads(run_cli(theme.main, ["--pair", "#767676", "#eeeeee"]))
        self.assertTrue(large_only["aa_large_or_ui"])
        self.assertFalse(large_only["aa_normal_text"])
        self.assertFalse(large_only["aaa_normal_text"])

        aa_only = json.loads(run_cli(theme.main, ["--pair", "#6750a4", "#ffffff"]))
        self.assertTrue(aa_only["aa_large_or_ui"])
        self.assertTrue(aa_only["aa_normal_text"])
        self.assertFalse(aa_only["aaa_normal_text"])

        aaa_pair = json.loads(run_cli(theme.main, ["--pair", "#1d1b20", "#fef7ff"]))
        self.assertTrue(aaa_pair["aa_large_or_ui"])
        self.assertTrue(aaa_pair["aa_normal_text"])
        self.assertTrue(aaa_pair["aaa_normal_text"])

        # CLI validation errors.
        expect_cli_error(self, theme.main, ["--seed", "not-hex"])
        expect_cli_error(self, theme.main, ["--audit", "--contrast", "high"])
        expect_cli_error(self, theme.main, ["--pair", "#000000", "#ffffff", "--seed", "#1A73E8"])


class SpringPhysicsTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "Node.js required for spring.mjs test")
    def test_spring_presets_converge_and_clamp_negative_dt(self) -> None:
        js = (
            "import assert from 'node:assert/strict';"
            "import fs from 'node:fs';"
            "import { sampleSpring, createSpring } from './assets/spring.mjs';"
            "const motion = JSON.parse(fs.readFileSync('./assets/motion.json', 'utf8'));"
            "for (const scheme of Object.values(motion.schemes)) {"
            "  for (const spec of Object.values(scheme)) {"
            "    const start = sampleSpring(0, 0, 100, 0, spec);"
            "    assert.equal(start.position, 0);"
            "    const end = sampleSpring(0, 0, 100, 3.0, spec);"
            "    assert.ok(Math.abs(end.position - 100) < 0.01);"
            "  }"
            "}"
            "let cb = null;"
            "globalThis.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });"
            "globalThis.requestAnimationFrame = fn => { cb = fn; return 1; };"
            "globalThis.cancelAnimationFrame = () => { cb = null; };"
            "const rendered = [];"
            "const spec = motion.schemes.expressive['md.sys.motion.spring.fast.spatial'];"
            "const s = createSpring(0, spec, v => rendered.push(v));"
            "s.to(100, 0);"
            "cb(0);"
            "assert.equal(rendered.at(-1), 0, 'negative rAF dt must clamp to 0');"
            "cb(performance.now() + 3000);"
            "assert.equal(rendered.at(-1), 100, 'spring must advance and settle at target');"
            "s.dispose();"
        )
        proc = subprocess.run(["node", "--input-type=module", "-e", js], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
