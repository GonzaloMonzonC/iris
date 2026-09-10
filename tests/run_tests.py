#!/usr/bin/env python3
"""🌈 Iris — full test suite (MIT, single command).

Runs every check against a REAL lumen MVM on a throwaway PDB. No external
services, no credentials, no Poli needed — only a lumen M runtime (see
harness/iris_harness.py for how to provide one).

Checks:
  1. INIT seeds the canonical personality (idempotent + force)
  2. IRIS status: active=1, identity_len in range, counts at zero
  3. HYPO creates a hypothesis: speculative=1, purpose=hypothesis, zona=open,
     falsifier and inputs stored
  4. HYPO without falsifier is REJECTED (falsabilidad obligatoria)
  5. HYPO without hypothesis text is rejected
  6. VERDICT plausible keeps it open with status=plausible
  7. VERDICT contradicha moves it to the refuted zone (memoria de refutación)
  8. REFUTED lists the refutation with its contradicting cid
  9. CONTRACT INVARIANT: every open hypothesis carries speculative=1
  10. Identity sync: src/iris.m identity line == personalities/iris.md ASCII
      block; pure ASCII; 600–1400 chars

Usage:  python tests/run_tests.py          (exit 0 = all green)
"""

import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARNESS = ROOT / "harness"
sys.path.insert(0, str(HARNESS))
from iris_harness import _mvm, SRC_ROUTINES  # noqa: E402  (shared loader)

DB = os.path.join(tempfile.gettempdir(), "iris_tests.db")
if os.path.exists(DB):
    os.remove(DB)

FAILURES: list[str] = []


def check(label: str, cond: bool, detail: str = ""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(label)


def run(src: str, expect_ok: bool = True) -> str:
    r = _mvm()(src, routines=SRC_ROUTINES, sqlite_path=DB, gas_limit=200000)
    out = ((r.get("state") or {}).get("output") or "") if isinstance(r, dict) else ""
    ok = r.get("ok") if isinstance(r, dict) else False
    if expect_ok and not ok:
        raise RuntimeError(f"MVM ejecución falló: {src[:80]}… out={out[:200]}")
    return out


print("═══ 1. INIT ═══")
out = run("D INIT^IRIS")
check("INIT siembra (mensaje)", "iris sembrada" in out)
run("D INIT^IRIS")  # idempotente: no debe romper
out = run('W $G(^PERSONALITY("iris","name"))')
check("idempotente (name intacto)", "iris" in out)

print("═══ 2. STATUS ═══")
out = run("D IRIS^IRIS")
check("status activo", "active=1" in out)
check("status versión", "v0.1.0" in out)
check("status counts a cero", "hipotesis_open=0 refuted=0" in out)
m = re.search(r"identity_len=(\d+)", out)
check("identity_len en rango", bool(m) and 600 <= int(m.group(1)) <= 1400, f"len={m.group(1) if m else '?'}")

print("═══ 3. HYPO (contrato speculative) ═══")
out = run('S ^H=$$HYPO^IRIS("Si el eco sube, esperariamos mas adopcion","mecanismo: refuerzo social","medir adopcion en 2 semanas","cid_001") W ^H')
hid = out.strip()
check("HYPO devuelve id", hid.startswith("h_"), f"id={hid}")
out = run(f'W $G(^HYPOTHESIS("{hid}","speculative"))_"/"_$G(^HYPOTHESIS("{hid}","purpose"))_"/"_$G(^HYPOTHESIS("{hid}","zona"))')
check("speculative=1 purpose=hypothesis zona=open", out.strip() == "1/hypothesis/open", out.strip())
out = run(f'W $G(^HYPOTHESIS("{hid}","falsifier"))')
check("falsifier almacenado", "2 semanas" in out)
out = run('S ^H2=$$HYPO^IRIS("Hipotesis con inputs","","experimento X","cid_abc,cid_def") W ^H2')
hid2 = out.strip()
out = run(f'W $G(^HYPOTHESIS("{hid2}","inputs"))')
check("inputs (cids) almacenados", "cid_abc,cid_def" in out)

print("═══ 4/5. RECHAZOS (falsabilidad obligatoria) ═══")
out = run('W $$HYPO^IRIS("Hipotesis sin como matarla","","","")')
check("sin falsificador → rechazada", "rechazada:sin_falsificador" in out, out.strip())
out = run('W $$HYPO^IRIS("","","experimento Y","")')
check("sin texto → rechazada", "rechazada:sin_hipotesis" in out, out.strip())

print("═══ 6. VERDICT plausible ═══")
out = run(f'S ^R=$$VERDICT^IRIS("{hid}","plausible","cid_111") W ^R_"/"_$G(^HYPOTHESIS("{hid}","status"))')
check("plausible queda open", "ok/plausible" in out, out.strip())

print("═══ 7/8. VERDICT contradicha → memoria de refutación ═══")
out = run(f'S ^R=$$VERDICT^IRIS("{hid2}","contradicha","cid_999") W ^R')
check("contradicha ok", "ok" in out)
out = run(f'W $G(^HYPOTHESIS("{hid2}","zona"))')
check("zona pasa a refuted", out.strip() == "refuted", out.strip())
out = run("D REFUTED^IRIS")
check("REFUTED lista la refutación", hid2 in out and "cid_999" in out)
out = run(f'W $G(^HYPOTHESIS("{hid2}","contradice"))')
check("cid contradictorio archivado", "cid_999" in out)
out = run("D LIST^IRIS")
check("LIST ya no la muestra", hid2 not in out)

print("═══ 9. INVARIANTE DEL CONTRATO ═══")
out = run(
    'N id,bad S id=$O(^HYPOTHESIS("")) S bad=0 ' +
    'F  Q:id=""  D' + "\n" +
    '. I $G(^HYPOTHESIS(id,"zona"))="open" D' + "\n" +
    '. . I $G(^HYPOTHESIS(id,"speculative"))\'="1" S bad=bad+1' + "\n" +
    '. S id=$O(^HYPOTHESIS(id))' + "\n" +
    'W "sin_speculative=",bad'
)
check("toda hipótesis abierta lleva speculative=1", "sin_speculative=0" in out, out.strip())

print("═══ 10. IDENTITY SYNC ═══")
src_text = (ROOT / "src" / "iris.m").read_text(encoding="utf-8")
md_text = (ROOT / "personalities" / "iris.md").read_text(encoding="utf-8")
m = re.search(r'D SETIF\^IRIS\("identity","([^"]+)"\)', src_text)
identity = m.group(1) if m else ""
check("identity extraída de src/iris.m", bool(identity))
check("identity ASCII puro", identity.isascii(), repr(identity[:60]))
check("identity en rango 600-1400", 600 <= len(identity) <= 1400, f"len={len(identity)}")
check("sync src ↔ personalities/iris.md", identity in md_text)

print()
if FAILURES:
    print(f"❌ {len(FAILURES)} FALLOS: {FAILURES}")
    sys.exit(1)
print("🎉 TODO VERDE — Iris lista para cerrar ciclo")
