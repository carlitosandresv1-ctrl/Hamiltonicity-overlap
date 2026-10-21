# Programas exhaustivos en C.  Requieren gcc y nada mas.
CC      = gcc
CFLAGS  = -O2 -Wall
BIN     = exh exhd exhm exhs par casih hunt2 hunts clases clases5 ventana patron patronp cazapat
BIN_V2  = verif_indep hc gadget gadget1 near11
BIN_V3  = near111 gadget11 anneal11 quot11 plug1

all: $(BIN) $(BIN_V2) $(BIN_V3)

%: src/c/%.c
	$(CC) $(CFLAGS) -o $@ $<

%: src/c/v2/%.c
	$(CC) $(CFLAGS) -o $@ $<

%: src/c/v3/%.c
	$(CC) $(CFLAGS) -o $@ $< -lm

clean:
	rm -f $(BIN) $(BIN_V2) $(BIN_V3)

.PHONY: all clean
