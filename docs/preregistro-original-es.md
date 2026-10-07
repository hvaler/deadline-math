# Prerregistro — conjunto confirmatorio de pares (Deadline Math)

**Escrito el 2026-10-04 a las 06:53 UTC (08:53 en Madrid), antes de generar los casos y de ejecutar ninguno.**
No se editará después de la primera ejecución. Cualquier cambio posterior irá en una sección «Desviaciones»
fechada al final, con su motivo.

## Por qué

Los 31 casos actuales son **exploratorios**: el nivel difícil se diseñó después de ver dónde fallaban los modelos.
Lo que observamos allí (2026-10-03, cohorte de 19 modelos, 321 respuestas equivocadas) fue que el 60 % de los
errores eran **exactamente de una hora**: en la semana de otoño desfasada, 38 de 39; en las duraciones que cruzan
un cambio de hora, 47 de 63 eran +1 h. Este conjunto existe para **confirmar o refutar** eso con un diseño fijado
de antemano, no para buscar fallos nuevos.

## Hipótesis

- **H1 (penalización por el cambio de hora).** Para un mismo enunciado, los modelos aciertan menos cuando la fecha
  cae en un periodo en que la diferencia horaria habitual no vale (semana desfasada, o duración que cruza un cambio
  de hora) que cuando la misma fecha se mueve fuera de ese periodo.
- **H2 (el fallo es mecánico).** Entre las respuestas equivocadas a los casos trampa, **más de la mitad coinciden
  exactamente con la «respuesta ingenua»**: la que sale de aplicar la diferencia horaria de las fechas de control
  (conversiones) o de sumar horas de reloj (duraciones).

## Diseño

- **Pares emparejados.** Cada caso trampa tiene un gemelo de control con el mismo texto, el mismo lector, la misma
  hora de reloj y el mismo día de la semana; solo cambia la fecha, desplazada fuera del periodo problemático:
  - conversiones de otoño: trampa entre el 26 y el 31/10/2026; control, 7 días antes (19–24/10, ambos lados en
    horario de verano);
  - conversiones de primavera: trampa entre el 9 y el 14/03/2026; control, 21 días después (30/03–04/04, ambos en
    horario de verano);
  - duraciones (24, 48 y 72 h): la trampa cruza un cambio de hora en la zona del evento; el control empieza 7 días
    antes y no cruza ninguno.
- **Factores que varían**: par de zonas (Pacífico y Este de EE. UU. frente a Madrid, Londres, Berlín y París),
  sentido de la conversión (EE. UU.→Europa y Europa→EE. UU.), hora del día (incluidas horas que cambian de día),
  estación (otoño y primavera) y duración.
- **Zonas por nombre genérico** («PT», «ET», «London time»), nunca por abreviaturas que ya fijan el desfase (PDT,
  CEST): el modelo tiene que saber qué regla rige ese día.
- **Respuesta correcta** calculada con `zoneinfo` y comprobada contra un **segundo oráculo independiente** escrito
  a mano con las reglas de cambio de hora de EE. UU. y de la UE. Si discrepan en un solo caso, no se ejecuta nada.
- **El generador comprueba cada par**: en la trampa, la diferencia horaria (o el desfase al final de la duración)
  es distinta de la del control; en el control, la respuesta ingenua coincide con la correcta.
- **Prompt**: el mismo del modo directo actual (`PROMPTS["direct"]`). Modo razonado solo si sobra cuota, como
  análisis secundario.
- **Modelos**: la cohorte de 19 de `benchmark/resultados/tabla-cohorte.md` (2026-10-03). Si alguno no puede
  ejecutarse por infraestructura, se informa como «no completado».
- **Una ejecución por modelo**, temperatura 0 (la del SDK).

## Medidas y análisis

- Por modelo: acierto en trampas y en controles, con intervalo de Wilson al 95 %; **penalización** = acierto en
  controles − acierto en trampas; prueba de McNemar exacta sobre los pares discordantes.
- Agregado: penalización media de la cohorte con intervalo por bootstrap sobre pares; número de modelos con
  penalización positiva, negativa y nula (prueba de signos).
- H2: proporción de errores en trampas que igualan la respuesta ingenua, con intervalo de Wilson. **H2 se sostiene
  si el límite inferior del intervalo supera el 50 %.**
- **H1 se sostiene** si la penalización agregada es positiva con un intervalo que no incluye el cero.
- Se informa por separado de: estación, tipo (conversión o duración) y sentido. Son descripciones, no pruebas nuevas.
- **Exclusiones**: casos sin respuesta por infraestructura (403/404/429/503) quedan fuera del par entero. Respuestas
  sin línea `ANSWER` cuentan como fallo y se informan aparte. No hay más exclusiones.
- **Se publica el resultado sea cual sea**, también si H1 o H2 no se sostienen.

