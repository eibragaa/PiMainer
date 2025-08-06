#!/bin/bash

# --- Configuração ---
TMUX_SESSION_NAME="nerdminer"
MINER_DIR="/root/cpuminer-opt"
MINER_CMD="./cpuminer -a sha256d -o stratum+tcp://solo.ckpool.org:3333 -u bc1qkfm0r9mpqnk7gnfercqyheqa3n5x6ycmyav48p"
DISPLAY_SCRIPT_PATH="/root/PiMainer/pimainer_display.py" # Verifique se este é o nome e caminho corretos

# --- Lógica do Script ---
# Garante que não haja uma sessão antiga com o mesmo nome
tmux kill-session -t $TMUX_SESSION_NAME 2>/dev/null

# Cria uma nova sessão tmux desanexada (-d)
tmux new-session -d -s $TMUX_SESSION_NAME

# Janela 0: Inicia o minerador
tmux send-keys -t $TMUX_SESSION_NAME:0 "cd $MINER_DIR" C-m
tmux send-keys -t $TMUX_SESSION_NAME:0 "$MINER_CMD" C-m

# Janela 1: Inicia o painel visual
tmux new-window -t $TMUX_SESSION_NAME:1
tmux send-keys -t $TMUX_SESSION_NAME:1 "python3 $DISPLAY_SCRIPT_PATH" C-m

echo "Sessão PiMainer iniciada em segundo plano."

