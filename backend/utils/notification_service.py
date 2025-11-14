"""
Notification Service for Email and WhatsApp
Supports multiple notification channels
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import os
import requests

class NotificationService:
    """Multi-channel notification service"""
    
    def __init__(self):
        # Email configuration (SMTP)
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@hexabid.com')
        
        # WhatsApp configuration (using WhatsApp Business API or services like Twilio)
        self.whatsapp_enabled = os.getenv('WHATSAPP_ENABLED', 'false').lower() == 'true'
        self.whatsapp_api_url = os.getenv('WHATSAPP_API_URL', '')
        self.whatsapp_api_key = os.getenv('WHATSAPP_API_KEY', '')
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        body_html: str = None,
        cc: List[str] = None,
        bcc: List[str] = None
    ) -> bool:
        """
        Send email notification
        
        Args:
            to_email: Recipient email
            subject: Email subject
            body: Plain text body
            body_html: HTML body (optional)
            cc: CC recipients
            bcc: BCC recipients
            
        Returns:
            True if sent successfully
        """
        try:
            if not self.smtp_user or not self.smtp_password:
                print("SMTP credentials not configured")
                return False
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Add plain text
            part1 = MIMEText(body, 'plain')
            msg.attach(part1)
            
            # Add HTML if provided
            if body_html:
                part2 = MIMEText(body_html, 'html')
                msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def send_whatsapp(
        self,
        phone_number: str,
        message: str,
        template_name: str = None,
        template_params: Dict[str, Any] = None
    ) -> bool:
        """
        Send WhatsApp notification
        
        Args:
            phone_number: Recipient phone number (with country code)
            message: Message text
            template_name: WhatsApp template name (if using templates)
            template_params: Template parameters
            
        Returns:
            True if sent successfully
        """
        try:
            if not self.whatsapp_enabled:
                print("WhatsApp notifications not enabled")
                return False
            
            if not self.whatsapp_api_url or not self.whatsapp_api_key:
                print("WhatsApp API not configured")
                return False
            
            # Generic WhatsApp API call (adapt to your provider)
            payload = {
                "phone": phone_number,
                "message": message
            }
            
            if template_name and template_params:
                payload["template"] = template_name
                payload["params"] = template_params
            
            headers = {
                "Authorization": f"Bearer {self.whatsapp_api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.whatsapp_api_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send WhatsApp: {str(e)}")
            return False
    
    def send_tender_alert(
        self,
        user_email: str,
        tender_data: Dict[str, Any],
        channels: List[str] = ["email"]
    ) -> Dict[str, bool]:
        """
        Send tender alert notification
        
        Args:
            user_email: User's email
            tender_data: Tender information
            channels: Notification channels (email, whatsapp)
            
        Returns:
            Dictionary with channel: success status
        """
        results = {}
        
        subject = f"New Tender Alert: {tender_data.get('tender_number', 'N/A')}"
        body = f"""
        New tender matching your interests:
        
        Tender Number: {tender_data.get('tender_number', 'N/A')}
        Title: {tender_data.get('title', 'N/A')}
        Organization: {tender_data.get('organization', 'N/A')}
        Value: ₹{tender_data.get('tender_value', 0):,.2f}
        Deadline: {tender_data.get('submission_deadline', 'N/A')}
        
        Login to HexaBid to view complete details and submit your bid.
        
        Best regards,
        HexaBid Team
        """
        
        if "email" in channels:
            results["email"] = self.send_email(user_email, subject, body)
        
        if "whatsapp" in channels and "phone" in tender_data:
            whatsapp_msg = f"🔔 *New Tender Alert*\n\n{tender_data.get('tender_number')}: {tender_data.get('title')}\nDeadline: {tender_data.get('submission_deadline')}\n\nView on HexaBid"
            results["whatsapp"] = self.send_whatsapp(tender_data["phone"], whatsapp_msg)
        
        return results
    
    def send_rfq_to_vendor(
        self,
        vendor_email: str,
        vendor_phone: str,
        rfq_data: Dict[str, Any],
        channels: List[str] = ["email"]
    ) -> Dict[str, bool]:
        """
        Send RFQ to vendor
        
        Args:
            vendor_email: Vendor email
            vendor_phone: Vendor phone
            rfq_data: RFQ information
            channels: Notification channels
            
        Returns:
            Dictionary with channel: success status
        """
        results = {}
        
        subject = f"RFQ: {rfq_data.get('rfq_number', 'N/A')}"
        body = rfq_data.get('email_template', '')
        
        if "email" in channels:
            results["email"] = self.send_email(vendor_email, subject, body)
        
        if "whatsapp" in channels and vendor_phone:
            whatsapp_msg = rfq_data.get('whatsapp_template', '')
            results["whatsapp"] = self.send_whatsapp(vendor_phone, whatsapp_msg)
        
        return results
    
    def send_bid_status_update(
        self,
        user_email: str,
        tender_number: str,
        status: str,
        message: str,
        channels: List[str] = ["email"]
    ) -> Dict[str, bool]:
        """
        Send bid status update
        
        Args:
            user_email: User email
            tender_number: Tender number
            status: Status (submitted, won, lost, etc.)
            message: Status message
            channels: Notification channels
            
        Returns:
            Dictionary with channel: success status
        """
        results = {}
        
        subject = f"Bid Status Update: {tender_number}"
        body = f"""
        Tender Number: {tender_number}
        Status: {status.upper()}
        
        {message}
        
        Login to HexaBid for complete details.
        
        Best regards,
        HexaBid Team
        """
        
        if "email" in channels:
            results["email"] = self.send_email(user_email, subject, body)
        
        return results

# Global notification service instance
notification_service = NotificationService()
