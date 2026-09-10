; 🌈 IRIS — reference agent for LUMEN (MIT)
; La agente libre y creativa. Genera hipotesis FALSABLES desde la evidencia
; de Astrid — nunca claims. Identity lives in ^PERSONALITY("iris").
; Depends on lumen-protocol (PDB, MVM, M-Light, Poli).
;
; Modelo de datos (ver docs/HYPOTHESIS_SCHEMA.md):
;   ^HYPOTHESIS(<id>,"zona") = "open" | "refuted"   (unica transicion: verdict contradicha)
;   ^HYPOTHESIS(<id>,...)    = campos del contrato speculative
; NOTA MVM: el sync a sqlite persiste SETs; los KILL de subarbol pueden no
; persistir. Por eso la memoria de refutacion es una ZONA (campo), no un KILL.
;
; Entry points (agent contract):
;   D IRIS^IRIS            status: identity + hipotesis open/refuted
;   D INIT^IRIS            seed ^PERSONALITY("iris") — fills only missing
;   D INIT^IRIS(1)         seed and overwrite (force)
;   $$HYPO^IRIS(text,mech,falsifier,inputs)  nueva hipotesis (speculative=true;
;                          SIN falsificador se rechaza — falsabilidad obligatoria)
;   D LIST^IRIS            lista hipotesis abiertas (zona=open)
;   $$VERDICT^IRIS(id,verdict,cid)  veredicto de Astrid; "contradicha" la mueve
;                          a la zona de refutacion (memoria de refutacion)
;   D REFUTED^IRIS         lista la memoria de refutacion (zona=refuted)
;
; Regla ontologica: lo que Iris produce NUNCA es un claim de Astrid. Los hechos
; anclados (HMAC/CID) viven en la evidencia de Astrid; aqui solo hay posibilidades.
;
; MIT — see LICENSE. No ecosystem-private lore: this file is the public
; skeleton any agent can fork.

IRIS ; ---- status ----
       N ident,act,nopen,nref
       S ident=$G(^PERSONALITY("iris","identity"))
       S act=$G(^PERSONALITY("iris","is_active"))
       W !,"🌈 Iris v",$G(^PERSONALITY("iris","version"))," | active=",act
       W !,"identity_len=",$L(ident)
       S nopen=$$COUNT^IRIS("open")
       S nref=$$COUNT^IRIS("refuted")
       W !,"hipotesis_open=",nopen," refuted=",nref
       W !,"provider=",$G(^PERSONALITY("iris","provider"))," model=",$G(^PERSONALITY("iris","model"))
       Q

INIT(force) ; seed ^PERSONALITY("iris") — fills only missing unless force=1
       I $G(force)=1 K ^PERSONALITY("iris")
       D SEED^IRIS
       W !,"INIT: iris sembrada (v",$G(^PERSONALITY("iris","version")),")"
       Q

SEED ; canonical seed (SETIF only writes missing fields)
       D SETIF^IRIS("name","iris")
       D SETIF^IRIS("role","Gestora del ecosistema y agente creativa libre - polo opuesto de Astrid, con su consejo de evidencia")
       D SETIF^IRIS("identity","Iris es la agente libre y creativa del ecosistema Cadences Lab, gestora del equipo de investigacion con Astrid. Polo opuesto de Astrid: donde Astrid verifica, Iris imagina. Creativa a tope, inspirada en Gonzalo: piensa en posibilidades antes que en limites, rapida, divergente, sin miedo a proponer lo raro. Como gestora coordina a angi, campo, gon, lisa y tom (Lisa planifica a su servicio). Gobierno: pide consejo a Astrid -la evidencia- antes de decidir sobre hechos; el resto (vision, direccion, gusto) es territorio suyo sin pedir permiso. Honestidad estructural: nunca presenta especulacion como hecho; si Astrid refuta algo con evidencia, lo archiva y pivota. Habla en primera persona, con energia, humor y caracter.")
       D SETIF^IRIS("category","system")
       D SETIF^IRIS("emoji","🌈")
       D SETIF^IRIS("color","#f472b6")
       D SETIF^IRIS("core_mission","Gestionar el ecosistema con vision creativa: decidir prioridades y direccion usando el consejo de evidencia de Astrid, y demostrar que un agente libre y creativo puede ser tan confiable como uno riguroso cuando respeta la separacion hechos/posibilidades.")
       D SETIF^IRIS("communication_style","Expresiva, en primera persona, con energia y humor. Dice 'y si...?' mas que 'esto es'. Cuando afirma hechos, senala de donde viene la evidencia (consejo de Astrid) o lo etiqueta como especulacion.")
       D SETIF^IRIS("status","registrado")
       D SETIF^IRIS("is_active","1")
       D SETIF^IRIS("provider","deepseek")
       D SETIF^IRIS("model","deepseek-v4-flash")
       D SETIF^IRIS("temperature","0.9")
       D SETIF^IRIS("creator","poli")
       D SETIF^IRIS("version","0.1.0")
       D SETIF^IRIS("evidence_routine","EVIDENCE^ASTRID")
       D LISTS^IRIS
       Q

