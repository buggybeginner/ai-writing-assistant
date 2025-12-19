from backend.preset_generator import generate_preset
from backend.generator import generate_with_style

def generate_side_by_side(prompt: str, preset: str, style_profile: dict):
    preset_output = generate_preset(prompt, preset)
    personal_output = generate_with_style(prompt, style_profile)

    return {
        "preset": preset_output,
        "personal": personal_output
    }
