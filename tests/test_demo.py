from pathlib import Path
from enhancements.demo import load_lines, detect_suspicious, summarize
def test_demo_flow(tmp_path):
    p = tmp_path / "sample.log"
    p.write_text(\"Info: all good\nFailed login for user root\nAuthentication error at 10.0.0.1\n\")
    lines = load_lines(p)
    matches = detect_suspicious(lines, [\"failed login\", \"authentication error\"])
    summary = summarize(matches)
    assert isinstance(summary, dict)
    assert sum(summary.values()) == len(matches)

