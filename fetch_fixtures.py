#!/usr/bin/env python3
"""Fetch today's football fixtures and write a small JSON the screensaver reads.

Run from GitHub Actions every 20 minutes; the API key comes from the repository secrets and is
never written to the file.
"""
import datetime
import json
import os
import pathlib
import sys
import urllib.request

TIMEZONE = "Asia/Riyadh"
URL = "https://v3.football.api-sports.io/fixtures?date=%s&timezone=%s"
ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
ARCHIVE = DOCS / "archive"


def today() -> str:
    tz = datetime.timezone(datetime.timedelta(hours=3))
    return datetime.datetime.now(tz).date().isoformat()


def fetch(day: str) -> list:
    key = os.environ.get("API_FOOTBALL_KEY", "").strip()
    if not key:
        sys.exit("API_FOOTBALL_KEY is missing")
    request = urllib.request.Request(URL % (day, TIMEZONE), headers={
        "x-apisports-key": key,
        "User-Agent": "prayer-screen/1.0",
    })
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    if data.get("errors"):
        sys.exit("API error: %s" % data["errors"])
    return data.get("response", [])


def compact(fixtures: list) -> list:
    out = []
    for item in fixtures:
        league = item["league"]
        teams = item["teams"]
        status = item["fixture"]["status"]
        goals = item["goals"]
        out.append({
            "l": league["id"],
            "n": league["name"],
            "h": teams["home"]["name"],
            "a": teams["away"]["name"],
            "s": status["short"],
            "e": status.get("elapsed"),
            "gh": goals["home"],
            "ga": goals["away"],
            "t": item["fixture"]["date"],
        })
    return out


def main() -> None:
    day = today()
    rows = compact(fetch(day))
    document = {
        "date": day,
        "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "count": len(rows),
        "fixtures": rows,
    }
    DOCS.mkdir(exist_ok=True)
    ARCHIVE.mkdir(exist_ok=True)
    text = json.dumps(document, ensure_ascii=False, separators=(",", ":"))
    (DOCS / "latest.json").write_text(text, encoding="utf-8")
    (ARCHIVE / ("%s.json" % day)).write_text(text, encoding="utf-8")
    print("wrote %d fixtures for %s (%d KB)" % (len(rows), day, len(text.encode()) // 1024))


if __name__ == "__main__":
    main()
