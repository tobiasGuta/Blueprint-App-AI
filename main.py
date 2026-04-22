"""
AI-Powered 3D Electronics Blueprint Generator — Backend
Uses LiteLLM (multi-provider abstraction) + Pydantic for strict JSON validation.
"""

import json
import logging
import os
import re
from typing import Any, List, Optional

import litellm
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator, model_validator

from components import CATEGORY_META, COMPONENT_DATABASE

load_dotenv()
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Electronics Blueprint Generator", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────

class BOMItem(BaseModel):
    component_id: str
    name: str
    quantity: int
    unit_cost_usd: Optional[float] = None
    description: str

    @field_validator("quantity")
    @classmethod
    def qty_positive(cls, v):
        if v < 1:
            raise ValueError("quantity must be ≥ 1")
        return v


class ComponentPlacement(BaseModel):
    component_id: str
    instance_id: str
    label: str
    x: float
    y: float
    z: float
    rotation_y: float = 0.0


class WireConnection(BaseModel):
    from_instance: str = ""
    from_pin: str = ""
    to_instance: str = ""
    to_pin: str = ""
    wire_color: str = "#888888"
    signal_name: Optional[str] = None


class Blueprint(BaseModel):
    project_name: str
    project_description: str
    design_notes: str
    bom: List[BOMItem]
    placements: List[ComponentPlacement]
    connections: List[WireConnection]

    @model_validator(mode="before")
    @classmethod
    def sanitize_connections(cls, data):
        if not isinstance(data, dict):
            return data

        raw_connections = data.get("connections")
        if not isinstance(raw_connections, list):
            return data

        required_keys = {"from_instance", "from_pin", "to_instance", "to_pin"}
        cleaned_connections = []

        for idx, item in enumerate(raw_connections):
            if not isinstance(item, dict):
                logger.warning("Skipping malformed connection at index %s: expected dict, got %s", idx, type(item).__name__)
                continue

            missing_count = sum(1 for key in required_keys if key not in item)
            if missing_count > 2:
                logger.warning(
                    "Skipping malformed connection at index %s: missing %s required keys",
                    idx,
                    missing_count,
                )
                continue

            cleaned_connections.append(item)

        data["connections"] = cleaned_connections
        return data

    @model_validator(mode="after")
    def cross_validate(self):
        ids = {p.instance_id for p in self.placements}
        cleaned_connections = []

        for c in self.connections:
            if c.from_instance not in ids:
                # Silently fix bad references instead of crashing
                c.from_instance = list(ids)[0] if ids else c.from_instance
            if c.to_instance not in ids:
                c.to_instance = list(ids)[0] if ids else c.to_instance
            if any(value in ("", None) for value in (c.from_instance, c.to_instance, c.from_pin, c.to_pin)):
                continue
            cleaned_connections.append(c)

        self.connections = cleaned_connections
        return self


REQUIRED_BLUEPRINT_KEYS = {
    "project_name",
    "project_description",
    "design_notes",
    "bom",
    "placements",
    "connections",
}


def extract_blueprint_root(parsed: Any) -> dict:
    def is_blueprint_dict(value: Any) -> bool:
        return isinstance(value, dict) and REQUIRED_BLUEPRINT_KEYS.issubset(value.keys())

    found_keys = []

    if isinstance(parsed, dict):
        found_keys = sorted(parsed.keys())
        if "bom" in parsed:
            return parsed
        if is_blueprint_dict(parsed):
            return parsed
        for value in parsed.values():
            if is_blueprint_dict(value):
                return value
    elif isinstance(parsed, list):
        found_keys = [sorted(item.keys()) if isinstance(item, dict) else type(item).__name__ for item in parsed]
        for item in parsed:
            if is_blueprint_dict(item):
                return item

    raise HTTPException(
        status_code=500,
        detail=f"Could not locate blueprint root in model response. Found keys: {found_keys}",
    )


def repair_truncated_json(raw: str) -> str:
    stack = []
    in_string = False
    escape = False

    for char in raw:
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            stack.append("}")
        elif char == "[":
            stack.append("]")
        elif char in {"}", "]"} and stack and stack[-1] == char:
            stack.pop()

    repaired = raw
    if in_string:
        repaired += '"'
    if stack:
        repaired += "".join(reversed(stack))
    return repaired


