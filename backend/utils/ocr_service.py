"""
OCR Service for extracting text from images and PDFs
Uses Tesseract OCR with fallback options
"""

import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import io
import os
from typing import List, Dict, Any

class OCRService:
    """OCR service for document text extraction"""
    
    def __init__(self):
        # Set tesseract path if needed (usually auto-detected)
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        pass
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='eng')
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from image: {str(e)}")
    
    def extract_text_from_image_bytes(self, image_bytes: bytes) -> str:
        """
        Extract text from image bytes
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            Extracted text
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image, lang='eng')
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from image bytes: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path: str, max_pages: int = None) -> str:
        """
        Extract text from PDF file by converting to images and OCR
        
        Args:
            pdf_path: Path to PDF file
            max_pages: Maximum number of pages to process (None for all)
            
        Returns:
            Extracted text from all pages
        """
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            if max_pages:
                images = images[:max_pages]
            
            # Extract text from each page
            full_text = []
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image, lang='eng')
                full_text.append(f"--- Page {i+1} ---\n{page_text}")
            
            return "\n\n".join(full_text)
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_text_with_confidence(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text with confidence scores
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with text and confidence data
        """
        try:
            image = Image.open(image_path)
            
            # Get detailed OCR data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang='eng')
            
            # Extract text with confidence
            text_blocks = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 0:  # Filter out low confidence
                    text_blocks.append({
                        'text': data['text'][i],
                        'confidence': int(data['conf'][i]),
                        'level': data['level'][i],
                        'block_num': data['block_num'][i],
                        'line_num': data['line_num'][i],
                        'word_num': data['word_num'][i]
                    })
            
            # Calculate average confidence
            confidences = [block['confidence'] for block in text_blocks if block['confidence'] > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Full text
            full_text = ' '.join([block['text'] for block in text_blocks])
            
            return {
                'text': full_text,
                'average_confidence': avg_confidence,
                'blocks': text_blocks,
                'total_words': len(text_blocks)
            }
        except Exception as e:
            raise Exception(f"Failed to extract text with confidence: {str(e)}")
    
    def is_text_quality_good(self, ocr_result: Dict[str, Any], min_confidence: float = 70.0) -> bool:
        """
        Check if OCR quality is good enough
        
        Args:
            ocr_result: Result from extract_text_with_confidence
            min_confidence: Minimum average confidence threshold
            
        Returns:
            True if quality is good
        """
        return ocr_result.get('average_confidence', 0) >= min_confidence

# Global OCR service instance
ocr_service = OCRService()
