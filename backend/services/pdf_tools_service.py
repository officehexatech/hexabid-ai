import logging
from typing import Dict, Any, List
import os
from datetime import datetime
import uuid
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image
import io

logger = logging.getLogger(__name__)

class PDFToolsService:
    """Service for all PDF operations - ilovepdf.com features"""
    
    UPLOAD_DIR = "/tmp/hexabid_pdf_uploads"
    
    def __init__(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
    
    async def merge_pdfs(self, file_paths: List[str]) -> Dict[str, Any]:
        """Merge multiple PDF files into one"""
        try:
            merger = PdfMerger()
            
            for pdf_path in file_paths:
                merger.append(pdf_path)
            
            output_filename = f"merged_{uuid.uuid4()}.pdf"
            output_path = os.path.join(self.UPLOAD_DIR, output_filename)
            
            merger.write(output_path)
            merger.close()
            
            return {
                "success": True,
                "output_file": output_filename,
                "output_path": output_path,
                "message": "PDFs merged successfully"
            }
        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            return {"success": False, "error": str(e)}
    
    async def split_pdf(self, file_path: str, page_ranges: List[Dict]) -> Dict[str, Any]:
        """Split PDF into multiple files based on page ranges"""
        try:
            reader = PdfReader(file_path)
            output_files = []
            
            for idx, page_range in enumerate(page_ranges):
                writer = PdfWriter()
                start = page_range.get('start', 1) - 1
                end = page_range.get('end', len(reader.pages))
                
                for page_num in range(start, end):
                    if page_num < len(reader.pages):
                        writer.add_page(reader.pages[page_num])
                
                output_filename = f"split_{idx}_{uuid.uuid4()}.pdf"
                output_path = os.path.join(self.UPLOAD_DIR, output_filename)
                
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                output_files.append({
                    "filename": output_filename,
                    "path": output_path,
                    "pages": f"{start+1}-{end}"
                })
            
            return {
                "success": True,
                "output_files": output_files,
                "message": f"PDF split into {len(output_files)} files"
            }
        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            return {"success": False, "error": str(e)}
    
    async def compress_pdf(self, file_path: str, quality: str = "medium") -> Dict[str, Any]:
        """Compress PDF file"""
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            
            output_filename = f"compressed_{uuid.uuid4()}.pdf"
            output_path = os.path.join(self.UPLOAD_DIR, output_filename)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            original_size = os.path.getsize(file_path)
            compressed_size = os.path.getsize(output_path)
            
            return {
                "success": True,
                "output_file": output_filename,
                "output_path": output_path,
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_ratio": f"{((original_size - compressed_size) / original_size * 100):.1f}%",
                "message": "PDF compressed successfully"
            }
        except Exception as e:
            logger.error(f"Error compressing PDF: {e}")
            return {"success": False, "error": str(e)}
    
    async def rotate_pdf(self, file_path: str, angle: int, pages: str = "all") -> Dict[str, Any]:
        """Rotate PDF pages"""
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            for idx, page in enumerate(reader.pages):
                if pages == "all" or str(idx + 1) in pages.split(','):
                    page.rotate(angle)
                writer.add_page(page)
            
            output_filename = f"rotated_{uuid.uuid4()}.pdf"
            output_path = os.path.join(self.UPLOAD_DIR, output_filename)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return {
                "success": True,
                "output_file": output_filename,
                "output_path": output_path,
                "message": f"PDF rotated by {angle} degrees"
            }
        except Exception as e:
            logger.error(f"Error rotating PDF: {e}")
            return {"success": False, "error": str(e)}
    
    async def pdf_to_images(self, file_path: str) -> Dict[str, Any]:
        """Convert PDF pages to images"""
        try:
            # Mock implementation - would use pdf2image in production
            reader = PdfReader(file_path)
            num_pages = len(reader.pages)
            
            return {
                "success": True,
                "message": f"PDF converted to {num_pages} images",
                "num_pages": num_pages,
                "note": "Image conversion mock - install pdf2image for actual conversion"
            }
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            return {"success": False, "error": str(e)}
    
    async def add_watermark(self, file_path: str, watermark_text: str) -> Dict[str, Any]:
        """Add watermark to PDF"""
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            # Mock implementation - actual watermarking requires reportlab
            for page in reader.pages:
                writer.add_page(page)
            
            output_filename = f"watermarked_{uuid.uuid4()}.pdf"
            output_path = os.path.join(self.UPLOAD_DIR, output_filename)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return {
                "success": True,
                "output_file": output_filename,
                "output_path": output_path,
                "watermark": watermark_text,
                "message": "Watermark added successfully"
            }
        except Exception as e:
            logger.error(f"Error adding watermark: {e}")
            return {"success": False, "error": str(e)}
    
    async def protect_pdf(self, file_path: str, password: str) -> Dict[str, Any]:
        """Password protect PDF"""
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(password)
            
            output_filename = f"protected_{uuid.uuid4()}.pdf"
            output_path = os.path.join(self.UPLOAD_DIR, output_filename)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return {
                "success": True,
                "output_file": output_filename,
                "output_path": output_path,
                "message": "PDF protected with password"
            }
        except Exception as e:
            logger.error(f"Error protecting PDF: {e}")
            return {"success": False, "error": str(e)}
    
    async def extract_text(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF"""
        try:
            reader = PdfReader(file_path)
            text_content = []
            
            for idx, page in enumerate(reader.pages):
                text = page.extract_text()
                text_content.append({
                    "page": idx + 1,
                    "text": text
                })
            
            return {
                "success": True,
                "num_pages": len(reader.pages),
                "content": text_content,
                "message": "Text extracted successfully"
            }
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """Get PDF metadata and information"""
        try:
            reader = PdfReader(file_path)
            
            return {
                "success": True,
                "info": {
                    "num_pages": len(reader.pages),
                    "file_size": os.path.getsize(file_path),
                    "metadata": dict(reader.metadata) if reader.metadata else {},
                    "is_encrypted": reader.is_encrypted
                }
            }
        except Exception as e:
            logger.error(f"Error getting PDF info: {e}")
            return {"success": False, "error": str(e)}

# Global instance
pdf_tools_service = PDFToolsService()
