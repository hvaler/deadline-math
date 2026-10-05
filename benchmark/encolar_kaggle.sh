#!/bin/sh
# Encola ejecuciones en Kaggle respetando el tope de 40 sesiones simultáneas.
# Sin argumentos: cada task contra todos los modelos. Con un fichero: solo los pares «task modelo» que liste
# (lo genera benchmark/pendientes_kaggle.py).
# Uso (desde la raíz): sh benchmark/encolar_kaggle.sh [pendientes.txt] > benchmark/resultados/encolar.log 2>&1
export PYTHONIOENCODING=utf-8
KAGGLE=.venv/Scripts/kaggle.exe

if [ -n "$1" ]; then
  PARES=$(tr -d '\r' < "$1")  # los ficheros escritos desde Python en Windows llevan CRLF
else
  MODELOS=$(awk 'NR>2{print $1}' benchmark/resultados/modelos-kaggle-2026-10-03.txt)
  PARES=$(for task in deadline-math-direct deadline-math-hard-direct deadline-math-hard-reasoned deadline-math-reasoned; do
    for modelo in $MODELOS; do echo "$task $modelo"; done
  done)
fi

echo "$PARES" | while read -r task modelo; do
  [ -z "$task" ] && continue
  fallos=0
  while true; do
    salida=$($KAGGLE b t run "$task" -m "$modelo" 2>&1)
    case "$salida" in
      *Scheduled*) echo "$(date -u +%T) $task $modelo programado"; break ;;
      *"session count"*) sleep 60 ;;                       # tope de 40 sesiones: esperar
      *[Qq]uota*) echo "$(date -u +%T) PARADA por cuota: $task $modelo: $salida"; exit 1 ;;
      *)
        fallos=$((fallos + 1))
        echo "$(date -u +%T) $task $modelo (intento $fallos): $salida"
        if [ "$fallos" -ge 3 ]; then echo "$(date -u +%T) SALTADO: $task $modelo"; break; fi  # no insistir sin fin
        sleep 30 ;;
    esac
  done
done
echo "$(date -u +%T) FIN"
