# Changelog — Iris

Todos los cambios notables se documentan aquí. Formato basado en [Keep a Changelog](https://keepachangelog.com/), semver.

## [0.1.2] — 2026-09-11

### Added
- 🌈 **Landing — [iris.cadences.app](https://iris.cadences.app)**: single-file (EN/ES),
  su personaje y *su realidad sobre LUMEN* (el patio de juegos: zonas, memoria de
  refutación, el digest de Astrid en su mesa), OG, favicon; cross-links de la tríada.

### Docs
- README (+ ES): 🌐 landing link.

## [0.1.1] — 2026-09-10

### Docs
- README (+ ES): **la tríada se completa** — Elena referenciada junto a Astrid
  (frase de equipo + bullet *"cierra el ciclo"* en la lista de roles).

## [0.1.0] — 2026-09-10

### Added
- `src/iris.m` — rutina M: personalidad (INIT/SEED/SETIF) + contrato de hipótesis:
  `HYPO` (crea, falsificador obligatorio), `LIST`, `VERDICT` (abridora/plausible/contradicha),
  `REFUTED` (memoria de refutación por zona), `COUNT`, `NOW`.
- `personalities/iris.md` — personalidad legible: identidad canónica ASCII, ficha, 6 reglas críticas, 7 capacidades.
- `harness/iris_harness.py` — conexión a un runtime lumen MVM: modos status/seed/new/list/verdict/refuted.
- `tests/run_tests.py` — suite completa contra MVM real (15 checks): INIT idempotente, contrato
  speculative, rechazos por falsabilidad, veredictos, memoria de refutación, invariante del
  contrato, sync de identidad src ↔ personalities.
- `docs/HYPOTHESIS_SCHEMA.md` — el contrato `speculative` (schema v1) y el ciclo de vida.
- `SECURITY.md`, `CONTRIBUTING.md`, `README.es.md`, `.gitignore`.

### Design
- `DESIGN.md` v0.2 — pivote de Gonzalo (2026-09-10): Iris como agente libre creativa y
  gestora del ecosistema, con Astrid de consejera de evidencia. Sustituye la v0.1
  (generadora de hipótesis contenida, sin agencia).

### Notes
- La memoria de refutación se modela como zona (`zona=refuted`), no como borrado —
  preferencia semántica (la historia se archiva). El bug de MVM que afectaba a los
  KILL de subárbol contra SQLite se detectó durante el desarrollo de iris v0.1.0 y
  se corrigió en [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol)
  (commit `3528f30`, con tests de roundtrip string/número incluidos).
- `HYPO` (no `NEW`): `NEW` es comando reservado de M y no puede usarse como etiqueta.

## [Unreleased] — diseño inicial (v0.1.0-draft)

### Added (2026-09-10)
- Diseño inicial + semilla del repo (LICENSE MIT, README, CHANGELOG).
- Decisión de arquitectura registrada: separación ontológica evidencia/hipótesis.
