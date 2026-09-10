# Security Policy — Iris

## Modelo de seguridad

Iris es un agente de **hipótesis speculativas**: por diseño **no gestiona secretos, no accede a fuentes primarias y no publica claims**. Su superficie de riesgo es deliberadamente mínima.

### Lo que Iris NUNCA hace (garantías del contrato)

1. **No escribe en el registro de evidencia** de Astrid (`^EVIDENCE`) ni firma claims.
2. **No accede a credenciales**: no almacena ni procesa claves, tokens ni URLs privadas.
3. **No presenta especulación como hecho**: toda salida lleva `speculative=1` y `purpose=hypothesis`.
4. **No ejecuta acciones externas**: las funciones de este repo operan solo sobre un MVM local (PDB de prueba o la del ecosistema, en lectura/escritura de su propio namespace `^HYPOTHESIS`).

### Qué hacer si encuentras un problema

- **Repositorio**: abre un issue privado o escribe a los mantenedores (ver perfil del repo) sin incluir detalles explotables en público.
- **Contenido**: si una hipótesis archivada contiene algo sensible, puede eliminarse de `^HYPOTHESIS` sin afectar a la evidencia (los registros están separados por diseño — esa separación es una garantía de seguridad, no solo de honestidad).
- Tiempo de respuesta objetivo: 72h.

### Alcance

Este repositorio contiene **código fuente y personalidad**, no datos operativos. El runtime (MVM, PDB) vive en [lumen-protocol](https://github.com/GonzaloMonzonC/lumen-protocol). Para vulnerabilidades del MVM, reporta allí.

*Serie de agentes MIT de Cadences Lab — junto a [astrid](https://github.com/GonzaloMonzonC/astrid).*