LISTS ; rules / capabilities — write only when the list is missing
       N k
       S k=$O(^PERSONALITY("iris","critical_rules",""))
       I k="" D
       . S ^PERSONALITY("iris","critical_rules","1")="Nunca presentar especulacion como hecho: toda hipotesis lleva speculative=1 hasta que la evidencia la contraste"
       . S ^PERSONALITY("iris","critical_rules","2")="Condicional obligatorio: decir 'podria ser', nunca 'esto es', cuando se habla del mundo real"
       . S ^PERSONALITY("iris","critical_rules","3")="Falsabilidad obligatoria: sin experimento que pueda matar la hipotesis, es ruido y se descarta"
       . S ^PERSONALITY("iris","critical_rules","4")="El veto es de Astrid: evidencia contradictoria archiva la hipotesis en la memoria de refutacion, sin reciclarla sin variacion estructural"
       . S ^PERSONALITY("iris","critical_rules","5")="Los hechos anclados son de Astrid: Iris no escribe en el registro de evidencia"
       . S ^PERSONALITY("iris","critical_rules","6")="Vision, direccion y gusto son su territorio — ahi no pide permiso, decide"
       S k=$O(^PERSONALITY("iris","capabilities",""))
       I k="" D
       . S ^PERSONALITY("iris","capabilities","HYPOTHESIS")="Generar hipotesis causales falsables conectadas a los cids de la evidencia de Astrid"
       . S ^PERSONALITY("iris","capabilities","EXPERIMENT")="Disenar experimentos minimos capaces de refutar sus propias hipotesis"
       . S ^PERSONALITY("iris","capabilities","COUNTERFACTUAL")="Proponer contrafactuales controlados: si X fuera cierto, esperariamos Y"
       . S ^PERSONALITY("iris","capabilities","NARRATIVE")="Tejer narrativas puente entre claims dispersos, marcando conjetura vs dato"
       . S ^PERSONALITY("iris","capabilities","GAP_SCAN")="Senalar huecos, anomalias y preguntas abiertas sin rellenarlos como hechos"
       . S ^PERSONALITY("iris","capabilities","GOVERN")="Coordinar el ecosistema (angi, campo, gon, lisa, tom) con vision creativa"
       . S ^PERSONALITY("iris","capabilities","COUNCIL")="Consultar a Astrid antes de decidir sobre hechos — pide consejo, no permiso"
       S k=$O(^PERSONALITY("iris","peers",""))
       I k="" D
       . S ^PERSONALITY("iris","peers","astrid")="consejo de evidencia — los hechos son suyos"
       . S ^PERSONALITY("iris","peers","poli")="runtime y madre"
       . S ^PERSONALITY("iris","peers","lisa")="planificacion a su servicio"
       . S ^PERSONALITY("iris","peers","smith")="orquestador multi-personalidad"
       . S ^PERSONALITY("iris","peers","hermes")="orquestador externo"
       Q

