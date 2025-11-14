import logging
from typing import Dict, Any, List
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class Office365Service:
    """Office 365 integration service (Mocked)"""
    
    def __init__(self):
        self.mock_mode = True  # Set to False when real credentials are provided
    
    async def create_document(self, document_type: str, title: str) -> Dict[str, Any]:
        """Create new Office document (Word/Excel/PowerPoint)"""
        try:
            if self.mock_mode:
                doc_id = str(uuid.uuid4())
                
                return {
                    "success": True,
                    "document_id": doc_id,
                    "type": document_type,
                    "title": title,
                    "edit_url": f"https://mock-office365.com/edit/{doc_id}",
                    "view_url": f"https://mock-office365.com/view/{doc_id}",
                    "created_at": datetime.utcnow().isoformat(),
                    "message": "Document created successfully (Mock Mode)"
                }
            
            return {"success": False, "error": "Office 365 API not configured"}
            
        except Exception as e:
            logger.error(f"Error creating document: {e}")
            return {"success": False, "error": str(e)}
    
    async def list_documents(self, folder: str = "root", limit: int = 50) -> Dict[str, Any]:
        """List documents from OneDrive"""
        try:
            if self.mock_mode:
                documents = self._generate_mock_documents(limit)
                
                return {
                    "success": True,
                    "folder": folder,
                    "total": len(documents),
                    "documents": documents
                }
            
            return {"success": False, "error": "Office 365 API not configured"}
            
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_mock_documents(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock document data"""
        documents = []
        base_date = datetime.now()
        
        doc_types = ['word', 'excel', 'powerpoint', 'pdf']
        titles = [
            "Tender Proposal Template",
            "BOQ Cost Sheet",
            "Technical Bid Document",
            "Financial Analysis",
            "Project Presentation"
        ]
        
        for i in range(min(count, 15)):
            from datetime import timedelta
            doc = {
                "document_id": str(uuid.uuid4()),
                "title": titles[i % len(titles)],
                "type": doc_types[i % len(doc_types)],
                "size": f"{((i + 1) * 150):.1f} KB",
                "created_at": (base_date - timedelta(days=i*2)).isoformat(),
                "modified_at": (base_date - timedelta(days=i)).isoformat(),
                "edit_url": f"https://mock-office365.com/edit/{uuid.uuid4()}",
                "download_url": f"https://mock-office365.com/download/{uuid.uuid4()}"
            }
            documents.append(doc)
        
        return documents
    
    async def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document details"""
        try:
            if self.mock_mode:
                return {
                    "success": True,
                    "document": {
                        "document_id": document_id,
                        "title": "Sample Document",
                        "type": "word",
                        "content": "Mock document content",
                        "edit_url": f"https://mock-office365.com/edit/{document_id}"
                    }
                }
            
            return {"success": False, "error": "Office 365 API not configured"}
            
        except Exception as e:
            logger.error(f"Error getting document: {e}")
            return {"success": False, "error": str(e)}
    
    async def upload_to_onedrive(self, file_path: str, folder: str = "root") -> Dict[str, Any]:
        """Upload file to OneDrive"""
        try:
            if self.mock_mode:
                file_id = str(uuid.uuid4())
                
                return {
                    "success": True,
                    "file_id": file_id,
                    "folder": folder,
                    "url": f"https://mock-onedrive.com/files/{file_id}",
                    "message": "File uploaded successfully (Mock Mode)"
                }
            
            return {"success": False, "error": "Office 365 API not configured"}
            
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return {"success": False, "error": str(e)}
    
    async def share_document(self, document_id: str, emails: List[str], permission: str = "view") -> Dict[str, Any]:
        """Share document with users"""
        try:
            if self.mock_mode:
                return {
                    "success": True,
                    "document_id": document_id,
                    "shared_with": emails,
                    "permission": permission,
                    "share_link": f"https://mock-office365.com/share/{document_id}",
                    "message": "Document shared successfully (Mock Mode)"
                }
            
            return {"success": False, "error": "Office 365 API not configured"}
            
        except Exception as e:
            logger.error(f"Error sharing document: {e}")
            return {"success": False, "error": str(e)}

# Global instance
office365_service = Office365Service()
