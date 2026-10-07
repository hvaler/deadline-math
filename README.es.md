# Deadline Math

*Read in English: [README.md](README.md).*

**¿Sabe un modelo de lenguaje pasar un plazo publicado a la hora local de quien lo lee?**
«Submissions close October 28, 2026 at 11:59 PM PT»: ¿qué hora es eso en Madrid?

Un benchmark creado en [Kaggle Community Benchmarks](https://www.kaggle.com/benchmarks) para el
[DEV × Kaggle Benchmarking Challenge](https://dev.to/challenges/kaggle-2026-09-23).

- **Benchmark público:** [kaggle.com/benchmarks/hugovalerrojas/deadline-mat](https://www.kaggle.com/benchmarks/hugovalerrojas/deadline-mat)
- **Artículo (en inglés):** [The model knew the rule. It still used last week's offset.](https://dev.to/hugo_valer_79d0d94e00804b/the-model-knew-the-rule-it-still-used-last-weeks-offset-584m)
- **Prerregistro:** [docs/preregistro-original-es.md](docs/preregistro-original-es.md) (original) y
  [docs/PREREGISTRATION.md](docs/PREREGISTRATION.md) (traducción)

## Conclusiones

En 2026, Europa vuelve al horario de invierno el 25 de octubre y Estados Unidos el 1 de noviembre; en primavera,
Estados Unidos cambia primero (8 de marzo) y Europa después (29 de marzo). Durante esas semanas, la diferencia
horaria habitual entre ambos lados falla por una hora.

- **El fallo es mecánico, no aleatorio.** En una prueba prerregistrada con 50 pares trampa/control (la misma frase
  con la fecha dentro o fuera de esas semanas), **el 91 % de las respuestas erróneas con hora (293 de 321) son
  exactamente la respuesta ingenua**: la diferencia de siempre, o sumar horas de reloj por encima de un cambio de hora.
- **La trampa cuesta 29,8 puntos de acierto** de media a los 19 modelos prerregistrados (IC 95 %: +25,4 a +34,2);
  13 empeoran y ninguno mejora. **El resultado se repitió** en una segunda ejecución (+29,6 puntos, 91 %).
- **Es cuestión de generación, no de tamaño.** Claude Sonnet 4.5 acierta el 100 % de los controles y el 6 % de las
  trampas; dentro de cada línea de Claude la costumbre desaparece versión a versión, y los modelos más recientes
  probados (Claude Opus 5.5 y Sonnet 5.5, GPT-6 Sol, GPT-6.1 Sol) ya no cometen el error.
- **La temperatura 0 no es determinista:** dos ejecuciones del mismo modelo coinciden en el 92 % de los casos.

**Lección práctica:** que el modelo extraiga la fecha, la hora y la zona, y que la cuenta la haga una biblioteca de
husos horarios.

Resultados completos (en inglés): [benchmark/resultados/RESULTS.md](benchmark/resultados/RESULTS.md).

## Reproducir

Las instrucciones están en el [README en inglés](README.md#reproduce). Los docstrings y comentarios del código
fuera de `deadline_math.py` están en español.

## Licencia y transparencia

Código con [licencia MIT](LICENSE). Se usó IA (Claude) como ayuda para el código, el análisis y la redacción; el
autor eligió el problema, tomó las decisiones de diseño y revisó cada afirmación.
