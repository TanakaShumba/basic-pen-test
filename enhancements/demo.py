#!/usr/bin/env python3
"""
Demo module (educational & defensive) for recruiters.
"""
from __future__ import annotations
import argparse, json, logging, re
from pathlib import Path
from typing import List, Tuple, Dict
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
_LOG = logging.getLogger("demo")
SUSPICIOUS_PATTERNS = [
    r"failed login",
    r"invalid credentials",
    r"authentication error",
    r"sql syntax",
    r"unauthorized",
]
def load_lines(path: Path) -> List[str]:
    if not path.exists():
        _LOG.warning("sample.log not found at %s; returning empty list", path)
        return []
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()
def detect_suspicious(lines: List[str], patterns: List[str]) -> List[Tuple[int, str, str]]:
    compiled = [re.compile(pat, re.IGNORECASE) for pat in patterns]
    results: List[Tuple[int, str, str]] = []
    for i, line in enumerate(lines, start=1):
        for cp in compiled:
            if cp.search(line):
                results.append((i, cp.pattern, line.strip()))
                break
    return results
def summarize(matches: List[Tuple[int, str, str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for _, pattern, _ in matches:
        counts[pattern] = counts.get(pattern, 0) + 1
    return counts
def write_report(path: Path, summary: Dict[str, int], matches: List[Tuple[int, str, str]]) -> None:
    report = {"summary": summary, "matches": [{"line": ln, "pattern": pat, "text": txt} for ln, pat, txt in matches]}
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    _LOG.info("Report written to %s", path)
def main() -> int:
    parser = argparse.ArgumentParser(description="Safe demo: parse a local log for suspicious patterns and write a report.")
    parser.add_argument("--log", "-l", default="sample.log", help="Path to sample log (local only)")
    parser.add_argument("--out", "-o", default="demo_report.json", help="Output JSON report file")
    args = parser.parse_args()
    log_path = Path(args.log)
    out_path = Path(args.out)
    lines = load_lines(log_path)
    matches = detect_suspicious(lines, SUSPICIOUS_PATTERNS)
    summary = summarize(matches)
    write_report(out_path, summary, matches)
    print(json.dumps({"status": "ok", "total_matches": len(matches), "report": str(out_path)}))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())

