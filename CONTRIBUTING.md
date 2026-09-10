# Contributing — Iris

Gracias por querer contribuir. Iris es un agente MIT y su diseño está pensado para que **cualquiera pueda forkearlo y crear su propio agente**.

## Principios que NO se negocian

Toda contribución debe respetar el contrato de Iris (ver `docs/HYPOTHESIS_SCHEMA.md`):

1. **Nunca especulación como hecho** — toda hipótesis lleva `speculative=1` hasta que la evidencia la contraste.
2. **Condicional obligatorio** — "podría ser", nunca "esto es".
3. **Falsabilidad obligatoria** — sin experimento que pueda matar la hipótesis, es ruido.
4. **Separación ontológica** — los hechos anclados son de Astrid; Iris solo produce posibilidades.
5. **Sin lore privado** — este repo es autocontenido: nada de URLs, claves o rutas del ecosistema privado.

## Cómo contribuir

### Reportar un problema
Abre un issue describiendo: qué esperabas, qué pasó, cómo reproducirlo (los tests son el mejor formato).

### Proponer un cambio
1. Fork + rama descriptiva (`feat/lo-que-sea`, `fix/lo-que-sea`).
2. **Los tests deben pasar**: `python tests/run_tests.py` (exit 0). Toda funcionalidad nueva, con su check.
3. Mantén la identidad canónica ASCII sincronizada: `src/iris.m` ↔ `personalities/iris.md` (el check 10 lo verifica).
4. Comandos M portables: solo M-Light (sin dependencias de rutinas externas del ecosistema).
5. Pull request con una frase clara: **qué hipótesis nueva permite crear o qué invariante protege**.

### Ideas bienvenidas
- Nuevos formatos de hipótesis (contrafactuales, vectores de plausibilidad).
- Mejoras al diseño experimental sugerido.
- Traducciones de docs (patrón actual: `X.md` + `X.es.md`).

## Entorno de desarrollo

```
python tests/run_tests.py     # suite completa (necesita un runtime lumen M)
python harness/iris_harness.py status    # estado de la personalidad
```

Requiere un runtime MVM: clona [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol) al lado (o `pip install lumen-mcp` + `LUMEN_MLIGHT_LIB`).

## Licencia

Al contribuir aceptas que tu contribución se publica bajo la licencia MIT del repositorio.
