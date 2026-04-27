"""OpenAI API caller via OpenAI-API-simple.sh (RCIFENI-O)."""
import json
import subprocess
import time

SCRIPT = "/home/fong/Projects/ICE-2026-HUIT/.fong/scripts/OpenAI-API-simple.sh"


def call_llm(role, context, instructions, fmt, inp, okr,
             notices="", example=""):
    """Call GPT-4o-mini via OpenAI-API-simple.sh with RCIFENI-O params.
    Returns (parsed_dict, duration_seconds).
    """
    cmd = [
        SCRIPT,
        "-r", role,
        "-c", context,
        "-i", instructions,
        "-f", fmt,
        "-I", inp,
        "-o", okr,
    ]
    if notices:
        cmd.extend(["-n", notices])
    if example:
        cmd.extend(["-e", example])

    t0 = time.time()
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=120
    )
    dur = time.time() - t0

    if result.returncode != 0:
        raise RuntimeError(f"API error: {result.stderr[:200]}")

    # Skip timing header line, parse content
    lines = result.stdout.strip().split("\n")
    content_lines = [l for l in lines if not l.startswith("⏱️") and l != "---"]
    raw = "\n".join(content_lines).strip()
    return raw, dur


def parse_response(raw):
    """Parse JSON response from LLM."""
    import re
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        d = json.loads(m.group()) if m else {}

    label_map = {
        "confirmed_greenwashing": "confirmed",
        "suspected_greenwashing": "suspected",
        "confirmed": "confirmed", "suspected": "suspected",
        "clean": "clean", "not_greenwashing": "clean",
    }
    raw_label = d.get("label", "suspected").lower().strip()
    label = label_map.get(raw_label, "suspected")
    conf = max(0.1, min(0.99, float(d.get("confidence", 0.5))))
    reasoning = d.get("reasoning", "")[:300]
    scores = d.get("scores", {})
    return label, conf, reasoning, scores
