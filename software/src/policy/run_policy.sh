#!/usr/bin/env bash
# Run a trained policy on XLeRobot in sim (or real) from a YAML config.
# Usage: ./run_policy.sh [policy_config.yaml] [extra run_policy.py flags...]
#   ./run_policy.sh                                   # default config, headless
#   ./run_policy.sh configs/policy_act_pick_place.yaml --viewer
set -euo pipefail

# Force system NVIDIA GL over the conda mesa libGL in the sim env (else the Genesis
# renderer segfaults in PyOpenGL). Harmless for the real-robot path.
SYS_GL=/usr/lib/x86_64-linux-gnu
export LD_PRELOAD="$SYS_GL/libGLdispatch.so.0:$SYS_GL/libGLX.so.0:$SYS_GL/libGL.so.1"
export DISPLAY="${DISPLAY:-:1}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${1:-$SCRIPT_DIR/configs/policy_act_pick_place.yaml}"
shift || true

exec "$HOME/miniconda3/envs/xlerobot-sim/bin/python" "$SCRIPT_DIR/run_policy.py" "$CONFIG" "$@"
