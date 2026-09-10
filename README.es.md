# Iris

**Iris descompone la luz de la evidencia en un arcoíris de posibilidades — sin afirmar nunca que alguna de ellas sea real.**

Iris es el agente de **hipótesis** del equipo de investigación de Cadences Lab. Trabaja junto a [Astrid](https://github.com/GonzaloMonzonC/astrid) y [Elena](https://github.com/GonzaloMonzonC/elena), sus hermanas de la tríada:

- **Astrid** encuentra, ancla y verifica los hechos (claims con source, CID, firma HMAC — *"evidencia registrada, o silencio"*).
- **Iris** imagina lo que esos hechos podrían significar: hipótesis causales falsables, contrafactuales y experimentos capaces de matarlas — siempre etiquetadas `speculative=1`, nunca presentadas como claims.
- **Elena** cierra el ciclo: convierte *verdad suficiente* + *opciones abiertas* en una decision card firmada — *"¿Y ahora qué hacemos?"*.

> Una exige evidencia. La otra genera hipótesis que la evidencia pueda sostener o matar. Eso es un equipo de investigación.

## El contrato en una frase

Iris **no afirma**. Solo propone: *"No lo afirmo. Pero si fuera cierto, esto lo demostraría."*

Toda hipótesis de Iris es falsable por diseño (sin experimento que pueda matarla, es ruido), y toda promoción a evidencia la decide Astrid — nunca Iris.

## Uso

```bash
python tests/run_tests.py                        # suite completa (exit 0 = verde)
python harness/iris_harness.py status            # estado de la personalidad
python harness/iris_harness.py seed              # siembra ^PERSONALITY("iris")
python harness/iris_harness.py new \
    --text "Si X, esperaríamos Y" \
    --falsifier "medir Z en dos semanas"         # crea una hipótesis
python harness/iris_harness.py list              # hipótesis abiertas
python harness/iris_harness.py verdict --id h_... --verdict contradicha --cid df1231b4
python harness/iris_harness.py refuted           # memoria de refutación
```

## Estructura

| Ruta | Contenido |
|---|---|
| `src/iris.m` | La rutina M: personalidad + contrato de hipótesis (M-Light, sin dependencias externas) |
| `personalities/iris.md` | La personalidad legible (identidad canónica ASCII + ficha) |
| `harness/iris_harness.py` | Conecta Iris a un runtime lumen MVM (status/seed/new/list/verdict/refuted) |
| `tests/run_tests.py` | Suite completa contra un MVM real (PDB desechable, sin servicios externos) |
| `docs/HYPOTHESIS_SCHEMA.md` | El contrato `speculative` (schema v1) |
| `DESIGN.md` | Diseño y rol: agente libre creativa, gestora del ecosistema, con el consejo de evidencia de Astrid |

## Requisitos

Un runtime lumen MVM: clona [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) al lado del repo (recomendado) o instala `lumen-mcp` + apunta `LUMEN_MLIGHT_LIB` a tu `lumen_mlight.dll`/`.so`.

*Corre sobre un MVM lumen: una única librería nativa de ~4 MB (Rust a código máquina) — sin intérprete que instalar, sin runtime que arrancar.*

## Estado

**v0.1.0** — personalidad + contrato de hipótesis + suite verde (15 checks). Iris vive además como agente del ecosistema (mode `iris` en Poli, routing `^AGENTES("routing","iris")`).

## Licencia

MIT — Copyright (c) 2026 Gonzalo Monzón · Cadences Lab
