.PHONY: scan train-detector test serve figures clean lint

scan:
	python scripts/extract_features.py --model-dir ./models --output ./outputs/features.npz

train-detector:
	python scripts/run_detection.py --features ./outputs/features.npz --output ./outputs/results.json

test:
	python -m pytest tests/ -v --tb=short

serve:
	uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload

figures:
	python scripts/make_report_figures.py --input ./outputs/results.json --output ./outputs/figures/

clean:
	rm -rf outputs/*.npz outputs/*.json outputs/figures/ __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

lint:
	python -m py_compile src/trust_score.py
	python -m py_compile src/extraction/activation_extractor.py
	python -m py_compile src/detectors/isolation_forest.py
