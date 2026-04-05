"""
PersonaWrite AI — Voice Assistant Module (v3)

STT: OpenAI Whisper (local model, high accuracy)
Recording: Stream-based start/stop via sounddevice.InputStream

Completely decoupled from Streamlit — no UI logic here.
"""

import re
import threading
from typing import Optional, List

import numpy as np
import sounddevice as sd
import whisper


# ===================== WHISPER MODEL (LAZY SINGLETON) =====================

_whisper_model = None


def _get_whisper_model(model_name: str = "base"):
    """
    Load Whisper model once and cache it for the process lifetime.
    Uses 'base' by default — good accuracy, fast on M1/M2 Mac.
    """
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(model_name)
    return _whisper_model


# ===================== STREAM-BASED RECORDER =====================

class StreamRecorder:
    """
    Manages a sounddevice InputStream that continuously captures audio
    into a list of numpy chunks until explicitly stopped.

    Thread-safe: the callback runs on a PortAudio background thread;
    all shared state is guarded by a lock.
    """

    SAMPLE_RATE = 16_000   # Whisper expects 16 kHz
    CHANNELS = 1
    DTYPE = "float32"
    BLOCKSIZE = 1024       # frames per callback (~64 ms at 16 kHz)

    def __init__(self):
        self._chunks: List[np.ndarray] = []
        self._stream: Optional[sd.InputStream] = None
        self._lock = threading.Lock()
        self._is_recording = False

    # ---- public API ----

    @property
    def is_recording(self) -> bool:
        with self._lock:
            return self._is_recording

    def start(self) -> None:
        """Open mic stream and begin collecting audio chunks."""
        with self._lock:
            if self._is_recording:
                return  # already recording — idempotent
            self._chunks.clear()
            self._stream = sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
                dtype=self.DTYPE,
                blocksize=self.BLOCKSIZE,
                callback=self._audio_callback,
            )
            self._stream.start()
            self._is_recording = True

    def stop(self) -> Optional[np.ndarray]:
        """
        Stop recording and return the captured audio as a 1-D float32 array.
        Returns None if no audio was captured.
        """
        with self._lock:
            if not self._is_recording:
                return None

            self._is_recording = False

            if self._stream is not None:
                try:
                    self._stream.stop()
                    self._stream.close()
                except Exception:
                    pass  # stream may already be closed
                self._stream = None

            if not self._chunks:
                return None

            audio = np.concatenate(self._chunks, axis=0).flatten()
            self._chunks.clear()
            return audio

    # ---- internal ----

    def _audio_callback(self, indata, frames, time_info, status):
        """
        Called by PortAudio on its own thread for every audio block.
        Simply stash a copy of the incoming data.
        """
        # No lock needed for append (GIL-safe list.append) but we copy
        # indata because the buffer is reused by PortAudio.
        self._chunks.append(indata.copy())


# Module-level singleton so it survives Streamlit reruns when stored
# in session_state or referenced globally.
_recorder_instance: Optional[StreamRecorder] = None


def get_recorder() -> StreamRecorder:
    """Return the module-level StreamRecorder singleton."""
    global _recorder_instance
    if _recorder_instance is None:
        _recorder_instance = StreamRecorder()
    return _recorder_instance


# ===================== WHISPER TRANSCRIPTION =====================

def transcribe(audio: np.ndarray) -> str:
    """
    Transcribe audio using OpenAI Whisper.

    Args:
        audio: Float32 numpy array of audio samples at 16 kHz.

    Returns:
        Raw transcription text.
    """
    model = _get_whisper_model()
    result = model.transcribe(audio, fp16=False, language="en")
    return result.get("text", "").strip()


# ===================== TEXT CLEANING =====================

def clean_text(raw: str) -> str:
    """
    Remove speech-recognition noise artifacts from transcribed text.

    Handles:
      - Stray dimensional tokens: "1D", "2D", "3D"
      - Isolated single characters/digits
      - Repeated punctuation or random symbols
      - Extra whitespace
    """
    if not raw:
        return ""

    # Remove tokens like "1D", "2D", "3D" (case-insensitive)
    cleaned = re.sub(r'\b\d+[dD]\b', '', raw)

    # Remove isolated single digits
    cleaned = re.sub(r'\b\d\b', '', cleaned)

    # Remove isolated single letters (except "I" and "A")
    cleaned = re.sub(r'\b(?![IAia])[a-zA-Z]\b', '', cleaned)

    # Remove stray symbols that aren't normal punctuation
    cleaned = re.sub(r'[^\w\s.,!?\'\"-]', '', cleaned)

    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


# ===================== LEGACY CONVENIENCE =====================
# Kept for backward compatibility (preset.py might still use it).

def record_audio(duration: int = 8, sample_rate: int = 16000) -> np.ndarray:
    """Record a fixed-duration audio clip (legacy API)."""
    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    return audio_data.flatten()


def listen_speech(duration: int = 8) -> str:
    """Legacy full pipeline: record → transcribe → clean."""
    try:
        audio = record_audio(duration=duration)
        raw_text = transcribe(audio)
        return clean_text(raw_text)
    except Exception:
        return ""