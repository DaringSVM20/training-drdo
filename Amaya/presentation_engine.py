import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from pptx import Presentation
from pptx.util import Pt

from config import config

logger = logging.getLogger("PresentationEngine")

class PresentationEngine:
    """
    Ultra-Simplified PowerPoint Generation Engine.
    Produces plain-text slides with headings and bullet points only.
    """
    def __init__(self):
        self.output_root = Path(config.OUTPUT_ROOT)

    def create_presentation(self, title: str, subtitle: str, slides_data: List[Dict[str, Any]], output_path: Path) -> str:
        """
        Constructs a 100% text-only .pptx file.
        """
        prs = Presentation()

        # 1. Title Slide
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = title
        slide.placeholders[1].text = subtitle

        # 2. Content Slides
        for data in slides_data:
            title_text = data.get("title", "Strategic Insight")
            content = data.get("content", [])
            
            # Use standard Title and Content layout
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = title_text
            
            # Populate text
            body_shape = slide.placeholders[1]
            tf = body_shape.text_frame
            tf.word_wrap = True
            
            for i, bullet in enumerate(content[:10]): # Limit to 10 bullets
                p = tf.paragraphs[i] if i == 0 else tf.add_paragraph()
                # Remove any remaining Markdown characters
                clean_bullet = re.sub(r'^\*\*|\*\*$', '', bullet).strip()
                p.text = clean_bullet
                p.font.size = Pt(18)
                p.level = 0

        # 3. Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(output_path))
        logger.info(f"Simple Presentation generated: {output_path}")
        return str(output_path)

    def parse_llm_summary(self, llm_text: str) -> List[Dict[str, Any]]:
        """
        Robustly parses LLM output into structured slide data.
        Discards conversational filler and cleans up unwanted labels.
        """
        import re
        slides = []
        current_slide = None
        
        # 1. Split into lines and find the first SLIDE: tag
        lines = llm_text.split("\n")
        start_index = -1
        for i, line in enumerate(lines):
            if re.search(r'^\s*(?:\*\*|###)?\s*SLIDE\b', line, re.IGNORECASE):
                start_index = i
                break
        
        if start_index == -1:
            logger.warning("No SLIDE: tags found in LLM output.")
            return []

        # 2. Process only from the first SLIDE: tag onwards
        for line in lines[start_index:]:
            line = line.strip()
            if not line: continue
            
            # Match SLIDE: Title
            header_match = re.search(r'(?:\*\*|###)?\s*SLIDE\s*(?:[0-9]+)?\s*[:\-]*\s*(?:\*\*)?(.*)', line, re.IGNORECASE)
            if header_match:
                if current_slide:
                    slides.append(current_slide)
                
                title = header_match.group(1).strip()
                # Clean up any trailing markdown or image hints like "(Image: ...)"
                title = re.sub(r'\(Image:.*?\)', '', title, flags=re.IGNORECASE)
                title = re.sub(r'^\*\*|\*\*$', '', title).strip()
                if not title: title = "Insight"
                
                current_slide = {"title": title, "content": []}
                continue

            if not current_slide: continue

            # Match Bullet Points or any informative lines
            # Clean up labels like "Headline:", "Impact:", "Key Benefit:", etc.
            clean_line = re.sub(r'^(?:[-*]\s*)?(?:Headline|Impact|Key Benefit|Subtitle|Briefly state|Result|Goal|Bullet Points)\s*[:\-]*\s*', '', line, flags=re.IGNORECASE).strip()
            # Strip leading bullet hyphens or asterisks
            clean_line = re.sub(r'^[-*]\s*', '', clean_line).strip()
            # Remove any remaining Markdown bolding
            clean_line = re.sub(r'^\*\*|\*\*$', '', clean_line).strip()
            # Remove image hints
            clean_line = re.sub(r'\(Image:.*?\)', '', clean_line, flags=re.IGNORECASE).strip()
            # Remove separator lines like "--"
            if clean_line and clean_line != "--":
                current_slide["content"].append(clean_line)
                
        if current_slide:
            slides.append(current_slide)
            
        return slides
