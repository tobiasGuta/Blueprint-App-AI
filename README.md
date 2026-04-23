# Blueprint App

Blueprint App is an AI-assisted electronics design tool for turning a plain-English hardware idea into a structured electronics blueprint.

<img width="1850" height="985" alt="image" src="https://github.com/user-attachments/assets/ebdab65e-8a01-4a4c-8e53-780ea3cfdaa7" />


It generates:

- a validated bill of materials
- live Mouser pricing and availability when configured
- component placements
- wiring connections
- design notes
- an interactive 3D viewer
- an interactive schematic.

The project uses:

- `FastAPI` for the backend
- `LiteLLM` for model routing
- `Pydantic` for schema validation
- `Three.js` for the 3D viewer
- HTML canvas plus plain JavaScript for the schematic renderer
- plain HTML, CSS, and JavaScript for the frontend
- `httpx` for async Mouser API pricing lookups

## What It Does

You enter a prompt such as:

- `Build a racing drone`
- `Create a smart greenhouse controller`
- `Design a robot car with obstacle avoidance`
- `Make a home security control board`

The app asks an LLM to return a structured blueprint with:

- `project_name`
- `project_description`
- `design_notes`
- `bom`
- `placements`
- `connections`

That model output is then validated, cleaned, enriched with local component metadata, auto-laid-out for compact rendering, and shown in multiple views.

## Features

- Multi-model support through LiteLLM
- Claude, GPT-4o, and Gemini model options
- Strict JSON schema validation
- Automatic fallback from tool-calling to plain JSON mode
- Truncated JSON repair and root extraction
- Compact PCB-style auto-layout pass on the frontend
- X-ray style 3D viewer with category layers
- Interactive canvas-based wiring diagram with draggable components
- BOM stats, live Mouser pricing, datasheet/product links, and CSV export

## Architecture

### Backend

The backend is implemented in `main.py`.

Responsibilities:

- define the blueprint schema
- build the system prompt
- call the selected model through LiteLLM
- recover from malformed model responses
- validate and sanitize the returned blueprint
- enrich placements and BOM rows with component metadata
- enrich BOM rows with cached Mouser pricing and availability data when `MOUSER_API_KEY` is set
- serve API endpoints and the frontend

API endpoints:

- `POST /api/generate`
- `GET /api/components`

### Component Catalog

The source of truth for components lives in `components.py`.

Each component entry includes:

- name
- category
- description
- dimensions
- color
- pins
- Mouser search keywords

The model is instructed to use only component IDs from this catalog.

### Frontend

The entire frontend lives in `static/index.html`.

It includes:

- prompt UI
- model selector
- loading overlay
- project summary card
- 3D visualization
- schematic visualization
- BOM table with live pricing, stock status, and links
- CSV export

## Generation Flow

### 1. Prompt entry

The user enters a project description and chooses a model.

### 2. System prompt generation

`build_system_prompt()` injects:

- component catalog restrictions
- wiring rules
- placement rules
- compact PCB placement guidance

### 3. First model call

The backend calls `litellm.completion()` with:

- a system prompt
- the user prompt
- the blueprint tool schema
- `tool_choice="auto"`

### 4. Automatic fallback

If the provider returns no usable tool call or no usable content, the backend retries without tools and asks for raw JSON only.

### 5. Response recovery

Before validation, the backend can:

- strip markdown fences
- repair truncated JSON
- locate the real blueprint root inside nested responses

### 6. Validation and cleanup

The response is validated with:

- `Blueprint`
- `BOMItem`
- `ComponentPlacement`
- `WireConnection`

Cleanup includes:

- dropping malformed connections
- tolerating partially missing wire fields
- correcting bad instance references when possible
- removing unusable connections before response return

### 7. Enrichment

The backend attaches:

- component dimensions
- colors
- categories
- pins
- category labels and icons
- Mouser pricing, availability, and external links when configured

### 8. Frontend layout and rendering

Before rendering, the frontend runs `autoLayout()` to cluster placements around the primary microcontroller in a compact board-style arrangement.

The same post-layout placements feed both:

- the 3D viewer
- the schematic wiring diagram

## 3D Viewer

The 3D tab is built with Three.js.

Current characteristics:

- dark X-ray CAD style scene
- `CSS2DRenderer` HTML labels
- compact component grouping
- dimension lines and labels
- curved wire tubes between component centers
- electrical layer visibility toggles by category

