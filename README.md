# Iris

**Iris splits the light of evidence into a rainbow of possibilities — never claiming any of them is real.**

Iris is the **hypothesis agent** of the Cadences Lab research team. It works alongside [Astrid](https://github.com/GonzaloMonzonC/astrid):

- **Astrid** finds, anchors and verifies facts (claims with source, CID, HMAC signature — *"evidence on record, or silence"*).
- **Iris** imagines what those facts could mean: falsifiable causal hypotheses, counterfactuals, and experiments able to kill them — always labelled `speculative=1`, never presented as claims.

> One demands evidence. The other generates hypotheses that evidence can support or kill. That is a research team.

## The contract in one sentence

Iris **does not assert**. It only proposes: *"I'm not claiming it. But if it were true, this is how we'd show it."*

Every Iris hypothesis is falsifiable by design (no experiment able to kill it ⇒ noise), and every promotion to evidence is decided by Astrid — never by Iris.

## Usage

```bash
python tests/run_tests.py                        # full suite (exit 0 = green)
python harness/iris_harness.py status            # personality status
python harness/iris_harness.py seed              # seed ^PERSONALITY("iris")
python harness/iris_harness.py new \
    --text "If X, we would expect Y" \
    --falsifier "measure Z within two weeks"     # create a hypothesis
python harness/iris_harness.py list              # open hypotheses
python harness/iris_harness.py verdict --id h_... --verdict contradicha --cid df1231b4
python harness/iris_harness.py refuted           # refutation memory
```

## Layout

| Path | Content |
|---|---|
| `src/iris.m` | The M routine: personality + hypothesis contract (M-Light, no external deps) |
| `personalities/iris.md` | Human-readable personality (canonical ASCII identity + fact sheet) |
| `harness/iris_harness.py` | Connects Iris to a lumen MVM runtime (status/seed/new/list/verdict/refuted) |
| `tests/run_tests.py` | Full suite against a real MVM (throwaway PDB, no external services) |
| `docs/HYPOTHESIS_SCHEMA.md` | The `speculative` contract (schema v1) |
| `DESIGN.md` | Design & role: free creative agent, ecosystem steward, with Astrid's evidence counsel |

## Requirements

A lumen MVM runtime: clone [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) next to this repo (recommended) or install `lumen-mcp` + point `LUMEN_MLIGHT_LIB` at your `lumen_mlight.dll`/`.so`.

## Status

**v0.1.0** — personality + hypothesis contract + green suite (15 checks). Iris also lives as an ecosystem agent (`mode: iris` in Poli, routing `^AGENTES("routing","iris")`).

## License

MIT — Copyright (c) 2026 Gonzalo Monzón · Cadences Lab
