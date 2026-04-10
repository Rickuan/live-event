"""
Known Taiwan live music venue lookup.

Maps venue name (as it appears on FANSI GO) to (city, address).
Used by the scraper when city/address is not available in the listing HTML.

To add a new venue: append to KNOWN_VENUES.
If a venue is not found, the scraper falls back to city="台灣", address=None.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VenueInfo:
    city: str
    address: str | None = None

# TODO: 補上地址, 刪除已歇業地點
# fmt: off
KNOWN_VENUES: dict[str, VenueInfo] = {
    # 台北
    "PIPE Live Music":          VenueInfo("台北", "台北市中山區樂群三路200號"),
    "The Wall":                 VenueInfo("台北", "台北市中正區羅斯福路四段200號B1"),
    "Legacy Taipei":            VenueInfo("台北", "台北市中正區八德路一段1號"),
    "女巫店":                   VenueInfo("台北", "台北市大安區新生南路三段55巷7號"),
    "地下社會":                 VenueInfo("台北", "台北市大安區新生南路三段55巷7號"),
    "河岸留言 西門紅樓":        VenueInfo("台北", "台北市萬華區成都路10號"),
    "河岸留言 公館":            VenueInfo("台北", "台北市中正區羅斯福路四段210號"),
    "Revolver":                 VenueInfo("台北", "台北市大安區復興南路一段1號"),
    "海邊的卡夫卡":             VenueInfo("台北", "台北市大安區復興南路一段243巷13號"),
    "西門紅樓":                 VenueInfo("台北", "台北市萬華區成都路10號"),
    "ATT SHOW BOX":             VenueInfo("台北", "台北市信義區松壽路12號"),
    "Clap Taipei":              VenueInfo("台北"),
    "Kraftwerk Taipei":         VenueInfo("台北"),
    "百樂門酒館":               VenueInfo("台北"),
    "卡米地喜劇俱樂部":         VenueInfo("台北"),
    "台北流行音樂中心":         VenueInfo("台北", "台北市南港區市民大道八段99號"),
    "Zeelandia":                VenueInfo("台北"),
    "Brickyard 33":             VenueInfo("台北"),
    "好地下":                   VenueInfo("台北"),

    # 台中
    "Legacy Taichung":          VenueInfo("台中"),
    "原來酒廠":                 VenueInfo("台中"),

    # 高雄
    "Legacy Kaohsiung":         VenueInfo("高雄"),
    "駁二藝術特區":             VenueInfo("高雄", "高雄市鹽埕區大勇路1號"),
    "The dome of Light":        VenueInfo("高雄"),

    # 台南
    "好好 LiveHouse":           VenueInfo("台南"),
}
# fmt: on

_NORMALIZED: dict[str, VenueInfo] = {k.strip().lower(): v for k, v in KNOWN_VENUES.items()}


def lookup(venue_name: str) -> VenueInfo:
    """Return VenueInfo for a known venue, or a default if not found."""
    return _NORMALIZED.get(venue_name.strip().lower(), VenueInfo("台灣", None))
