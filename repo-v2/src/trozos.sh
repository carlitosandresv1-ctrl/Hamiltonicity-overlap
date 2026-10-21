#!/bin/sh
cd "$(dirname "$0")/.."
N=$1; SAL=$2; shift 2
TOT=$(./patronp $N -2 "$@" | sed 's/[^0-9]//g')
touch "$SAL"
i=0
while [ $i -lt $TOT ]; do
  if grep -q "placa $i :" "$SAL"; then i=$((i+1)); continue; fi
  OUT=$(./patronp $N $i "$@" 2>&1)
  printf '%s\n' "$OUT" >> "$SAL"
  sync
  i=$((i+1))
done
printf 'TERMINADO %s colocaciones\n' "$TOT" >> "$SAL"
