import logging
from typing import Dict, Any, List
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class EmailService:
    """Email service with Gmail API and SMTP support (Mocked)"""
    
    def __init__(self):
        self.mock_mode = True  # Set to False when real credentials are provided
    
    async def send_email(self, to: List[str], subject: str, body: str, attachments: List[str] = None) -> Dict[str, Any]:
        """Send email via Gmail API or SMTP"""
        try:
            if self.mock_mode:
                email_id = str(uuid.uuid4())
                logger.info(f"[MOCK] Sending email to {to}: {subject}")
                
                return {
                    "success": True,
                    "email_id": email_id,
                    "message": "Email sent successfully (Mock Mode)",
                    "recipients": to,
                    "subject": subject,
                    "sent_at": datetime.utcnow().isoformat()
                }
            
            # Real implementation would go here with Gmail API or SMTP
            return {"success": False, "error": "Gmail API not configured"}
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {"success": False, "error": str(e)}
    
    async def fetch_emails(self, folder: str = "inbox", limit: int = 50) -> Dict[str, Any]:
        """Fetch emails from Gmail"""
        try:
            if self.mock_mode:
                # Generate mock emails
                emails = self._generate_mock_emails(limit)
                
                return {
                    "success": True,
                    "folder": folder,
                    "total": len(emails),
                    "emails": emails
                }
            
            return {"success": False, "error": "Gmail API not configured"}
            
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_mock_emails(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock email data"""
        emails = []
        base_date = datetime.now()
        
        senders = [
            "procurement@railways.gov.in",
            "tender@aiims.edu",
            "rfq@iit.ac.in",
            "bids@drdo.gov.in"
        ]
        
        subjects = [
            "Tender Notification - IT Hardware",
            "RFQ Response Deadline Extended",
            "Bid Submission Confirmation",
            "Technical Evaluation Results",
            "Payment Release Notification"
        ]
        
        for i in range(min(count, 20)):
            email = {
                "email_id": str(uuid.uuid4()),
                "from": senders[i % len(senders)],
                "subject": subjects[i % len(subjects)],
                "snippet": "This is regarding your recent bid submission...",
                "body": "Full email body content would be here.",
                "received_at": (base_date - timedelta(hours=i*2)).isoformat(),
                "is_read": i > 5,
                "has_attachments": i % 3 == 0,
                "labels": ["tenders", "important"] if i % 2 == 0 else ["general"]
            }
            emails.append(email)
        
        return emails
    
    async def create_draft(self, to: List[str], subject: str, body: str) -> Dict[str, Any]:
        """Create email draft"""
        try:
            if self.mock_mode:
                draft_id = str(uuid.uuid4())
                
                return {
                    "success": True,
                    "draft_id": draft_id,
                    "message": "Draft created successfully (Mock Mode)"
                }
            
            return {"success": False, "error": "Gmail API not configured"}
            
        except Exception as e:
            logger.error(f"Error creating draft: {e}")
            return {"success": False, "error": str(e)}
    
    async def mark_as_read(self, email_ids: List[str]) -> Dict[str, Any]:
        """Mark emails as read"""
        try:
            return {
                "success": True,
                "marked_count": len(email_ids),
                "message": f"Marked {len(email_ids)} emails as read"
            }
        except Exception as e:
            logger.error(f"Error marking emails: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_emails(self, email_ids: List[str]) -> Dict[str, Any]:
        """Delete emails"""
        try:
            return {
                "success": True,
                "deleted_count": len(email_ids),
                "message": f"Deleted {len(email_ids)} emails"
            }
        except Exception as e:
            logger.error(f"Error deleting emails: {e}")
            return {"success": False, "error": str(e)}

from datetime import timedelta

# Global instance
email_service = EmailService()