# ─── LiteLLM Tool Schema ──────────────────────────────────────────────────────

BLUEPRINT_TOOL = {
    "type": "function",
    "function": {
        "name": "generate_blueprint",
        "description": (
            "Generate a complete, production-ready electronics blueprint with a "
            "bill of materials, 3D spatial component placements, and pin-to-pin wiring."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "project_name":        {"type": "string"},
                "project_description": {"type": "string"},
                "design_notes":        {"type": "string", "description": "Power budget, key design decisions, warnings"},
                "bom": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "component_id":  {"type": "string"},
                            "name":          {"type": "string"},
                            "quantity":      {"type": "integer", "minimum": 1},
                            "unit_cost_usd": {"type": "number"},
                            "description":   {"type": "string"},
                        },
                        "required": ["component_id", "name", "quantity", "description"],
                    },
                },
                "placements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "component_id": {"type": "string"},
                            "instance_id":  {"type": "string"},
                            "label":        {"type": "string"},
                            "x":            {"type": "number", "description": "X in cm, range -35 to 35"},
                            "y":            {"type": "number", "description": "Y in cm, range 0 to 10"},
                            "z":            {"type": "number", "description": "Z in cm, range -35 to 35"},
                            "rotation_y":   {"type": "number", "description": "Y-axis rotation in degrees"},
                        },
                        "required": ["component_id", "instance_id", "label", "x", "y", "z"],
                    },
                },
                "connections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "from_instance": {"type": "string"},
                            "from_pin":      {"type": "string"},
                            "to_instance":   {"type": "string"},
                            "to_pin":        {"type": "string"},
                            "wire_color":    {"type": "string", "description": "Hex: red=power, black=GND, yellow=PWM/signal, blue=I2C/SPI, green=analog"},
                            "signal_name":   {"type": "string"},
                        },
                        "required": ["from_instance", "from_pin", "to_instance", "to_pin", "wire_color"],
                    },
                },
            },
            "required": ["project_name", "project_description", "design_notes", "bom", "placements", "connections"],
        },
    },
}


def build_system_prompt() -> str:
    lines = ["You are a senior electrical engineer. Design complete, safe, working electronics systems."]
    lines.append("\nCOMPONENT CATALOG — use ONLY the following component_ids:")
    for cid, comp in COMPONENT_DATABASE.items():
        pin_preview = ", ".join(comp["pins"][:6])
        if len(comp["pins"]) > 6:
            pin_preview += f" … (+{len(comp['pins'])-6})"
        lines.append(f"  • {cid}: {comp['name']} | {comp['description']} | Pins: {pin_preview}")

    lines.append("""
DESIGN RULES:
1. Select realistic components — every component must serve a clear function.
2. Include power management (battery, regulator, or PDB as appropriate).
3. Wire ALL power pins (VCC/5V/3.3V) to the correct supply voltage.
4. Wire ALL GND pins to ground.
5. Use correct interface protocols: I2C (SCL/SDA), SPI (SCK/MOSI/MISO/CS), UART (TX→RX), PWM, ADC.
6. Generate 12–25 wiring connections minimum.
7. Wire colors: "#ff3333"=power, "#222222"=GND, "#ffcc00"=PWM/signal, "#3399ff"=I2C/SPI, "#33ff88"=analog, "#ffffff"=UART/data.
8. For multi-unit items (4 motors, 4 ESCs), create separate instance_ids: motor_1 … motor_4.
9. PLACEMENT RULES: You are placing components on a compact custom PCB. The total board must fit within a 120mm × 120mm area (12 units × 12 units in your coordinate system where 1 unit = 1 cm).
10. Place the primary microcontroller at exactly x=0, y=0, z=0.
11. Place all other components tightly around it. Sensors go behind (positive Z), actuators go to the right (positive X), power components go to the left (negative X), communication modules go in front (negative Z), displays go top-right diagonal.
12. Maximum allowed coordinate values: x between -8 and 8, z between -8 and 8. Never exceed these bounds.
13. Space components just enough to avoid overlap: use their actual dimensions to calculate clearance. A component that is 4cm wide needs at least 2cm clearance from its neighbor (half its width plus half the neighbor's width plus 0.5cm gap).
14. Keep y=0 for all components so they sit flat on the board. Only stack components (y > 0) if one physically mounts on top of another.
15. Do not place all components in a single straight line. Distribute them in a 2D cluster around the microcontroller.
16. ALL component_ids in bom/placements/connections MUST exist in the catalog above. No hallucinated IDs.
""")
    return "\n".join(lines)


