def generate_preset(prompt: str, preset: str) -> str:
    style_prompts = {
        "casual": f"Write casually: {prompt}",
        "academic": f"Write academically: {prompt}",
        "formal": f"Write formally: {prompt}"
    }
    return style_prompts.get(preset, prompt)
