# Contrato de Hipótesis — Iris (schema v1)

Este documento define **qué es una hipótesis de Iris** y cómo se relaciona con la evidencia de [Astrid](https://github.com/GonzaloMonzonC/astrid). Es el equivalente al `EVIDENCE_SCHEMA.md` de Astrid — pero para posibilidades, no para hechos.

## El objeto hipótesis

Toda hipótesis vive en el namespace `^HYPOTHESIS(<id>)` del MVM y tiene esta forma:

```
^HYPOTHESIS(<id>,"zona")         = "open" | "refuted"
^HYPOTHESIS(<id>,"hypothesis")   = frase condicional ("si P, esperaríamos Q")
^HYPOTHESIS(<id>,"mechanism")    = mecanismo causal propuesto (conjetura)
^HYPOTHESIS(<id>,"falsifier")    = experimento mínimo que podría matarla (OBLIGATORIO)
^HYPOTHESIS(<id>,"inputs")       = cids de la evidencia de Astrid que la motivaron
^HYPOTHESIS(<id>,"speculative")  = "1"   (inmutable: nunca se promueve aquí a claim)
^HYPOTHESIS(<id>,"purpose")      = "hypothesis"
^HYPOTHESIS(<id>,"plausibility") = "subjetiva" (declarada como tal)
^HYPOTHESIS(<id>,"status")       = "open" | "plausible" | "insuficiente" | "contradicha"
^HYPOTHESIS(<id>,"ts")           = timestamp de creación
^HYPOTHESIS(<id>,"contradice")   = cid contradictorio (solo si zona=refuted)
^HYPOTHESIS(<id>,"refuted_ts")   = timestamp de refutación
```

### Identificadores

`<id>` = `h_<epoch>_<seq>` — único, nunca reutilizado. El `seq` resuelve colisiones dentro del mismo segundo.

## Las seis reglas del contrato

1. **Etiquetado inmutable** — toda salida de Iris declara `speculative=1`. No existe salida sin etiqueta.
2. **Almacenes separados** — hechos anclados (Astrid, HMAC/CID) vs. hipótesis (Iris, `^HYPOTHESIS`). La creatividad puede contaminar la discusión, jamás la base de hechos.
3. **Condicional obligatorio** — Iris no afirma: "esto podría ser", nunca "esto es".
4. **Falsabilidad obligatoria** — sin `falsifier` no hay hipótesis: `$$HYPO` rechaza la creación (`rechazada:sin_falsificador`).
5. **Veto de Astrid** — evidencia contradictoria ⇒ `zona=refuted` + `contradice=<cid>`. La hipótesis no se repite sin variación estructural.
6. **Memoria de refutación** — las hipótesis refutadas quedan archivadas en la zona `refuted` (visibles con `REFUTED^IRIS`), nunca recicladas silenciosamente.

## Ciclo de vida

```
       $$HYPO^IRIS(text,mech,falsifier,inputs)
                      │
                      ▼
              zona=open  ──veredicto "plausible"/"insuficiente"──▶  sigue open
                      │                                              (status actualizado)
                      │
       $$VERDICT^IRIS(id,"contradicha",cid)
                      │
                      ▼
              zona=refuted  (memoria de refutación; LIST deja de mostrarla)
```

**La promoción a evidencia NO está en este contrato**: una hipótesis que sobrevive al contraste puede ser *candidata*, pero la promoción la decide Astrid con su pipeline de evidencia (fuera del alcance de Iris, por diseño).

## Interfaz M (resumen)

| Entrada | Significado |
|---|---|
| `D IRIS^IRIS` | status: identidad + conteos open/refuted |
| `D INIT^IRIS[(1)]` | siembra la personalidad (idempotente / forzar) |
| `$$HYPO^IRIS(text,mech,falsifier,inputs)` | crea hipótesis → `h_...` o `rechazada:<razón>` |
| `D LIST^IRIS` | lista las abiertas |
| `$$VERDICT^IRIS(id,verdict,cid)` | veredicto de Astrid; contradicha ⇒ refutación |
| `D REFUTED^IRIS` | memoria de refutación |

## Nota de implementación (MVM)

La memoria de refutación es una **zona** (campo `zona=refuted`), no un borrado: la historia no se borra, se archiva. (Contexto: al implementar v0.1.0 se descubrió que el KILL de subárbol no persistía correctamente contra SQLite en el MVM — corregido en lumen-protocol `3528f30` con tests. El modelo de zonas se mantiene por preferencia semántica: archivar es mejor que borrar para una memoria de refutación.)

## Compatibilidad

- Schema v1 — Iris v0.1.0.
- Cambios incompatibles ⇒ schema v2 + nota de migración en CHANGELOG.
