from pathlib import Path
import yaml

from scraper.base import EventRaw

_YAML_PATH = Path(__file__).parent / "whitelist.yaml"


class WhitelistFilter:
    def __init__(self, yaml_path: Path = _YAML_PATH) -> None:
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self._keywords: list[str] = [kw.lower() for kw in data.get("keywords", [])]

    def matches(self, event: EventRaw) -> bool:
        text = event.searchable_text
        return any(kw in text for kw in self._keywords)

    def filter(self, events: list[EventRaw]) -> list[EventRaw]:
        return [e for e in events if self.matches(e)]
