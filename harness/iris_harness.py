#!/usr/bin/env python3
"""🌈 Iris harness — connect the creative agent to LUMEN (MIT).

Modes (run what you have):

  1. STATUS  — run IRIS^IRIS against any lumen-m-light MVM. Prints identity
               status + hipotesis counts.
  2. SEED    — INIT^IRIS on the throwaway PDB (fills only missing; use
               --force to overwrite).
  3. NEW     — create a hypothesis: --text, --falsifier (required), optional
               --mech, --inputs (comma-separated cids).
  4. LIST    — list open hypotheses.
  5. VERDICT — register Astrid's verdict on a hypothesis: --id, --verdict
               (insuficiente|plausible|contradicha), optional --cid.
               "contradicha" moves it to the refutation memory.
  6. REFUTED — list the refutation memory.

Requirements: a lumen M runtime to execute the M routines. Two options:
  1. local lumen-protocol clone (https://github.com/GonzaloMonzonC/lumen-protocol)
     with the Rust MVM built (`cargo build --release` → lumen_mlight.dll,
     copied to implementations/mcp-servers/pdb/), or
  2. `LUMEN_MLIGHT_LIB` pointing at an existing lumen_mlight.dll.

Usage:
    python iris_harness.py status
    python iris_harness.py seed [--force]
    python iris_harness.py new --text "si X, esperariamos Y" --falsifier "experimento Z"
    python iris_harness.py list
    python iris_harness.py verdict --id h_... --verdict contradicha --cid df1231b4
    python iris_harness.py refuted
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_ROUTINES = {
    "IRIS": (ROOT / "src" / "iris.m").read_text(encoding="utf-8"),
}


def _mvm() -> object:
    """Load the lumen m-light python wrapper (published lumen-mcp or local clone)."""
    try:
        from lumen_mlight import execute  # published/local wrapper

        return execute
    except ImportError:
        pass
    here = Path(__file__).resolve()
    for cand in here.parents:
        p = cand / "lumen-protocol" / "implementations" / "mcp-servers" / "pdb"
        if (p / "lumen_mlight.py").exists():
            sys.path.insert(0, str(p))
            from lumen_mlight import execute  # type: ignore

            return execute
    raise SystemExit(
        "No lumen-mcp found. Install `pip install lumen-mcp` or clone lumen-protocol "
        "next to this repo (https://github.com/GonzaloMonzonC/lumen-protocol)."
    )


def _run(execute, src: str, db: str):
    r = execute(src, routines=SRC_ROUTINES, sqlite_path=db, gas_limit=100000)
    out = ((r.get("state") or {}).get("output") or "") if isinstance(r, dict) else ""
    print(out.strip() or r)
    return r


def _m_escape(s: str) -> str:
    return s.replace('"', '""')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["status", "seed", "new", "list", "verdict", "refuted"])
    ap.add_argument("--text", default="", help="hypothesis text (new)")
    ap.add_argument("--falsifier", default="", help="experiment that could kill it (new, required)")
    ap.add_argument("--mech", default="", help="causal mechanism, conjecture (new)")
    ap.add_argument("--inputs", default="", help="comma-separated cids from Astrid (new)")
    ap.add_argument("--id", default="", help="hypothesis id (verdict)")
    ap.add_argument("--verdict", default="", help="insuficiente|plausible|contradicha (verdict)")
    ap.add_argument("--cid", default="", help="evidence cid (verdict)")
    ap.add_argument("--force", action="store_true", help="seed: overwrite/reset (INIT(1))")
    ap.add_argument("--db", default=os.path.join(os.environ.get("TEMP", "."), "iris_pdb.db"))
    args = ap.parse_args()

    execute = _mvm()
    if args.mode == "status":
        _run(execute, "D IRIS^IRIS", args.db)
    elif args.mode == "seed":
        _run(execute, "D INIT^IRIS(" + ("1" if args.force else "0") + ")", args.db)
    elif args.mode == "new":
        src = (
            f'S ^R=$$HYPO^IRIS("{_m_escape(args.text)}","{_m_escape(args.mech)}",'
            f'"{_m_escape(args.falsifier)}","{_m_escape(args.inputs)}") W ^R'
        )
        _run(execute, src, args.db)
    elif args.mode == "list":
        _run(execute, "D LIST^IRIS", args.db)
    elif args.mode == "verdict":
        src = (
            f'S ^R=$$VERDICT^IRIS("{_m_escape(args.id)}","{_m_escape(args.verdict)}",'
            f'"{_m_escape(args.cid)}") W ^R'
        )
        _run(execute, src, args.db)
    elif args.mode == "refuted":
        _run(execute, "D REFUTED^IRIS", args.db)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