## Calendario

Generación y piloto local, 04/10. Ejecución en Kaggle, 05–06/10 si hay cuota. **Congelación de datos: miércoles
07/10.** Artículo, 08–10/10. Publicación, domingo 11/10.

## Desviaciones

- **2026-10-04 07:58 UTC — Ampliación a más modelos (análisis secundario).** Escrito antes de ejecutarla. Tras la ejecución
  confirmatoria, la cohorte de las 4 tasks creció de 19 a 33 modelos al recargarse la cuota. El conjunto de pares se
  ejecuta también sobre los 14 modelos nuevos (entre ellos los Claude Opus 4.x, GPT-5.5, GPT-5.6 Sol/Terra y Gemini
  3.1 Pro), con el mismo prompt, la misma versión de la task y el mismo análisis. **El resultado principal sigue
  siendo el de los 19 modelos prerregistrados**; el de la ampliación se presenta aparte y sin cambiar los criterios
  de H1 y H2. Motivo: sin ella no se sabe si los modelos más caros caen en la misma trampa. Se repite además Qwen3
  Next 80B Thinking, que no completó por un 429.

- **2026-10-05 08:09 UTC — Discrepancias encontradas al traducir el prerregistro** (no cambian ningún resultado):
  - El diseño cita como zonas europeas «Madrid, Londres, Berlín y París», pero el generador (fijado y publicado
    antes de ejecutar) usa Madrid, Londres y Berlín: **París no aparece en ningún caso**.
  - El calendario preveía ejecutar en Kaggle el 05–06/10; la ejecución confirmatoria se hizo el 04/10, en cuanto
    se recargó la cuota.

## Registro de ejecución (no cambia el plan)

- 2026-10-04 ~07:00 UTC — **Piloto local de validación del diseño** (no forma parte del análisis confirmatorio):
  Gemini 3.1 Flash Lite y GPT-5.4 nano, modo directo, 100 casos cada uno. Flash Lite: trampas 32 %, controles
  100 %, 34/34 errores iguales a la respuesta ingenua. Nano: trampas 6 %, controles 54 %, 23/47. Ningún error de
  infraestructura ni de formato que obligue a cambiar el diseño. Informe: `benchmark/resultados/pares-piloto-direct.md`.
- **Fecha de congelación movida al miércoles 07/10** (antes, martes 06/10) para dar tiempo al conjunto de pares.
- 2026-10-04 ~07:15–07:45 UTC — **Ejecución confirmatoria** en Kaggle (`deadline-math-pairs-direct` v1), cohorte
  de 19. Completan 18; Qwen3 Next 80B Thinking termina en error de infraestructura (429 en `pc-aut-11-C`) y queda
  como «no completado». Resultado (`benchmark/resultados/pares-kaggle-deadline-math-pairs-direct.md`):
  - **H1 se sostiene**: penalización media +29,6 % (IC bootstrap 95 % +25,4 % a +33,7 %); 12 modelos con
    penalización positiva, 0 negativa, 6 sin diferencia (prueba de signos p = 0,0005).
  - **H2 se sostiene**: 278 de 306 errores en trampas (91 %, IC Wilson 87–94 %) son exactamente la respuesta
    ingenua.
  - Nota de proceso: la primera descarga llegó incompleta (9 de 18); el análisis se repitió con la descarga
    completa. Las cifras de arriba son las de la descarga completa.
- 2026-10-04 ~19:45 UTC — **Ampliación (secundaria)**: 8 de 14 modelos completan antes de agotarse otra vez la
  cuota (403); Qwen3 Next Thinking vuelve a fallar (503). H1 y H2 también se sostienen en la ampliación: penalización
  +25,5 % (IC +20,5 % a +30,5 %), 118/121 errores ingenuos (98 %). Destacan Claude Sonnet 4.5 (trampas 6 %, controles
  100 %, 47/47 ingenuos) y que GPT-5.5, GPT-5.6 Sol y GPT-5.6 Terra no muestran penalización.
  Pendientes para el 05/10: Opus 4.5 y 4.8, GPT-6 Astra, Gemini 2.5 Pro, 3.1 Pro y 3.5 Flash, Qwen3 Next Thinking.
- 2026-10-05 ~07:50 UTC — **Ampliación (secundaria), completada**: 14 modelos. H1: penalización +20,7 % (IC +16,6 % a
  +24,7 %), 8 positivos / 1 negativo. H2: 169/173 errores ingenuos (98 %). Claude Opus 4.5 22 % / 82 %, Sonnet 4.5
  6 % / 100 %, Opus 4.8 78 % / 100 %; GPT-5.5, GPT-5.6 Sol/Terra, GPT-6 Astra, Gemini 3.1 Pro y 3.5 Flash sin
  penalización. Se añaden a la ampliación, con el mismo criterio, los 4 modelos del benchmark público que aún no la
  tenían (Qwen3 Next Instruct, DeepSeek R1, Qwen3 235B, Claude Opus 5).
