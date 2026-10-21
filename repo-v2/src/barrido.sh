#!/bin/sh
# Patrones baratos a tamanos grandes: {5}, {1,4}, {2,3}
cd "$(dirname "$0")/.."
for N in 16 17 18 19; do
  echo "== n=$N =="
  ./patron $N 5
  ./patron $N 1 4
  ./patron $N 2 3
done
