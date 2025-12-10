# main.py - CORRECT VERSION
from fastapi import FastAPI
from pydantic import BaseModel  # FIXED: pydantic NOT pydbmtic
from fastapi.middleware.cors import CORSMiddleware  # FIXED: cors NOT core, CORSMiddleware NOT CDRSMiddleware

# Request Model
class GenerateRequest(BaseModel):
    text: str
    style: str = "formal"  # Default value

# Response Model  
class GenerateResponse(BaseModel):
    original_text: str
    styled_text: str
    style_used: str

app = FastAPI(title="AI Writing Backend", version="1.0")

# CORS - Keep as is, it's correct
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Improved styling function
def apply_style(text: str, style: str) -> str:
    styles = {
        "formal": f"Formal version:\n\n{text}\n\nRespectfully submitted.",
        "friendly": f"Hey there! 😊\n\n{text}\n\nHope that helps!",
        "academic": f"Academic analysis:\n\n{text}\n\n(Source: Required)",
        "business": f"Business communication:\n\n{text}\n\nBest regards,\nTeam",
        "creative": f"Creative writing:\n✨ {text} ✨\n\nThe story continues..."
    }
    return styles.get(style, text)

@app.get("/")
def root():
    return {"message": "AI Writing Backend v1.0", "docs": "/docs", "health": "ok"}

@app.post("/generate")
def generate_text(body: GenerateRequest):
    styled = apply_style(body.text, body.style)
    return GenerateResponse(
        original_text=body.text,
        styled_text=styled,
        style_used=body.style
    )
# Add after existing routes:

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-15T10:30:00Z"}

@app.get("/styles")
def list_styles():
    return {
        "available_styles": [
            {"id": "formal", "name": "Formal", "description": "Professional writing"},
            {"id": "friendly", "name": "Friendly", "description": "Casual tone"},
            {"id": "academic", "name": "Academic", "description": "Research style"}
        ]
    }