Visible categories can include:

- `microcontroller`
- `sensor`
- `communication`
- `display`
- `power`
- `actuator`
- `passive`

## Schematic View

The schematic tab is now built as a custom canvas-based wiring diagram.

It renders:

- draggable component cards grouped by category
- only the pins that are actually used by the blueprint connections
- curved bezier wire paths between pins or fallback component anchors
- semantic wire coloring for power, ground, UART, PWM, analog, and signal/data lines
- inline wire labels when available
- pin hover tooltips
- click-to-highlight nets
- a net-color legend

The schematic builder also includes defensive pin matching and component-card fallback logic so slightly mismatched pin names do not prevent connection rendering.

## BOM View

The BOM tab shows:

- category badges
- component names and descriptions
- quantities
- Mouser part numbers
- stock availability
- live unit pricing and total pricing
- datasheet and product links
- summary stat cards
- CSV export

## Model Support

The current UI model list includes:

- `claude-sonnet-4-6`
- `claude-opus-4-6`
- `claude-haiku-4-5-20251001`
- `gpt-4o`
- `gemini/gemini-2.5-flash`
- `gemini/gemini-1.5-pro`

The backend also normalizes older Gemini Flash references to the new prefixed format.

## Reliability Notes

The app includes several safeguards for real-world model behavior:

- handles empty `choices`
- accepts tool-call output or plain JSON content
- retries without tools for provider compatibility
- repairs truncated JSON
- extracts the correct blueprint root from wrapped responses
- avoids crashes from malformed connection objects
- prevents duplicate frontend submissions while a request is already running

## Setup

### Requirements

Install dependencies from `requirements.txt`.

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and provide one provider key. Add a Mouser API key as well if you want live BOM pricing and stock availability.

Supported keys:

- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `MOUSER_API_KEY`

### 4. Run the server

```bash
python main.py
```

Open:

```text
http://localhost:8000
```

## API

### `POST /api/generate`

Request:

```json
{
  "prompt": "Build a smart greenhouse controller with automatic irrigation",
  "model": "claude-sonnet-4-6"
}
```

Response includes:

- `project_name`
- `project_description`
- `design_notes`
- `bom`
- `placements`
- `connections`
- `category_meta`

Each BOM item may also include live Mouser fields such as:

- `unit_cost_usd`
- `mouser_pn`
- `mfr_pn`
- `availability`
- `datasheet_url`
- `product_url`
- `image_url`

### `GET /api/components`

Returns the component catalog without pin lists.

## Project Structure

```text
.
├── main.py
├── components.py
├── requirements.txt
├── .env.example
├── static/
│   └── index.html
├── README.md
├── CONTRIBUTOR.md
└── LICENSE
```

#### Screenshot

<img width="1850" height="985" alt="image" src="https://github.com/user-attachments/assets/e2b75317-e734-43b7-b696-b1d2ac933b4c" />

----

<img width="1850" height="985" alt="Screenshot From 2026-04-21 22-16-33" src="https://github.com/user-attachments/assets/f1c114a2-67c6-430e-b4f3-ece22d3d6df6" />

----

<img width="1513" height="925" alt="image" src="https://github.com/user-attachments/assets/880d0d47-cf4e-4fb2-89db-79fc205650dd" />


----

<img width="1867" height="982" alt="image" src="https://github.com/user-attachments/assets/6f80694e-9a39-4983-a3de-1a0c6a7643a2" />

---- 

https://github.com/user-attachments/assets/0f31b12d-e2ea-4d6e-a076-273fa3029fae


## Limitations

- This is concept and planning tooling, not manufacturing output
- The schematic is a systems diagram, not an EDA-native design file
- Routing and spatial layout are visual approximations
- Costs and stock data depend on Mouser API results when enabled
- Results still depend heavily on prompt quality

## Extending The Project

Common improvements:

- add more parts to `components.py`
- tune the system prompt in `main.py`
- add more models to the selector
- improve the component catalog metadata
- add persistence or export formats
- add test coverage around blueprint parsing and validation

## Developer Notes

- The frontend is intentionally kept in one HTML file for simplicity
- The backend serves the frontend directly through `StaticFiles`
- If you change the schema, update both the tool schema and the Pydantic models
- If you add categories, update backend metadata and frontend rendering logic together

## License

This repository now includes an MIT license in `LICENSE`.
