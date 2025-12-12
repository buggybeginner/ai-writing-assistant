import json
import time
import streamlit as st
from datetime import datetime

class MockAPIClient:
    """Mock API client for frontend development"""
    
    @staticmethod
    def analyze_writing_style(texts):
        """Simulate style analysis"""
        time.sleep(1.5)
        
        return {
            "formality_score": 72,
            "emotional_tone": "positive",
            "sentence_complexity": "medium",
            "vocabulary_richness": "high",
            "common_phrases": ["just wanted to", "thanks so much", "let me know"],
            "signature_words": ["awesome", "actually", "basically"],
            "punctuation_habits": {"exclamations": 3, "emojis": 2, "ellipsis": 1}
        }
    
    @staticmethod
    def generate_text(prompt, personality, creativity=0.7):
        """Simulate text generation"""
        time.sleep(1.0)
        
        responses = {
            "casual_friendly": f"Hey! So I was thinking about '{prompt}' and honestly, it's a great idea! 😊 Let's dive in and see where it takes us. What do you think?",
            "corporate_professional": f"Regarding the matter of '{prompt}', a comprehensive analysis suggests proceeding with structured implementation. Further discussion would be beneficial.",
            "formal_academic": f"This examination of '{prompt}' reveals several pertinent considerations. The evidence suggests methodological approaches warrant further investigation.",
            "motivational_speaker": f"Imagine what we could achieve with '{prompt}'! This isn't just an opportunity—it's our calling to make a difference! 🚀"
        }
        
        return responses.get(personality, f"Generated text about: {prompt}")
    
    @staticmethod
    def blend_styles(personal_style, preset_style, ratio):
        """Simulate style blending"""
        time.sleep(2.0)
        
        return {
            "blended_output": f"This text blends {ratio*100}% personal style with {(1-ratio)*100}% {preset_style} style.",
            "consistency_score": 85,
            "unique_phrases": ["combined approach", "hybrid tone", "balanced expression"]
        }