"""
Hybrid artist parser:
  1. Split title on common delimiters (、× + ｜ feat. ft. &)
  2. Match each segment against known artists in artists.yaml
  3. Return only matched artist names

Unknown artists (not in yaml) are silently skipped.
Add new artists to artists.yaml to make them discoverable.
"""

import re
from pathlib import Path

import yaml

_YAML_PATH = Path(__file__).parent / "artists.yaml"

# Delimiters that separate multiple performers in a title.
# Order matters: longer patterns first.
_DELIMITER_PATTERN = re.compile(
    r"feat\.|ft\.|、|×|＋|\+|｜|\||&|／|/",
    re.IGNORECASE,
)

# Noise suffixes that appear after an artist name in a segment,
# e.g. "Triple Deer (Special Guest)" → strip the parenthetical
_NOISE_PATTERN = re.compile(r"[\(（].*?[\)）]")


def _normalize(text: str) -> str:
    text = _NOISE_PATTERN.sub("", text)
    return text.strip().lower()


class ArtistParser:
    def __init__(self, yaml_path: Path = _YAML_PATH) -> None:
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        raw: list[str] = data.get("artists", [])
        # Build lookup: normalized → original name (for returning clean names)
        self._lookup: dict[str, str] = {_normalize(a): a for a in raw}

    def parse(self, title: str) -> list[str]:
        """
        Extract known artist names from a FANSI GO event title.

        Strategy:
        - Split on delimiters to get candidate segments
        - For each segment, check if any known artist name is contained within it
        - Return matched original names (deduplicated, order preserved)
        """
        segments = _DELIMITER_PATTERN.split(title)
        found: list[str] = []
        seen: set[str] = set()

        for segment in segments:
            seg_normalized = _normalize(segment)
            if not seg_normalized:
                continue
            # Check if any known artist appears in this segment
            for known_normalized, original_name in self._lookup.items():
                if known_normalized in seg_normalized and original_name not in seen:
                    found.append(original_name)
                    seen.add(original_name)

        return found
