# Contributor Guide

## Overview

This project is a compact full-stack app:

- `main.py` contains the FastAPI backend and model orchestration
- `components.py` contains the component catalog
- `static/index.html` contains the full frontend

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Contribution Principles

- keep changes focused and easy to review
- do not break the existing schema contract
- preserve the separation between backend validation and frontend rendering
- prefer defensive handling for model-output edge cases

## Backend Notes

When editing `main.py`:

- keep `Blueprint`, `BOMItem`, `ComponentPlacement`, and `WireConnection` aligned with the model tool schema
- maintain provider compatibility in `/api/generate`
- prefer clean `HTTPException` errors over raw exceptions

## Frontend Notes

When editing `static/index.html`:

- keep IDs used by JavaScript stable
- avoid breaking `handleGenerate()`, `autoLayout()`, `buildScene()`, `buildSchematic()`, or `buildBOM()`
- keep schematic-only changes out of the 3D path and vice versa unless the change truly spans both

## Component Catalog Changes

When adding components to `components.py`:

- include realistic dimensions
- provide a useful description
- define the correct category
- include accurate pin names

## Suggested Workflow

1. Make a small change.
2. Run the app locally.
3. Test prompt submission.
4. Verify 3D view, schematic, and BOM all still render.
5. Check the browser console for frontend errors.
6. Check the backend logs for parsing or validation issues.

## Pull Request Checklist

- code runs locally
- no obvious frontend console errors
- no backend tracebacks for normal usage
- docs updated when behavior changes
- schema changes reflected everywhere they need to be
