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

    def _capture_screen_region(self):
        """Capture the region of screen containing the prompt text."""
        # Get the main display
        main_display = Quartz.CGMainDisplayID()
        
        # For now, capture a fixed region - this should be made configurable
        # TODO: Make this region configurable or detect automatically
        x, y = 100, 100  # Starting coordinates
        width, height = 800, 100  # Size of region to capture
        
        # Capture the screen region
        image = Quartz.CGDisplayCreateImageForRect(
            main_display,
            Quartz.CGRectMake(x, y, width, height)
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
