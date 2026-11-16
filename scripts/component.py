"""Find a Material 3 recipe or matching official component tokens. Python 3."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIASES = {
    "搜索条": "search", "搜索框": "search", "searchbar": "search",
    "toolbar": "toolbars", "底部应用栏": "toolbars", "顶部应用栏": "app-bars",
    "悬浮按钮": "floating-action-button", "fab": "floating-action-button",
    "页签": "tabs", "标签页": "tabs", "复选框": "checkbox",
    "文本框": "text-fields", "输入框": "text-fields", "进度条": "progress-indicators",
    "开关": "switch", "抽屉": "navigation-drawer", "右键菜单": "menus",
}


def component_title(slug):
    with (ROOT / "references" / (slug + ".md")).open(encoding="utf-8") as card:
        return card.readline().lstrip("# ").strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", nargs="?", help="Component ID, Chinese name or English name")
    parser.add_argument("--token", metavar="TEXT", help="Print token names and values containing TEXT")
    args = parser.parse_args()
    directory = ROOT / "assets" / "tokens"
    slugs = sorted(path.stem for path in directory.glob("*.json"))

    if args.name is None:
        if args.token is not None:
            parser.error("--token requires a component name")
        for slug in slugs:
            print(slug, component_title(slug), sep="  ")
        return

    query = args.name.casefold().strip()
    slug = ALIASES.get(query, query)
    if slug not in slugs:
        matches = [name for name in slugs if query in name or query in component_title(name).casefold()]
        if len(matches) != 1:
            parser.error("Choose one component. Matches: " + (", ".join(matches) or "none. Run without a name to list all."))
        slug = matches[0]
    if args.token is None:
        card = ROOT / "references" / (slug + ".md")
        print(card.read_text(encoding="utf-8"), end="")
        return

    data = json.loads((directory / (slug + ".json")).read_text(encoding="utf-8"))["tokens"]
    needle = args.token.casefold()
    found = {key: value for key, value in data.items() if needle in key}
    if not found:
        parser.error("No matching token in " + slug)
    print(json.dumps(found, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