# ─── API Request Model ────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "claude-sonnet-4-6"


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@app.post("/api/generate")
async def generate_blueprint(req: GenerateRequest):
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="No API key found. Add ANTHROPIC_API_KEY (or OPENAI_API_KEY / GEMINI_API_KEY) to your .env file.",
        )

    system_prompt = build_system_prompt()
    model_name = req.model
    if model_name in {"gemini-1.5-flash", "gemini/gemini-1.5-flash"}:
        model_name = "gemini/gemini-2.5-flash"
    user_prompt = f"Design this electronics project: {req.prompt}"
    json_retry_prompt = (
        f"{user_prompt}\n\n"
        "Respond with only a raw JSON object matching this blueprint schema: "
        "project_name, project_description, design_notes, bom, placements, connections. "
        "Do not include markdown fences, commentary, or any text outside the JSON object."
    )

    try:
        response = litellm.completion(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            tools=[BLUEPRINT_TOOL],
            tool_choice="auto",
            max_tokens=8192,
            temperature=0.1,
        )
        raw = None

        if response.choices:
            msg = response.choices[0].message

            if msg.tool_calls:
                first_tool_call = msg.tool_calls[0]
                if getattr(first_tool_call, "function", None) and first_tool_call.function.arguments:
                    raw = first_tool_call.function.arguments

            if raw is None and msg.content:
                raw = msg.content

        if raw is None:
            retry_response = litellm.completion(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json_retry_prompt},
                ],
                max_tokens=8192,
                temperature=0.1,
            )

            if not retry_response.choices:
                raise HTTPException(
                    status_code=500,
                    detail="Model returned no choices, even after retrying without tools.",
                )

            retry_msg = retry_response.choices[0].message
            if retry_msg.content:
                raw = retry_msg.content

        if raw is None:
            raise HTTPException(
                status_code=500,
                detail="Model returned neither tool call arguments nor text content with blueprint JSON, including after retrying without tools.",
            )

        # Handle potential JSON wrapped in markdown fences
        raw = re.sub(r"^```json\s*|\s*```$", "", raw.strip())
        repaired_raw = repair_truncated_json(raw)
        try:
            parsed = json.loads(repaired_raw)
        except json.JSONDecodeError as e:
            preview = raw[:300]
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse model JSON after repair attempt: {e}. Raw response starts with: {preview}",
            )
        data = extract_blueprint_root(parsed)

    except HTTPException:
        raise
    except litellm.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid API key. Check your .env file.")
    except litellm.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded — try again shortly.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # ── Pydantic validation ──
    try:
        blueprint = Blueprint(**data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Blueprint validation failed: {e}")

    result = blueprint.model_dump()

    # ── Enrich placements with component metadata ──
    for placement in result["placements"]:
        cid = placement["component_id"]
        comp = COMPONENT_DATABASE.get(cid)
        if comp:
            placement["dimensions"] = comp["dimensions"]
            placement["color"]      = comp["color"]
            placement["pins"]       = comp["pins"]
            placement["category"]   = comp["category"]
        else:
            # Fallback for unknown component IDs (model hallucination)
            placement["dimensions"] = {"w": 4, "h": 1, "d": 4}
            placement["color"]      = "#888888"
            placement["pins"]       = []
            placement["category"]   = "passive"

    # ── Enrich BOM with metadata ──
    for item in result["bom"]:
        cid  = item["component_id"]
        comp = COMPONENT_DATABASE.get(cid)
        if comp:
            item["category"] = comp["category"]
            item["color"]    = comp["color"]
            meta = CATEGORY_META.get(comp["category"], {})
            item["category_label"] = meta.get("label", comp["category"])
            item["icon"]           = meta.get("icon", "🔧")

    result["category_meta"] = CATEGORY_META
    return result


@app.get("/api/components")
async def list_components():
    return {
        cid: {k: v for k, v in comp.items() if k != "pins"}
        for cid, comp in COMPONENT_DATABASE.items()
    }


# ── Serve the frontend ────────────────────────────────────────────────────────
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
