import unittest
import sys
from pathlib import Path
import tempfile
import re

# Add the Amaya folder to sys.path so we can import dependencies
sys.path.append(str(Path(__file__).parent))

from presentation_engine import PresentationEngine

class TestPresentationEngine(unittest.TestCase):
    def setUp(self):
        self.pe = PresentationEngine()

    def test_parse_standard_slides(self):
        llm_text = """
Some general intro text from LLM.

SLIDE: First slide
- This is bullet 1
- This is bullet 2

SLIDE: Second slide
- Bullet A
- Bullet B
"""
        slides = self.pe.parse_llm_summary(llm_text)
        self.assertEqual(len(slides), 2)
        self.assertEqual(slides[0]["title"], "First slide")
        self.assertEqual(slides[0]["content"], ["This is bullet 1", "This is bullet 2"])
        self.assertEqual(slides[1]["title"], "Second slide")
        self.assertEqual(slides[1]["content"], ["Bullet A", "Bullet B"])

    def test_parse_numbered_slides(self):
        llm_text = """
SLIDE 1: Exec Summary
- Key point 1
- Key point 2

SLIDE 2: Details
- Detail A
"""
        slides = self.pe.parse_llm_summary(llm_text)
        self.assertEqual(len(slides), 2)
        self.assertEqual(slides[0]["title"], "Exec Summary")
        self.assertEqual(slides[0]["content"], ["Key point 1", "Key point 2"])

    def test_parse_markdown_slides(self):
        llm_text = """
Some conversational filler...

### SLIDE 1: Technical Depth
- Bullet one
- Bullet two

**SLIDE 2: Conclusion**
- Bullet three
"""
        slides = self.pe.parse_llm_summary(llm_text)
        self.assertEqual(len(slides), 2)
        self.assertEqual(slides[0]["title"], "Technical Depth")
        self.assertEqual(slides[0]["content"], ["Bullet one", "Bullet two"])
        self.assertEqual(slides[1]["title"], "Conclusion")
        self.assertEqual(slides[1]["content"], ["Bullet three"])

    def test_parse_no_delimiters(self):
        llm_text = """
Hello world, no slide tags here.
"""
        slides = self.pe.parse_llm_summary(llm_text)
        self.assertEqual(len(slides), 0)

    def test_create_presentation(self):
        slides_data = [
            {"title": "Test Title", "content": ["Bullet 1", "Bullet 2"]}
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "test_pres.pptx"
            result_path = self.pe.create_presentation(
                title="Mock Presentation",
                subtitle="For testing",
                slides_data=slides_data,
                output_path=out_path
            )
            self.assertTrue(Path(result_path).exists())
            self.assertTrue(Path(result_path).stat().st_size > 0)

if __name__ == "__main__":
    unittest.main()