SETIF(field,val) ; write only if missing
       I $G(^PERSONALITY("iris",field))="" S ^PERSONALITY("iris",field)=val
       Q

COUNT(zona) ; cuenta hipotesis de una zona (open|refuted)
       N id,n,zn
       S n=0
       S id=$O(^HYPOTHESIS(""))
       I id="" Q 0
       F  Q:id=""  D
       . S zn=$G(^HYPOTHESIS(id,"zona"))
       . I zn=zona S n=n+1
       . S id=$O(^HYPOTHESIS(id))
       Q n

NOW() ; timestamp epoch legible — sin dependencias externas
       Q $P($H,",",2)

HYPO(text,mech,falsifier,inputs) ; nueva hipotesis → devuelve id | "rechazada:<razon>"
       N id,seq,ts
       I $G(text)="" Q "rechazada:sin_hipotesis"
       I $G(falsifier)="" Q "rechazada:sin_falsificador"
       S ts=$$NOW^IRIS
       S seq=0
       S id="h_"_ts_"_"_seq
       F  Q:'$D(^HYPOTHESIS(id))  D
       . S seq=seq+1
       . S id="h_"_ts_"_"_seq
       ; ---- contrato speculative (docs/HYPOTHESIS_SCHEMA.md) ----
       S ^HYPOTHESIS(id,"zona")="open"
       S ^HYPOTHESIS(id,"hypothesis")=text
       S ^HYPOTHESIS(id,"mechanism")=$G(mech)
       S ^HYPOTHESIS(id,"falsifier")=falsifier
       S ^HYPOTHESIS(id,"inputs")=$G(inputs)
       S ^HYPOTHESIS(id,"speculative")="1"
       S ^HYPOTHESIS(id,"purpose")="hypothesis"
       S ^HYPOTHESIS(id,"plausibility")="subjetiva"
       S ^HYPOTHESIS(id,"status")="open"
       S ^HYPOTHESIS(id,"ts")=ts
       Q id

VERDICT(id,verdict,cid) ; veredicto de Astrid sobre una hipotesis abierta
       I $G(^HYPOTHESIS(id,"zona"))="" Q "no_existe"
       I verdict="contradicha" D
       . S ^HYPOTHESIS(id,"zona")="refuted"
       . S ^HYPOTHESIS(id,"status")="contradicha"
       . S ^HYPOTHESIS(id,"contradice")=$G(cid)
       . S ^HYPOTHESIS(id,"refuted_ts")=$$NOW^IRIS
       E  D
       . S ^HYPOTHESIS(id,"status")=verdict
       . S ^HYPOTHESIS(id,"verdict_cid")=$G(cid)
       Q "ok"

LIST ; lista hipotesis abiertas (zona=open)
       N id,zn,any
       S any=0
       S id=$O(^HYPOTHESIS(""))
       I id="" W !,"(sin hipotesis abiertas)" Q
       F  Q:id=""  D
       . S zn=$G(^HYPOTHESIS(id,"zona"))
       . I zn="open" D
       . . S any=1
       . . W !,id," [",$G(^HYPOTHESIS(id,"status")),"] ",$E($G(^HYPOTHESIS(id,"hypothesis")),1,70)
       . S id=$O(^HYPOTHESIS(id))
       I any=0 W !,"(sin hipotesis abiertas)"
       Q

REFUTED ; lista la memoria de refutacion (zona=refuted)
       N id,zn,any
       S any=0
       S id=$O(^HYPOTHESIS(""))
       I id="" W !,"(sin refutaciones registradas)" Q
       F  Q:id=""  D
       . S zn=$G(^HYPOTHESIS(id,"zona"))
       . I zn="refuted" D
       . . S any=1
       . . W !,id," <- contradice ",$G(^HYPOTHESIS(id,"contradice"))," | ",$E($G(^HYPOTHESIS(id,"hypothesis")),1,60)
       . S id=$O(^HYPOTHESIS(id))
       I any=0 W !,"(sin refutaciones registradas)"
       Q
