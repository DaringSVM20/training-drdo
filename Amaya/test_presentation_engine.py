import unittest
import sys
from pathlib import Path
import tempfile
import re

# Add the Amaya folder to sys.path so we can import dependencies
sys.path.append(str(Path(__file__).parent))

from presentation_engine import PresentationEngine
from presentation_themes import THEMES, get_theme, get_theme_by_display_name, get_theme_names, DEFAULT_THEME


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
        """Basic file creation test (default theme)."""
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

    # ---- Phase 1: Theme tests ----

    def test_themed_presentation_all_themes(self):
        """Each theme should generate a valid, non-empty .pptx file."""
        slides_data = [
            {"title": "Overview", "content": ["Point one", "Point two", "Point three"]}
        ]
        for theme_name in THEMES:
            with self.subTest(theme=theme_name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    out_path = Path(tmpdir) / f"test_{theme_name}.pptx"
                    result_path = self.pe.create_presentation(
                        title=f"Test: {theme_name}",
                        subtitle="Automated Theme Test",
                        slides_data=slides_data,
                        output_path=out_path,
                        theme_name=theme_name
                    )
                    self.assertTrue(Path(result_path).exists(),
                                    f"File not created for theme '{theme_name}'")
                    self.assertGreater(Path(result_path).stat().st_size, 0,
                                       f"Empty file for theme '{theme_name}'")

    def test_themed_presentation_by_display_name(self):
        """Themes should also resolve by display name (user-facing)."""
        slides_data = [
            {"title": "Display Name Test", "content": ["Bullet A"]}
        ]
        for display_name in get_theme_names():
            with self.subTest(display_name=display_name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    out_path = Path(tmpdir) / "test_display.pptx"
                    result_path = self.pe.create_presentation(
                        title="Display Name Test",
                        subtitle="Test",
                        slides_data=slides_data,
                        output_path=out_path,
                        theme_name=display_name
                    )
                    self.assertTrue(Path(result_path).exists())

    def test_theme_fallback(self):
        """Invalid theme name should fall back to default without error."""
        slides_data = [
            {"title": "Fallback Test", "content": ["Bullet X"]}
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "test_fallback.pptx"
            result_path = self.pe.create_presentation(
                title="Fallback Test",
                subtitle="Invalid theme",
                slides_data=slides_data,
                output_path=out_path,
                theme_name="nonexistent_theme_xyz"
            )
            self.assertTrue(Path(result_path).exists())
            self.assertGreater(Path(result_path).stat().st_size, 0)

    def test_continuation_slides(self):
        """15 bullets should auto-split into multiple slides with cont'd titles."""
        from pptx import Presentation as PptxPresentation
        
        bullets = [f"Bullet {i+1}" for i in range(15)]
        slides_data = [{"title": "Many Bullets", "content": bullets}]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "test_overflow.pptx"
            self.pe.create_presentation(
                title="Overflow Test",
                subtitle="Test",
                slides_data=slides_data,
                output_path=out_path,
                theme_name="corporate_navy"
            )
            
            # Read the generated file and count slides
            prs = PptxPresentation(str(out_path))
            # 1 title slide + ceil(15/6) = 3 content slides = 4 total
            self.assertEqual(len(prs.slides), 4)


class TestPresentationThemes(unittest.TestCase):
    """Tests for the theme configuration module."""

    def test_all_themes_have_required_fields(self):
        for name, theme in THEMES.items():
            with self.subTest(theme=name):
                self.assertIsNotNone(theme.primary_color)
                self.assertIsNotNone(theme.secondary_color)
                self.assertIsNotNone(theme.accent_color)
                self.assertIsNotNone(theme.bg_color)
                self.assertIsNotNone(theme.title_font)
                self.assertIsNotNone(theme.body_font)
                self.assertTrue(len(theme.display_name) > 0)

    def test_get_theme_by_name(self):
        theme = get_theme("corporate_navy")
        self.assertEqual(theme.name, "corporate_navy")

    def test_get_theme_by_display_name(self):
        theme = get_theme_by_display_name("Emerald Executive")
        self.assertEqual(theme.name, "emerald_executive")

    def test_get_theme_fallback(self):
        theme = get_theme("does_not_exist")
        self.assertEqual(theme.name, DEFAULT_THEME)

    def test_get_theme_names_returns_all(self):
        names = get_theme_names()
        self.assertEqual(len(names), len(THEMES))

    def test_minimum_theme_count(self):
        """We require at least 4 themes as per spec."""
        self.assertGreaterEqual(len(THEMES), 4)


if __name__ == "__main__":
    unittest.main()
