#!/usr/bin/env bash
# Reproduce all FP-13 experiments from scratch.
# Usage: bash reproduce.sh
set -euo pipefail

echo "=== FP-13 Model Behavioral Fingerprinting — Full Reproduction ==="
echo ""

# 1. Run tests
echo "[1/4] Running tests..."
python -m pytest tests/ -v --tb=short
echo ""

# 2. Extract features (synthetic scaffold mode)
echo "[2/4] Extracting features..."
python scripts/extract_features.py --model-dir ./models --output ./outputs/features.npz
echo ""

# 3. Run detection experiments
echo "[3/4] Running detection experiments (30 combinations x 5 seeds)..."
python scripts/run_detection.py --features ./outputs/features.npz --output ./outputs/results.json
echo ""

# 4. Generate figures (stub)
echo "[4/4] Generating figures..."
python scripts/make_report_figures.py --input ./outputs/results.json --output ./outputs/figures/
echo ""

echo "=== Reproduction complete ==="
echo "Results: ./outputs/results.json"
echo "Figures: ./outputs/figures/"
