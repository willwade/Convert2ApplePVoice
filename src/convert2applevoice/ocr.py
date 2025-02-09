"""OCR module for extracting text from Personal Voice UI."""

from pathlib import Path
import Quartz
from Vision import VNRecognizeTextRequest, VNImageRequestHandler
from AppKit import NSBitmapImageRep

class OCRExtractor:
    """Handles OCR text extraction using Apple's Vision framework."""

    def __init__(self):
        """Initialize the OCR extractor."""
        self.request = VNRecognizeTextRequest.alloc().init()
        self.request.setRecognitionLevel_(1)  # Accurate
        self.request.setUsesLanguageCorrection_(True)
        self.request.setRecognitionLanguages_(["en"])
        
        # Get the main display once
        self.main_display = Quartz.CGMainDisplayID()
        
        # Default capture region - can be adjusted via config
        self.region = {
            'x': 100,      # Starting x coordinate
            'y': 300,      # Starting y coordinate (adjusted for phrase area)
            'width': 800,  # Width of capture
            'height': 100  # Height of capture
        }

    def set_capture_region(self, x: int, y: int, width: int, height: int):
        """Update the screen region to capture.
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
            width: Width of region to capture
            height: Height of region to capture
        """
        self.region = {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }

    def _capture_screen_region(self):
        """Capture the region of screen containing the prompt text."""
        # Capture the screen region
        image = Quartz.CGDisplayCreateImageForRect(
            self.main_display,
            Quartz.CGRectMake(
                self.region['x'],
                self.region['y'],
                self.region['width'],
                self.region['height']
            )
        )
        
        return image

    def extract_text(self) -> str:
        """Extract text from the captured screen region.
        
        Returns:
            str: The extracted text, or empty string if extraction failed.
        """
        try:
            # Capture the screen region
            image = self._capture_screen_region()
            if not image:
                return ""

            # Create image request handler
            handler = VNImageRequestHandler.alloc().initWithCGImage_options_(
                image, None
            )

            # Perform the text recognition
            handler.performRequests_error_([self.request], None)

            # Get the results
            results = self.request.results()
            if not results:
                return ""

            # Get the text from the first (usually only) result
            text = results[0].topCandidates_(1)[0].string()
            return text.strip()

        except Exception as e:
            print(f"Error during OCR: {str(e)}")
            return ""