- 2026-10-06 ~07:03 UTC — **Último reintento.** Qwen3 Next 80B Thinking completa los pares: **el resultado
  prerregistrado queda con 19 de 19 modelos.** Recalculado con el mismo análisis:
  - **H1 se sostiene**: penalización media +29,8 % (IC bootstrap 95 % +25,4 % a +34,2 %); 13 modelos con penalización
    positiva, 0 negativa (prueba de signos p = 0,00024).
  - **H2 se sostiene**: 293 de 321 errores en trampas (91 %, IC Wilson 88–94 %) son la respuesta ingenua.
  - Las cifras de 18 modelos anotadas el 04/10 (+29,6 %; 278/306) quedan sustituidas por estas; no cambia el veredicto.
  Ampliación (secundaria), ya con 18 modelos (se suman Qwen3 Next Instruct, DeepSeek R1, Qwen3 235B y Claude Opus 5):
  penalización +25,1 % (IC +21,7 % a +28,3 %), 11 positivos / 2 negativos; 261/274 errores ingenuos (95 %). Claude Opus 5
  sale con −6 puntos (trampas 96 %, controles 90 %; McNemar p = 0,45, no significativo).
- **2026-10-06 — Congelación de datos.** No se ejecuta nada más.
- **2026-10-06 18:32 UTC — Reapertura de la congelación (desviación, escrita antes de ejecutar).** Kaggle ha añadido 5 modelos después del 03/10 (Claude Opus 5.5, Claude Sonnet 5.5, GPT-6 Luna, GPT-6 Sol, GPT-6.1 Sol). Se ejecutan las 5 tasks sobre ellos con la misma versión de cada task. El resultado prerregistrado (19 modelos) no cambia; los pares de estos modelos entran en la ampliación secundaria. Motivo: saber si los modelos más recientes también caen en la trampa.
  Se reintentan también, en la misma reapertura: gpt-oss-120b (estándar directo y pares; ya completó las otras tres tasks) y Grok 4.5 y 4.6 (una prueba en el estándar directo; si el proxy sigue devolviendo 404, quedan fuera).
  - 2026-10-06 18:38 UTC: Grok 4.5 y 4.6 vuelven a dar 404 («model not found») en el proxy; quedan fuera.
  - 2026-10-06 ~18:50 UTC: el leaderboard público pinta las ejecuciones con error como resultado falso (0 en «Overall»). Se reintentan Qwen3 Next Thinking en las 4 tasks originales y Claude Sonnet 4.6 en el estándar directo para sustituirlas; se lanzan además los pares de Sonnet 4.6 (ampliación).
  - 2026-10-06 ~18:55 UTC: Grok 4.5/4.6 retirados del benchmark público. Se reintentan 3 celdas más con ejecución fallida en la última versión: Qwen3 Coder 480B (estándar razonado) y Qwen3 Next Instruct (estándar razonado y difícil razonado).
- **2026-10-06 19:14 UTC — Réplica (análisis secundario, escrita antes de ejecutarla).** Se repite una vez el conjunto de pares (misma versión de la task, mismo prompt, temperatura 0) sobre los 19 modelos prerregistrados. **El resultado principal sigue siendo la primera ejecución limpia de cada modelo**, tal como se prerregistró; la réplica se analiza aparte con los mismos criterios de H1 y H2 y se informa sea cual sea. Motivo: la temperatura 0 no es determinista (repetibilidad del 92,8 % en las tasks originales) y conviene saber si el resultado se repite.
- 2026-10-07 ~01:00 UTC — **Resultado de la reapertura y de la réplica.**
  - **Réplica (secundaria): H1 y H2 se repiten.** 18 de 19 modelos (Qwen3 Next Thinking falla todos los reintentos con 429): penalización +29,6 % (IC +26,0 % a +33,1 %); 277/306 errores ingenuos (91 %).
  - Ampliación (secundaria), ya con 24 modelos: penalización +22,6 % (IC +19,7 % a +25,4 %); 308/321 (96 %). Claude Opus 5.5, Sonnet 5.5, GPT-6 Sol y GPT-6.1 Sol: 100 % en trampas y controles; GPT-6 Luna 86 % / 100 %.
  - Cohorte de las 4 tasks: 43 modelos. Quedan fuera gpt-oss-120b (dos ejecuciones colgadas) y Grok 4.5/4.6 (404).
- **2026-10-07 — Nueva congelación de datos.** No se ejecuta nada más.
  - 2026-10-07 01:10 UTC: gpt-oss-120b completa el estándar directo después de la congelación (descarga 01:00); no entra en la cohorte. Visible en el leaderboard.
