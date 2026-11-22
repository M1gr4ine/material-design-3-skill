"""Find a Material 3 component card, query official tokens, or resolve token aliases. Python 3."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TOKENS_DIR = ASSETS / "tokens"
REFERENCES_DIR = ROOT / "references"

# Chinese names, synonyms, and non-trivial shorthands (simple singular/plural handled by resolve_slug).
ALIASES = {
    # Search & app bars
    "搜索": "search", "搜索栏": "search", "搜索条": "search", "搜索框": "search",
    "searchbar": "search", "search-bar": "search", "search-view": "search",
    "应用栏": "app-bars", "顶部应用栏": "app-bars", "顶部栏": "app-bars",
    "appbar": "app-bars", "top-app-bar": "app-bars", "topbar": "app-bars", "header": "app-bars",
    # Toolbars & menus
    "工具栏": "toolbars", "底部应用栏": "toolbars", "bottom-app-bar": "toolbars",
    "菜单": "menus", "右键菜单": "menus", "下拉菜单": "menus",
    "dropdown": "menus", "context-menu": "menus",
    # Buttons & FABs
    "按钮": "buttons", "btn": "buttons",
    "图标按钮": "icon-buttons", "iconbutton": "icon-buttons",
    "按钮组": "button-groups",
    "分裂按钮": "split-button", "split": "split-button", "splitbutton": "split-button",
    "分段按钮": "segmented-buttons", "segmented": "segmented-buttons",
    "悬浮按钮": "floating-action-button", "悬浮操作按钮": "floating-action-button",
    "fab": "floating-action-button",
    "扩展悬浮按钮": "extended-fab", "extended": "extended-fab",
    "悬浮菜单": "fab-menu", "悬浮操作菜单": "fab-menu",
    # Navigation
    "导航栏": "navigation-bar", "底部导航": "navigation-bar",
    "navbar": "navigation-bar", "bottom-nav": "navigation-bar",
    "导航轨": "navigation-rail", "侧边导航": "navigation-rail", "rail": "navigation-rail",
    "抽屉": "navigation-drawer", "导航抽屉": "navigation-drawer",
    "drawer": "navigation-drawer", "sidebar": "navigation-drawer",
    "页签": "tabs", "标签页": "tabs", "选项卡": "tabs",
    # Content & containment
    "列表": "lists",
    "卡片": "cards",
    "轮播": "carousel", "走马灯": "carousel",
    "分隔线": "divider", "分割线": "divider", "hr": "divider",
    "底部面板": "bottom-sheets",
    "侧面板": "side-sheets", "侧边面板": "side-sheets",
    "对话框": "dialogs", "弹窗": "dialogs", "modal": "dialogs",
    # Inputs & selection
    "文本框": "text-fields", "文本字段": "text-fields", "输入框": "text-fields",
    "textfield": "text-fields", "input": "text-fields",
    "日期选择器": "date-pickers", "日期": "date-pickers", "date": "date-pickers",
    "datepicker": "date-pickers",
    "时间选择器": "time-pickers", "时间": "time-pickers", "time": "time-pickers",
    "timepicker": "time-pickers",
    "复选框": "checkbox", "多选框": "checkbox",
    "单选": "radio-button", "单选按钮": "radio-button", "radio": "radio-button",
    "开关": "switch", "toggle": "switch",
    "滑块": "sliders", "滑动条": "sliders",
    "标签": "chips", "标签控件": "chips",
    # Feedback & progress
    "徽标": "badges", "徽章": "badges", "角标": "badges",
    "短消息": "snackbar", "轻提示": "snackbar", "toast": "snackbar",
    "工具提示": "tooltips", "提示": "tooltips",
    "加载": "loading-indicator", "加载指示器": "loading-indicator", "loading": "loading-indicator",
    "进度条": "progress-indicators", "进度指示器": "progress-indicators",
    "progress": "progress-indicators",
}


@dataclass(frozen=True)
class ResolveOptions:
    theme: str = "both"
    motion: str = "both"


class SystemCatalog:
    """Lazy-loaded offline system token registry (colors, metrics, typography, motion)."""

    def __init__(self) -> None:
        self.colors: dict[str, Any] = json.loads((ASSETS / "baseline-colors.json").read_text(encoding="utf-8"))
        self.metrics: dict[str, Any] = json.loads((ASSETS / "metrics.json").read_text(encoding="utf-8"))["tokens"]
        self.typescale: dict[str, Any] = json.loads((ASSETS / "type-scale.json").read_text(encoding="utf-8"))
        self.motion: dict[str, Any] = json.loads((ASSETS / "motion.json").read_text(encoding="utf-8"))
        self._comp_tokens: dict[str, Any] | None = None

    def all_component_tokens(self) -> dict[str, Any]:
        if self._comp_tokens is None:
            merged: dict[str, Any] = {}
            for path in sorted(TOKENS_DIR.glob("*.json")):
                merged.update(json.loads(path.read_text(encoding="utf-8"))["tokens"])
            self._comp_tokens = merged
        return self._comp_tokens

    def lookup_system(self, token: str, opts: ResolveOptions) -> tuple[bool, Any]:
        if token in self.colors["light"] or token in self.colors["dark"]:
            if opts.theme == "light":
                return True, self.colors["light"].get(token)
            if opts.theme == "dark":
                return True, self.colors["dark"].get(token)
            return True, {"light": self.colors["light"].get(token), "dark": self.colors["dark"].get(token)}
        if token in self.colors.get("referenceTones", {}):
            return True, self.colors["referenceTones"][token]
        if token in self.metrics:
            return True, self.metrics[token]
        if token in self.typescale["styles"]:
            return True, self.typescale["styles"][token]
        if token in self.typescale.get("weights", {}):
            return True, self.typescale["weights"][token]
        if token.startswith("md.sys.typescale."):
            base, _, field = token.rpartition(".")
            style = self.typescale["styles"].get(base)
            if style is not None and field in style:
                return True, style[field]
        return self._lookup_motion(token, opts)

    def _lookup_motion(self, token: str, opts: ResolveOptions) -> tuple[bool, Any]:
        schemes = self.motion["schemes"]
        suffixes: dict[str, str] = self.motion.get("scalarSuffixes", {})
        base = token
        scalar_field: str | None = None
        for suffix, field in suffixes.items():
            if token.endswith(suffix):
                base = token[: -len(suffix)]
                scalar_field = field
                break
        if base not in schemes["expressive"] and base not in schemes["standard"]:
            return False, None

        def extract(scheme_name: str) -> Any:
            entry = schemes[scheme_name].get(base)
            if entry is None:
                return None
            return entry[scalar_field] if scalar_field else entry

        if opts.motion in ("expressive", "standard"):
            return True, extract(opts.motion)
        return True, {"expressive": extract("expressive"), "standard": extract("standard")}

    def search_system(self, query: str, opts: ResolveOptions) -> dict[str, Any]:
        needle = query.casefold()
        results: dict[str, Any] = {}
        keys: list[str] = sorted(
            set(self.colors["light"])
            | set(self.colors["dark"])
            | set(self.colors.get("referenceTones", {}))
            | set(self.metrics)
            | set(self.typescale["styles"])
            | set(self.typescale.get("weights", {}))
            | set(self.motion["schemes"]["expressive"])
            | set(self.motion["schemes"]["standard"])
        )
        for key in keys:
            if needle in key.casefold():
                found, value = self.lookup_system(key, opts)
                if found:
                    results[key] = value
        return results

    def resolve_value(self, value: Any, opts: ResolveOptions, seen: frozenset[str] = frozenset()) -> Any:
        if isinstance(value, str):
            return self._resolve_alias(value, opts, seen)
        if isinstance(value, dict):
            for wrapper in ("byContext", "type"):
                sub = value.get(wrapper)
                if isinstance(sub, dict):
                    return {wrapper: {k: self.resolve_value(v, opts, seen) for k, v in sub.items()}}
        return value

    def _resolve_alias(self, token: str, opts: ResolveOptions, seen: frozenset[str]) -> Any:
        if not token.startswith("md.") or token in seen:
            return token
        found, sys_val = self.lookup_system(token, opts)
        if found:
            return {"alias": token, "value": sys_val}
        comp_val = self.all_component_tokens().get(token)
        if comp_val is not None:
            resolved = self.resolve_value(comp_val, opts, seen | {token})
            return {"alias": token, "resolved": resolved}
        return token


def component_title(slug: str) -> str:
    with (REFERENCES_DIR / f"{slug}.md").open(encoding="utf-8") as card:
        return card.readline().lstrip("# ").strip()


def resolve_slug(raw_query: str, slugs: list[str]) -> tuple[str | None, list[str]]:
    query = raw_query.casefold().strip()
    normalized = query.replace(" ", "-").replace("_", "-")
    for candidate in (query, normalized):
        mapped = ALIASES.get(candidate, candidate)
        if mapped in slugs:
            return mapped, [mapped]
        if mapped + "s" in slugs:
            return mapped + "s", [mapped + "s"]
        if mapped.endswith("s") and mapped[:-1] in slugs:
            return mapped[:-1], [mapped[:-1]]
    matches = [
        name for name in slugs
        if normalized in name or query in component_title(name).casefold()
    ]
    if len(matches) == 1:
        return matches[0], matches
    return None, matches


def _find_tokens(slug: str, needle: str, catalog: SystemCatalog | None, opts: ResolveOptions) -> dict[str, Any]:
    data = json.loads((TOKENS_DIR / f"{slug}.json").read_text(encoding="utf-8"))["tokens"]
    hits = {key: value for key, value in data.items() if needle in key.casefold()}
    if catalog is not None:
        return {key: catalog.resolve_value(value, opts) for key, value in hits.items()}
    return hits


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", nargs="?", help="Component ID, Chinese name or English name")
    query_group = parser.add_mutually_exclusive_group()
    query_group.add_argument("--token", metavar="TEXT", help="Search component tokens containing TEXT (omit name for global search)")
    query_group.add_argument("--sys", metavar="TEXT", help="Search system tokens (colors, metrics, typography, motion)")
    parser.add_argument("--resolve", action="store_true", help="Recursively resolve md.* aliases to concrete values")
    parser.add_argument("--theme", choices=("both", "light", "dark"), default="both", help="Color theme for --resolve or --sys")
    parser.add_argument("--motion", choices=("both", "expressive", "standard"), default="both", help="Motion scheme for --resolve or --sys")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    slugs = sorted(path.stem for path in TOKENS_DIR.glob("*.json"))
    opts = ResolveOptions(theme=args.theme, motion=args.motion)

    if args.resolve and args.token is None:
        parser.error("--resolve requires --token")

    if args.sys is not None:
        if args.name is not None:
            parser.error("--sys cannot be combined with a component name")
        found = SystemCatalog().search_system(args.sys, opts)
        if not found:
            parser.error(f"No matching system token for {args.sys!r}")
        print(json.dumps(found, ensure_ascii=False, indent=2))
        return

    if args.name is None and args.token is None:
        for slug in slugs:
            print(slug, component_title(slug), sep="  ")
        return

    catalog = SystemCatalog() if args.resolve else None

    if args.name is None and args.token is not None:
        needle = args.token.casefold()
        grouped = {
            slug: hits
            for slug in slugs
            if (hits := _find_tokens(slug, needle, catalog, opts))
        }
        if not grouped:
            parser.error(f"No matching token across components for {args.token!r}")
        print(json.dumps(grouped, ensure_ascii=False, indent=2))
        return

    slug, matches = resolve_slug(args.name, slugs)
    if slug is None:
        hint = ", ".join(matches) or "none. Run without a name to list all."
        parser.error(f"Choose one component. Matches: {hint}")

    if args.token is None:
        card = REFERENCES_DIR / f"{slug}.md"
        print(card.read_text(encoding="utf-8"), end="")
        return

    found = _find_tokens(slug, args.token.casefold(), catalog, opts)
    if not found:
        parser.error("No matching token in " + slug)
    print(json.dumps(found, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
