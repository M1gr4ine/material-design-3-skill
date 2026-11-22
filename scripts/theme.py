"""Zero-dependency Material Design 3 HCT dynamic theme generator & WCAG 2.1 contrast auditor."""
from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import sys
from typing import Literal, TypedDict

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "assets" / "baseline-colors.json"
HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")

# Standard D65 CAM16 viewing conditions matching Google Material Color Utilities.
WHITE_D65 = (95.047, 100.0, 108.883)
C_SURROUND = 0.69
NC_SURROUND = 1.0
F_SURROUND = 1.0


class Theme(TypedDict):
    seed: str
    variant: str
    contrast: str
    light: dict[str, str]
    dark: dict[str, str]


AuditRow = TypedDict(
    "AuditRow",
    {
        "mode": Literal["light", "dark"],
        "pair": str,
        "fg": str,
        "bg": str,
        "ratio": float,
        "min": float,
        "pass": bool,
    },
)


def srgb_to_linear(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def linear_to_srgb(channel: float) -> float:
    if channel <= 0.0:
        return 0.0
    if channel >= 1.0:
        return 1.0
    return 12.92 * channel if channel <= 0.0031308 else 1.055 * (channel ** (1.0 / 2.4)) - 0.055


def parse_hex(color: str) -> tuple[int, int, int]:
    match = HEX_RE.match(color.strip())
    if not match:
        raise ValueError(f"Expected 6-digit hex color like #6750a4, got {color!r}")
    raw = match.group(1)
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def format_hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def y_from_lstar(lstar: float) -> float:
    ft = (lstar + 16.0) / 116.0
    yn = ft ** 3 if ft > 6.0 / 29.0 else (116.0 * ft - 16.0) / (24389.0 / 27.0)
    return yn * 100.0


def lstar_from_y(y: float) -> float:
    yn = y / 100.0
    ft = yn ** (1.0 / 3.0) if yn > 216.0 / 24389.0 else (24389.0 / 27.0 * yn + 16.0) / 116.0
    return 116.0 * ft - 16.0


def _xyz_to_cat16(x: float, y: float, z: float) -> tuple[float, float, float]:
    return (
        0.401288 * x + 0.650173 * y - 0.051461 * z,
        -0.250268 * x + 1.204414 * y + 0.045854 * z,
        -0.002079 * x + 0.048952 * y + 0.953127 * z,
    )


def _cat16_to_xyz(r: float, g: float, b: float) -> tuple[float, float, float]:
    return (
        1.86206786 * r - 1.01125463 * g + 0.14918677 * b,
        0.38752654 * r + 0.62144744 * g - 0.00897398 * b,
        -0.01584150 * r - 0.03412294 * g + 1.04996444 * b,
    )


YB = y_from_lstar(50.0)
LA = (200.0 / math.pi) * YB / 100.0
_RW, _GW, _BW = _xyz_to_cat16(*WHITE_D65)
_D = max(0.0, min(1.0, F_SURROUND * (1.0 - (1.0 / 3.6) * math.exp((-LA - 42.0) / 92.0))))
DR, DG, DB = (_D * (100.0 / w) + 1.0 - _D for w in (_RW, _GW, _BW))
_K = 1.0 / (5.0 * LA + 1.0)
_K4 = _K ** 4
FL = _K4 * LA + 0.1 * (1.0 - _K4) ** 2 * ((5.0 * LA) ** (1.0 / 3.0))
N_BG = YB / WHITE_D65[1]
Z_EXP = 1.48 + math.sqrt(N_BG)
NBB = 0.725 * (N_BG ** -0.2)
NCB = NBB


def _compress(v: float) -> float:
    p = (FL * abs(v) / 100.0) ** 0.42
    return math.copysign(400.0 * p / (p + 27.13), v)


def _uncompress(va: float) -> float | None:
    av = abs(va)
    if av >= 399.999:
        return None
    return math.copysign((100.0 / FL) * ((27.13 * av) / (400.0 - av)) ** (1.0 / 0.42), va)


_RWA, _GWA, _BWA = (_compress(d * w) for d, w in ((DR, _RW), (DG, _GW), (DB, _BW)))
AW = (2.0 * _RWA + _GWA + 0.05 * _BWA) * NBB


def rgb_to_xyz(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    rl, gl, bl = (srgb_to_linear(c / 255.0) * 100.0 for c in rgb)
    return (
        0.41233895 * rl + 0.35762064 * gl + 0.18051042 * bl,
        0.2126 * rl + 0.7152 * gl + 0.0722 * bl,
        0.01932141 * rl + 0.11916382 * gl + 0.95034478 * bl,
    )


def xyz_to_linear_rgb(xyz: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = xyz
    return (
        (3.2413774792388685 * x - 1.5376652402851851 * y - 0.49885366846268053 * z) / 100.0,
        (-0.9691452513005321 * x + 1.8758853451067872 * y + 0.04156585616912061 * z) / 100.0,
        (0.05562093689691305 * x - 0.20395524564742123 * y + 1.0571799111220335 * z) / 100.0,
    )


@dataclass(frozen=True)
class Hct:
    hue: float
    chroma: float
    tone: float


def rgb_to_hct(rgb: tuple[int, int, int]) -> Hct:
    x, y, z = rgb_to_xyz(rgb)
    rc, gc, bc = _xyz_to_cat16(x, y, z)
    ra, ga, ba = _compress(DR * rc), _compress(DG * gc), _compress(DB * bc)
    a = ra - (12.0 * ga) / 11.0 + ba / 11.0
    bb = (ra + ga - 2.0 * ba) / 9.0
    u = (20.0 * ra + 20.0 * ga + 21.0 * ba) / 20.0
    p2 = (40.0 * ra + 20.0 * ga + ba) / 20.0
    hue = math.degrees(math.atan2(bb, a)) % 360.0
    ac = p2 * NBB
    j = 100.0 * ((ac / AW) ** (C_SURROUND * Z_EXP)) if ac > 0 else 0.0
    et = 0.25 * (math.cos(math.radians(hue) + 2.0) + 3.8)
    t = (50000.0 / 13.0) * NC_SURROUND * NCB * et * math.hypot(a, bb) / (u + 0.305)
    alpha = (t ** 0.9) * ((1.64 - 0.29 ** N_BG) ** 0.73) if t > 0 else 0.0
    chroma = alpha * math.sqrt(j / 100.0)
    return Hct(hue=hue, chroma=chroma, tone=lstar_from_y(y))


def _jch_to_xyz(j: float, chroma: float, hue: float) -> tuple[float, float, float] | None:
    if j <= 0.0:
        return 0.0, 0.0, 0.0
    alpha = chroma / math.sqrt(j / 100.0)
    t = (alpha / ((1.64 - 0.29 ** N_BG) ** 0.73)) ** (1.0 / 0.9) if alpha > 0 else 0.0
    h_rad = math.radians(hue)
    et = 0.25 * (math.cos(h_rad + 2.0) + 3.8)
    ac = AW * ((j / 100.0) ** (1.0 / (C_SURROUND * Z_EXP)))
    p1 = et * (50000.0 / 13.0) * NC_SURROUND * NCB
    p2 = ac / NBB
    if t == 0.0:
        a = bb = 0.0
    else:
        sin_h, cos_h = math.sin(h_rad), math.cos(h_rad)
        denom = 23.0 * p1 + 11.0 * t * cos_h + 108.0 * t * sin_h
        if denom <= 0.0:
            return None
        gamma = (23.0 * (p2 + 0.305) * t) / denom
        a = gamma * cos_h
        bb = gamma * sin_h
    ra = (460.0 * p2 + 451.0 * a + 288.0 * bb) / 1403.0
    ga = (460.0 * p2 - 891.0 * a - 261.0 * bb) / 1403.0
    ba = (460.0 * p2 - 220.0 * a - 6300.0 * bb) / 1403.0
    rc, gc, bc = _uncompress(ra), _uncompress(ga), _uncompress(ba)
    if rc is None or gc is None or bc is None:
        return None
    return _cat16_to_xyz(rc / DR, gc / DG, bc / DB)


def _solve_in_gamut(hue: float, chroma: float, tone: float) -> tuple[float, float, float] | None:
    target_y = y_from_lstar(tone)
    lo, hi = 0.0, 100.0
    for _ in range(36):
        mid = 0.5 * (lo + hi)
        xyz = _jch_to_xyz(mid, chroma, hue)
        if xyz is None or xyz[1] >= target_y:
            hi = mid
        else:
            lo = mid
    xyz = _jch_to_xyz(0.5 * (lo + hi), chroma, hue)
    if xyz is None or abs(xyz[1] - target_y) > 0.05:
        return None
    rl, gl, bl = xyz_to_linear_rgb(xyz)
    eps = 1e-4
    if -eps <= rl <= 1.0 + eps and -eps <= gl <= 1.0 + eps and -eps <= bl <= 1.0 + eps:
        return rl, gl, bl
    return None


def hct_to_rgb(hue: float, chroma: float, tone: float) -> tuple[int, int, int]:
    if tone <= 0.0001:
        return 0, 0, 0
    if tone >= 99.9999:
        return 255, 255, 255
    if chroma <= 0.001:
        g = round(linear_to_srgb(y_from_lstar(tone) / 100.0) * 255)
        return g, g, g
    hue_mod = hue % 360.0
    hit = _solve_in_gamut(hue_mod, chroma, tone)
    if hit is None:
        gray = y_from_lstar(tone) / 100.0
        best = (gray, gray, gray)
        lo, hi = 0.0, chroma
        for _ in range(28):
            mid = 0.5 * (lo + hi)
            cand = _solve_in_gamut(hue_mod, mid, tone)
            if cand is not None:
                best = cand
                lo = mid
            else:
                hi = mid
        hit = best
    return (
        round(linear_to_srgb(hit[0]) * 255),
        round(linear_to_srgb(hit[1]) * 255),
        round(linear_to_srgb(hit[2]) * 255),
    )


def _rotated_hue(source_hue: float, breakpoints: tuple[int, ...], rotations: tuple[int, ...]) -> float:
    for idx in range(len(breakpoints) - 1):
        if breakpoints[idx] <= source_hue < breakpoints[idx + 1]:
            return (source_hue + rotations[idx]) % 360.0
    return source_hue % 360.0


# Piecewise hue breakpoints (8 intervals spanning 0..360 deg) from Google Material Color Utilities.
EXPRESSIVE_HUES = (0, 21, 51, 121, 151, 191, 271, 321, 360)
EXPRESSIVE_SEC_ROT = (45, 95, 45, 20, 45, 90, 45, 45)
EXPRESSIVE_TER_ROT = (120, 120, 20, 45, 20, 15, 20, 120)

VIBRANT_HUES = (0, 41, 61, 101, 131, 181, 251, 301, 360)
VIBRANT_SEC_ROT = (18, 15, 10, 12, 15, 18, 15, 12)
VIBRANT_TER_ROT = (35, 30, 20, 25, 30, 35, 30, 25)

VARIANTS = ("tonal-spot", "fidelity", "expressive", "vibrant", "neutral", "monochrome")


@dataclass(frozen=True)
class PaletteSpec:
    primary: tuple[float, float]
    secondary: tuple[float, float]
    tertiary: tuple[float, float]
    neutral: tuple[float, float]
    neutral_variant: tuple[float, float]
    error: tuple[float, float] = (25.0, 84.0)


def build_palettes(seed: Hct, variant: str) -> PaletteSpec:
    h, c = seed.hue, seed.chroma
    if variant == "tonal-spot":
        return PaletteSpec((h, 36.0), (h, 16.0), ((h + 60.0) % 360.0, 24.0), (h, 6.0), (h, 8.0))
    if variant == "fidelity":
        return PaletteSpec(
            (h, max(c, 36.0)),
            (h, max(c / 3.0, 16.0)),
            ((h + 60.0) % 360.0, max(c / 2.0, 24.0)),
            (h, min(c / 8.0, 6.0)),
            (h, min(c / 4.0, 8.0)),
        )
    if variant == "expressive":
        return PaletteSpec(
            ((h + 240.0) % 360.0, 40.0),
            (_rotated_hue(h, EXPRESSIVE_HUES, EXPRESSIVE_SEC_ROT), 24.0),
            (_rotated_hue(h, EXPRESSIVE_HUES, EXPRESSIVE_TER_ROT), 32.0),
            ((h + 15.0) % 360.0, 8.0),
            ((h + 15.0) % 360.0, 12.0),
        )
    if variant == "vibrant":
        return PaletteSpec(
            (h, 200.0),
            (_rotated_hue(h, VIBRANT_HUES, VIBRANT_SEC_ROT), 24.0),
            (_rotated_hue(h, VIBRANT_HUES, VIBRANT_TER_ROT), 32.0),
            (h, 10.0),
            (h, 12.0),
        )
    if variant == "neutral":
        return PaletteSpec((h, 12.0), (h, 8.0), (h, 16.0), (h, 2.0), (h, 2.0))
    if variant == "monochrome":
        return PaletteSpec((h, 0.0), (h, 0.0), (h, 0.0), (h, 0.0), (h, 0.0))
    raise ValueError(f"Unknown variant: {variant}")


def _accent_roles(mode: Literal["light", "dark"]) -> dict[str, tuple[str, int]]:
    is_light = mode == "light"
    main_t, on_t = (40, 100) if is_light else (80, 20)
    cont_t, on_cont_t = (90, 30) if is_light else (30, 90)
    roles: dict[str, tuple[str, int]] = {}
    for name in ("primary", "secondary", "tertiary"):
        roles[name] = (name, main_t)
        roles[f"on-{name}"] = (name, on_t)
        roles[f"{name}-container"] = (name, cont_t)
        roles[f"on-{name}-container"] = (name, on_cont_t)
        roles[f"{name}-fixed"] = (name, 90)
        roles[f"{name}-fixed-dim"] = (name, 80)
        roles[f"on-{name}-fixed"] = (name, 10)
        roles[f"on-{name}-fixed-variant"] = (name, 30)
    roles["error"] = ("error", main_t)
    roles["on-error"] = ("error", on_t)
    roles["error-container"] = ("error", cont_t)
    roles["on-error-container"] = ("error", on_cont_t)
    roles["inverse-primary"] = ("primary", 80 if is_light else 40)
    roles["surface-tint"] = ("primary", main_t)
    roles["surface-tint-color"] = ("primary", main_t)
    return roles


# Official M3 semantic role -> (palette_field, tone) per mode.
TONE_TABLES: dict[Literal["light", "dark"], dict[str, tuple[str, int]]] = {
    "light": {
        **_accent_roles("light"),
        "background": ("neutral", 98),
        "on-background": ("neutral", 10),
        "surface": ("neutral", 98),
        "on-surface": ("neutral", 10),
        "surface-variant": ("neutral_variant", 90),
        "on-surface-variant": ("neutral_variant", 30),
        "surface-dim": ("neutral", 87),
        "surface-bright": ("neutral", 98),
        "surface-container-lowest": ("neutral", 100),
        "surface-container-low": ("neutral", 96),
        "surface-container": ("neutral", 94),
        "surface-container-high": ("neutral", 92),
        "surface-container-highest": ("neutral", 90),
        "inverse-surface": ("neutral", 20),
        "inverse-on-surface": ("neutral", 95),
        "outline": ("neutral_variant", 50),
        "outline-variant": ("neutral_variant", 80),
        "shadow": ("neutral", 0),
        "scrim": ("neutral", 0),
    },
    "dark": {
        **_accent_roles("dark"),
        "background": ("neutral", 6),
        "on-background": ("neutral", 90),
        "surface": ("neutral", 6),
        "on-surface": ("neutral", 90),
        "surface-variant": ("neutral_variant", 30),
        "on-surface-variant": ("neutral_variant", 80),
        "surface-dim": ("neutral", 6),
        "surface-bright": ("neutral", 24),
        "surface-container-lowest": ("neutral", 4),
        "surface-container-low": ("neutral", 10),
        "surface-container": ("neutral", 12),
        "surface-container-high": ("neutral", 17),
        "surface-container-highest": ("neutral", 22),
        "inverse-surface": ("neutral", 90),
        "inverse-on-surface": ("neutral", 20),
        "outline": ("neutral_variant", 60),
        "outline-variant": ("neutral_variant", 30),
        "shadow": ("neutral", 0),
        "scrim": ("neutral", 0),
    },
}


def _accent_overrides(
    main_t: int,
    *,
    on_t: int | None = None,
    cont_t: int | None = None,
    on_cont_t: int | None = None,
) -> dict[str, int]:
    result: dict[str, int] = {"surface-tint": main_t, "surface-tint-color": main_t}
    for name in ("primary", "secondary", "tertiary", "error"):
        result[name] = main_t
        if on_t is not None:
            result[f"on-{name}"] = on_t
        if cont_t is not None:
            result[f"{name}-container"] = cont_t
        if on_cont_t is not None:
            result[f"on-{name}-container"] = on_cont_t
    return result


# Standard (no override), medium, and high contrast overrides applied on top of TONE_TABLES.
CONTRAST_OVERRIDES: dict[str, dict[Literal["light", "dark"], dict[str, int]]] = {
    "standard": {"light": {}, "dark": {}},
    "medium": {
        "light": {
            **_accent_overrides(30, on_cont_t=20),
            "on-surface-variant": 25, "outline": 40, "outline-variant": 60,
        },
        "dark": {
            **_accent_overrides(85, on_t=15, on_cont_t=95),
            "on-background": 95, "on-surface": 95, "on-surface-variant": 85,
            "outline": 70, "outline-variant": 45,
        },
    },
    "high": {
        "light": {
            **_accent_overrides(20, cont_t=85, on_cont_t=10),
            "on-background": 0, "on-surface": 0, "on-surface-variant": 15,
            "outline": 25, "outline-variant": 45, "inverse-on-surface": 100,
        },
        "dark": {
            **_accent_overrides(92, on_t=0, cont_t=35, on_cont_t=100),
            "on-background": 100, "on-surface": 100, "on-surface-variant": 92,
            "outline": 80, "outline-variant": 60, "inverse-on-surface": 0,
        },
    },
}

AUDIT_PAIRS: tuple[tuple[str, str, float], ...] = (
    ("on-primary", "primary", 4.5),
    ("on-primary-container", "primary-container", 4.5),
    ("on-secondary", "secondary", 4.5),
    ("on-secondary-container", "secondary-container", 4.5),
    ("on-tertiary", "tertiary", 4.5),
    ("on-tertiary-container", "tertiary-container", 4.5),
    ("on-error", "error", 4.5),
    ("on-error-container", "error-container", 4.5),
    ("on-surface", "surface", 4.5),
    ("on-surface", "surface-container", 4.5),
    ("on-surface", "surface-container-high", 4.5),
    ("on-surface", "surface-container-highest", 4.5),
    ("on-surface-variant", "surface", 4.5),
    ("on-surface-variant", "surface-container-high", 4.5),
    ("inverse-on-surface", "inverse-surface", 4.5),
    ("on-primary-fixed", "primary-fixed", 4.5),
    ("on-primary-fixed-variant", "primary-fixed", 4.5),
    ("outline", "surface", 3.0),
)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (srgb_to_linear(c / 255.0) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    l1 = relative_luminance(parse_hex(fg_hex))
    l2 = relative_luminance(parse_hex(bg_hex))
    lighter, darker = (l1, l2) if l1 >= l2 else (l2, l1)
    return (lighter + 0.05) / (darker + 0.05)


def generate_scheme(palettes: PaletteSpec, mode: Literal["light", "dark"], contrast: str) -> dict[str, str]:
    if contrast not in CONTRAST_OVERRIDES:
        raise ValueError(f"Unknown contrast: {contrast}")
    base = TONE_TABLES[mode]
    overrides = CONTRAST_OVERRIDES[contrast][mode]
    cache: dict[tuple[str, int], str] = {}
    scheme: dict[str, str] = {}
    for role in sorted(base):
        palette_name, tone = base[role]
        tone = overrides.get(role, tone)
        key = (palette_name, tone)
        if key not in cache:
            hue, chroma = getattr(palettes, palette_name)
            cache[key] = format_hex(hct_to_rgb(hue, chroma, float(tone)))
        scheme[f"md.sys.color.{role}"] = cache[key]
    return scheme


def generate_theme(seed_hex: str, variant: str = "tonal-spot", contrast: str = "standard") -> Theme:
    rgb = parse_hex(seed_hex)
    seed_hct = rgb_to_hct(rgb)
    palettes = build_palettes(seed_hct, variant)
    return {
        "seed": format_hex(rgb),
        "variant": variant,
        "contrast": contrast,
        "light": generate_scheme(palettes, "light", contrast),
        "dark": generate_scheme(palettes, "dark", contrast),
    }


def _css_var(token: str) -> str:
    return "--" + token.replace(".", "-")


def _camel(role: str) -> str:
    parts = role.split("-")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def _format_css_decls(scheme: dict[str, str], indent: str) -> str:
    return "\n".join(f"{indent}{_css_var(k)}: {v};" for k, v in sorted(scheme.items()))


def render_css(theme: Theme) -> str:
    light, dark = theme["light"], theme["dark"]
    header = f"/* Material Design 3 theme — seed: {theme['seed']} | variant: {theme['variant']} | contrast: {theme['contrast']} */"
    return "\n".join([
        header,
        ":root {",
        "  color-scheme: light dark;",
        _format_css_decls(light, "  "),
        "}",
        "",
        "@media (prefers-color-scheme: dark) {",
        "  :root:not([data-theme=\"light\"]) {",
        _format_css_decls(dark, "    "),
        "  }",
        "}",
        "",
        "[data-theme=\"dark\"] {",
        "  color-scheme: dark;",
        _format_css_decls(dark, "  "),
        "}",
        "",
        "[data-theme=\"light\"] {",
        "  color-scheme: light;",
        _format_css_decls(light, "  "),
        "}",
    ])


def render_tailwind(theme: Theme) -> str:
    mappings = "\n".join(
        f"  --color-md-{k.removeprefix('md.sys.color.')}: var({_css_var(k)});"
        for k in sorted(theme["light"])
    )
    return f"{render_css(theme)}\n\n@theme inline {{\n{mappings}\n}}"


COMPOSE_ROLES = (
    "primary", "on-primary", "primary-container", "on-primary-container",
    "inverse-primary", "secondary", "on-secondary", "secondary-container",
    "on-secondary-container", "tertiary", "on-tertiary", "tertiary-container",
    "on-tertiary-container", "background", "on-background", "surface", "on-surface",
    "surface-variant", "on-surface-variant", "surface-tint", "inverse-surface",
    "inverse-on-surface", "error", "on-error", "error-container", "on-error-container",
    "outline", "outline-variant", "scrim", "surface-bright", "surface-dim",
    "surface-container", "surface-container-high", "surface-container-highest",
    "surface-container-low", "surface-container-lowest", "primary-fixed",
    "primary-fixed-dim", "on-primary-fixed", "on-primary-fixed-variant",
    "secondary-fixed", "secondary-fixed-dim", "on-secondary-fixed",
    "on-secondary-fixed-variant", "tertiary-fixed", "tertiary-fixed-dim",
    "on-tertiary-fixed", "on-tertiary-fixed-variant",
)

FLUTTER_ROLE_RENAMES = {"inverse-on-surface": "onInverseSurface"}


def _argb_literal(hex_str: str) -> str:
    return "0xFF" + hex_str.lstrip("#").upper()


def render_compose(theme: Theme) -> str:
    blocks: list[str] = [f"// Material Design 3 ColorScheme — seed: {theme['seed']} ({theme['variant']}, {theme['contrast']})"]
    for scheme, fn_name, val_name in (
        (theme["light"], "lightColorScheme", "LightColorScheme"),
        (theme["dark"], "darkColorScheme", "DarkColorScheme"),
    ):
        lines = [f"    {_camel(role)} = Color({_argb_literal(scheme[f'md.sys.color.{role}'])})," for role in COMPOSE_ROLES]
        blocks.append(f"val {val_name} = {fn_name}(\n" + "\n".join(lines) + "\n)")
    return "\n\n".join(blocks)


def render_flutter(theme: Theme) -> str:
    blocks: list[str] = [f"// Material Design 3 ColorScheme — seed: {theme['seed']} ({theme['variant']}, {theme['contrast']})"]
    for scheme, brightness, var_name in (
        (theme["light"], "Brightness.light", "lightColorScheme"),
        (theme["dark"], "Brightness.dark", "darkColorScheme"),
    ):
        lines = [f"  brightness: {brightness},"]
        for role in COMPOSE_ROLES:
            if role in ("background", "on-background", "surface-variant"):
                continue
            prop = FLUTTER_ROLE_RENAMES.get(role, _camel(role))
            lines.append(f"  {prop}: Color({_argb_literal(scheme[f'md.sys.color.{role}'])}),")
        lines.append(f"  shadow: Color({_argb_literal(scheme['md.sys.color.shadow'])}),")
        blocks.append(f"const {var_name} = ColorScheme(\n" + "\n".join(lines) + "\n);")
    return "\n\n".join(blocks)


RENDERERS: dict[str, Callable[[Theme], str]] = {
    "css": render_css,
    "json": lambda t: json.dumps(t, ensure_ascii=False, indent=2),
    "tailwind": render_tailwind,
    "compose": render_compose,
    "flutter": render_flutter,
}


def audit_theme(theme: Theme) -> tuple[list[AuditRow], int]:
    rows: list[AuditRow] = []
    failures = 0
    modes: tuple[tuple[Literal["light", "dark"], dict[str, str]], ...] = (
        ("light", theme["light"]),
        ("dark", theme["dark"]),
    )
    for mode, scheme in modes:
        for fg_role, bg_role, minimum in AUDIT_PAIRS:
            fg = scheme[f"md.sys.color.{fg_role}"]
            bg = scheme[f"md.sys.color.{bg_role}"]
            ratio = contrast_ratio(fg, bg)
            passed = ratio >= minimum
            if not passed:
                failures += 1
            rows.append({
                "mode": mode, "pair": f"{fg_role} / {bg_role}",
                "fg": fg, "bg": bg, "ratio": round(ratio, 2),
                "min": minimum, "pass": passed,
            })
    return rows, failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", metavar="HEX", help="Brand seed hex color, e.g. #1A73E8")
    parser.add_argument(
        "--variant",
        choices=VARIANTS,
        default=None,
        help="Material 3 dynamic color scheme variant (default: tonal-spot)",
    )
    parser.add_argument(
        "--contrast",
        choices=tuple(CONTRAST_OVERRIDES),
        default=None,
        help="Contrast level (default: standard)",
    )
    parser.add_argument(
        "--format",
        choices=tuple(RENDERERS),
        default="css",
        help="Output format",
    )
    parser.add_argument("--audit", action="store_true", help="Run WCAG 2.1 contrast audit across all semantic color pairs")
    parser.add_argument("--pair", nargs=2, metavar=("FG", "BG"), help="Compute WCAG 2.1 contrast ratio for two hex colors")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.pair is not None:
        if args.seed is not None or args.audit or args.variant is not None or args.contrast is not None:
            parser.error("--pair cannot be combined with --seed, --audit, --variant, or --contrast")
        fg, bg = args.pair
        try:
            ratio = contrast_ratio(fg, bg)
        except ValueError as err:
            parser.error(str(err))
        report = {
            "fg": format_hex(parse_hex(fg)),
            "bg": format_hex(parse_hex(bg)),
            "ratio": round(ratio, 2),
            "aa_large_or_ui": ratio >= 3.0,
            "aa_normal_text": ratio >= 4.5,
            "aaa_normal_text": ratio >= 7.0,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if args.seed is None and (args.variant is not None or args.contrast is not None):
        parser.error("--variant and --contrast require --seed")

    if args.seed is None and not args.audit:
        parser.error("Provide --seed HEX, --audit, or --pair FG BG")

    theme: Theme
    if args.seed is not None:
        try:
            theme = generate_theme(
                args.seed,
                variant=args.variant or "tonal-spot",
                contrast=args.contrast or "standard",
            )
        except ValueError as err:
            parser.error(str(err))
    else:
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        theme = {
            "seed": "baseline",
            "variant": "baseline",
            "contrast": "standard",
            "light": baseline["light"],
            "dark": baseline["dark"],
        }

    if args.audit:
        rows, failures = audit_theme(theme)
        for row in rows:
            status = "PASS" if row["pass"] else "FAIL"
            print(f"[{status}] {row['mode']:5s} {row['pair']:44s} {row['fg']} on {row['bg']}  {row['ratio']:5.2f}:1 (min {row['min']}:1)")
        if failures:
            sys.exit(1)
        return

    print(RENDERERS[args.format](theme))


if __name__ == "__main__":
    main()
