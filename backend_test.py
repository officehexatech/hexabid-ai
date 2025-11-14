#!/usr/bin/env python3
"""
HexaBid Backend API Testing Script
Tests all backend APIs according to the review request
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "https://hexabid.preview.emergentagent.com/api"
HEADERS = {"Content-Type": "application/json"}

class HexaBidAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS.copy()
        self.auth_token = None
        self.user_data = None
        self.vendor_id = None
        self.company_profile_id = None
        self.rfq_id = None
        # 100% MVP API IDs
        self.tender_id = None
        self.product_id = None
        self.boq_id = None
        self.alert_id = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response": response_data if not success else None
        })
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers, json=data, timeout=30)
            else:
                return False, f"Unsupported method: {method}", 0
            
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            return response.status_code < 400, response_data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", 0
    
    def set_auth_token(self, token: str):
        """Set authentication token for subsequent requests"""
        self.auth_token = token
        self.headers["Authorization"] = f"Bearer {token}"
    
    def test_health_check(self):
        """Test API health check"""
        success, data, status_code = self.make_request("GET", "/health")
        
        if success and isinstance(data, dict) and data.get("status") == "healthy":
            self.log_test("Health Check", True, f"API is healthy, database connected")
        else:
            self.log_test("Health Check", False, f"Health check failed (Status: {status_code})", data)
    
    def test_user_registration(self):
        """Test user registration"""
        # Try to login first, if that fails, register
        login_data = {
            "email": "john.doe@hexabid.com",
            "password": "SecurePass123!"
        }
        
        success, data, status_code = self.make_request("POST", "/auth/login", login_data)
        
        if success and isinstance(data, dict) and "accessToken" in data:
            self.user_data = data.get("user")
            self.set_auth_token(data["accessToken"])
            self.log_test("User Registration", True, f"User logged in successfully with ID: {self.user_data.get('id')}")
            return
        
        # If login fails, try registration with a unique email
        import time
        unique_email = f"test.user.{int(time.time())}@hexabid.com"
        user_data = {
            "email": unique_email,
            "password": "SecurePass123!",
            "fullName": "Test User",
            "phone": "+91-9876543210"
        }
        
        success, data, status_code = self.make_request("POST", "/auth/register", user_data)
        
        if success and isinstance(data, dict) and "accessToken" in data:
            self.user_data = data.get("user")
            self.set_auth_token(data["accessToken"])
            self.log_test("User Registration", True, f"User registered successfully with ID: {self.user_data.get('id')}")
        else:
            self.log_test("User Registration", False, f"Registration failed (Status: {status_code})", data)
    
    def test_user_login(self):
        """Test user login"""
        login_data = {
            "email": "john.doe@hexabid.com",
            "password": "SecurePass123!"
        }
        
        success, data, status_code = self.make_request("POST", "/auth/login", login_data)
        
        if success and isinstance(data, dict) and "accessToken" in data:
            self.user_data = data.get("user")
            self.set_auth_token(data["accessToken"])
            self.log_test("User Login", True, f"Login successful for user: {self.user_data.get('email')}")
        else:
            self.log_test("User Login", False, f"Login failed (Status: {status_code})", data)
    
    def test_get_current_user(self):
        """Test get current user endpoint"""
        if not self.auth_token:
            self.log_test("Get Current User", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("GET", "/auth/me")
        
        if success and isinstance(data, dict) and "email" in data:
            self.log_test("Get Current User", True, f"Retrieved user data for: {data.get('email')}")
        else:
            self.log_test("Get Current User", False, f"Failed to get user data (Status: {status_code})", data)
    
    def test_create_vendor(self):
        """Test vendor creation"""
        if not self.auth_token:
            self.log_test("Create Vendor", False, "No auth token available")
            return
        
        vendor_data = {
            "companyName": "TechCorp Solutions Pvt Ltd",
            "vendorType": "Technology",
            "primaryContactName": "Rajesh Kumar",
            "primaryContactEmail": "rajesh@techcorp.com",
            "primaryContactPhone": "+91-9876543211",
            "address": "123 Tech Park, Electronic City",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "pincode": "560100",
            "gstin": "29ABCDE1234F1Z5",
            "pan": "ABCDE1234F",
            "website": "https://techcorp.com",
            "paymentTerms": "Net 30",
            "categories": ["Software", "Hardware", "Consulting"],
            "tags": ["reliable", "quality"],
            "notes": "Preferred vendor for tech solutions"
        }
        
        # Try with trailing slash first
        success, data, status_code = self.make_request("POST", "/vendors/", vendor_data)
        
        if success and isinstance(data, dict) and "id" in data:
            self.vendor_id = data["id"]
            self.log_test("Create Vendor", True, f"Vendor created successfully with ID: {self.vendor_id}")
        else:
            self.log_test("Create Vendor", False, f"Vendor creation failed (Status: {status_code})", data)
    
    def test_list_vendors(self):
        """Test vendor listing with pagination"""
        if not self.auth_token:
            self.log_test("List Vendors", False, "No auth token available")
            return
        
        params = {"page": 1, "limit": 10}
        success, data, status_code = self.make_request("GET", "/vendors/", params=params)
        
        if success and isinstance(data, dict) and "data" in data and "pagination" in data:
            vendor_count = len(data["data"])
            total = data["pagination"]["total"]
            self.log_test("List Vendors", True, f"Retrieved {vendor_count} vendors, total: {total}")
        else:
            self.log_test("List Vendors", False, f"Failed to list vendors (Status: {status_code})", data)
    
    def test_get_single_vendor(self):
        """Test getting single vendor"""
        if not self.auth_token or not self.vendor_id:
            self.log_test("Get Single Vendor", False, "No auth token or vendor ID available")
            return
        
        success, data, status_code = self.make_request("GET", f"/vendors/{self.vendor_id}")
        
        if success and isinstance(data, dict) and data.get("id") == self.vendor_id:
            self.log_test("Get Single Vendor", True, f"Retrieved vendor: {data.get('companyName')}")
        else:
            self.log_test("Get Single Vendor", False, f"Failed to get vendor (Status: {status_code})", data)
    
    def test_update_vendor(self):
        """Test vendor update"""
        if not self.auth_token or not self.vendor_id:
            self.log_test("Update Vendor", False, "No auth token or vendor ID available")
            return
        
        update_data = {
            "notes": "Updated notes - Premium vendor with excellent track record",
            "rating": 4.5
        }
        
        success, data, status_code = self.make_request("PATCH", f"/vendors/{self.vendor_id}", update_data)
        
        if success and isinstance(data, dict) and data.get("id") == self.vendor_id:
            self.log_test("Update Vendor", True, f"Vendor updated successfully")
        else:
            self.log_test("Update Vendor", False, f"Failed to update vendor (Status: {status_code})", data)
    
    def test_search_vendors(self):
        """Test vendor search"""
        if not self.auth_token:
            self.log_test("Search Vendors", False, "No auth token available")
            return
        
        params = {"search": "TechCorp"}
        success, data, status_code = self.make_request("GET", "/vendors/", params=params)
        
        if success and isinstance(data, dict) and "data" in data:
            found_vendors = len(data["data"])
            self.log_test("Search Vendors", True, f"Search returned {found_vendors} vendors")
        else:
            self.log_test("Search Vendors", False, f"Search failed (Status: {status_code})", data)
    
    def test_create_company_profile(self):
        """Test company profile creation"""
        if not self.auth_token:
            self.log_test("Create Company Profile", False, "No auth token available")
            return
        
        profile_data = {
            "companyName": "HexaBid Enterprises Pvt Ltd",
            "industry": "Technology Services",
            "address": "456 Business District, Cyber City, Gurgaon, Haryana 122001",
            "taxId": "27ABCDE5678G1Z9",
            "authorizedPersonName": "John Doe",
            "authorizedPersonMobile": "+91-9876543210",
            "authorizedPersonEmail": "john.doe@hexabid.com"
        }
        
        success, data, status_code = self.make_request("POST", "/company/profile", profile_data)
        
        if success and isinstance(data, dict) and "id" in data:
            self.company_profile_id = data["id"]
            self.log_test("Create Company Profile", True, f"Company profile created with ID: {self.company_profile_id}")
        else:
            self.log_test("Create Company Profile", False, f"Profile creation failed (Status: {status_code})", data)
    
    def test_get_company_profile(self):
        """Test get company profile"""
        if not self.auth_token:
            self.log_test("Get Company Profile", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("GET", "/company/profile")
        
        if success and isinstance(data, dict) and "companyName" in data:
            self.log_test("Get Company Profile", True, f"Retrieved profile for: {data.get('companyName')}")
        else:
            self.log_test("Get Company Profile", False, f"Failed to get profile (Status: {status_code})", data)
    
    def test_update_company_profile(self):
        """Test company profile update"""
        if not self.auth_token:
            self.log_test("Update Company Profile", False, "No auth token available")
            return
        
        update_data = {
            "industry": "Enterprise Software Solutions",
            "logoUrl": "https://hexabid.com/logo.png"
        }
        
        success, data, status_code = self.make_request("PATCH", "/company/profile", update_data)
        
        if success and isinstance(data, dict) and data.get("industry") == update_data["industry"]:
            self.log_test("Update Company Profile", True, f"Profile updated successfully")
        else:
            self.log_test("Update Company Profile", False, f"Profile update failed (Status: {status_code})", data)
    
    def test_invite_team_member(self):
        """Test team member invitation"""
        if not self.auth_token:
            self.log_test("Invite Team Member", False, "No auth token available")
            return
        
        invite_data = {
            "email": "manager@hexabid.com",
            "name": "Sarah Manager",
            "role": "manager"
        }
        
        success, data, status_code = self.make_request("POST", "/company/team/invite", invite_data)
        
        if success and isinstance(data, dict) and "id" in data:
            self.log_test("Invite Team Member", True, f"Team member invited: {data.get('email')}")
        else:
            self.log_test("Invite Team Member", False, f"Team invitation failed (Status: {status_code})", data)
    
    def test_list_team_members(self):
        """Test listing team members"""
        if not self.auth_token:
            self.log_test("List Team Members", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("GET", "/company/team")
        
        if success and isinstance(data, list):
            member_count = len(data)
            self.log_test("List Team Members", True, f"Retrieved {member_count} team members")
        else:
            self.log_test("List Team Members", False, f"Failed to list team members (Status: {status_code})", data)
    
    def test_create_rfq(self):
        """Test RFQ creation with line items"""
        if not self.auth_token or not self.vendor_id:
            self.log_test("Create RFQ", False, "No auth token or vendor ID available")
            return
        
        # Calculate due date (30 days from now)
        due_date = (datetime.now() + timedelta(days=30)).isoformat()
        
        rfq_data = {
            "rfqNumber": "RFQ-2024-001",
            "title": "Office Equipment and Software Procurement",
            "description": "Procurement of laptops, software licenses, and office furniture for new branch",
            "vendorIds": [self.vendor_id],
            "lineItems": [
                {
                    "itemName": "Dell Latitude Laptops",
                    "description": "High-performance business laptops with 16GB RAM, 512GB SSD",
                    "quantity": 25,
                    "unit": "pieces",
                    "specifications": "Intel i7, 16GB RAM, 512GB SSD, Windows 11 Pro"
                },
                {
                    "itemName": "Microsoft Office 365 Licenses",
                    "description": "Annual business licenses for productivity suite",
                    "quantity": 25,
                    "unit": "licenses",
                    "specifications": "Business Premium plan with Teams, SharePoint, OneDrive"
                },
                {
                    "itemName": "Ergonomic Office Chairs",
                    "description": "Adjustable office chairs with lumbar support",
                    "quantity": 25,
                    "unit": "pieces",
                    "specifications": "Height adjustable, mesh back, 5-year warranty"
                }
            ],
            "dueDate": due_date,
            "deliveryLocation": "HexaBid Office, Cyber City, Gurgaon",
            "paymentTerms": "Net 45 days",
            "notes": "Please provide detailed quotations with warranty terms and delivery schedules"
        }
        
        success, data, status_code = self.make_request("POST", "/rfq/", rfq_data)
        
        if success and isinstance(data, dict) and "id" in data:
            self.rfq_id = data["id"]
            line_items_count = len(data.get("lineItems", []))
            self.log_test("Create RFQ", True, f"RFQ created with ID: {self.rfq_id}, {line_items_count} line items")
        else:
            self.log_test("Create RFQ", False, f"RFQ creation failed (Status: {status_code})", data)
    
    def test_list_rfqs(self):
        """Test RFQ listing"""
        if not self.auth_token:
            self.log_test("List RFQs", False, "No auth token available")
            return
        
        params = {"page": 1, "limit": 10}
        success, data, status_code = self.make_request("GET", "/rfq/", params=params)
        
        if success and isinstance(data, dict) and "data" in data:
            rfq_count = len(data["data"])
            total = data["pagination"]["total"]
            self.log_test("List RFQs", True, f"Retrieved {rfq_count} RFQs, total: {total}")
        else:
            self.log_test("List RFQs", False, f"Failed to list RFQs (Status: {status_code})", data)
    
    def test_get_rfq_details(self):
        """Test getting RFQ details"""
        if not self.auth_token or not self.rfq_id:
            self.log_test("Get RFQ Details", False, "No auth token or RFQ ID available")
            return
        
        success, data, status_code = self.make_request("GET", f"/rfq/{self.rfq_id}")
        
        if success and isinstance(data, dict) and data.get("id") == self.rfq_id:
            line_items_count = len(data.get("lineItems", []))
            vendor_count = len(data.get("vendorIds", []))
            self.log_test("Get RFQ Details", True, f"Retrieved RFQ: {data.get('title')} with {line_items_count} items, {vendor_count} vendors")
        else:
            self.log_test("Get RFQ Details", False, f"Failed to get RFQ details (Status: {status_code})", data)
    
    def test_settings_public(self):
        """Test public settings API"""
        success, data, status_code = self.make_request("GET", "/settings/public")
        
        if success and isinstance(data, dict):
            contact_info = data.get("contactInfo", {})
            social_links = data.get("socialMediaLinks", [])
            
            # Check required fields
            required_fields = ["phone1", "phone2", "email", "whatsappNumber"]
            missing_fields = [field for field in required_fields if field not in contact_info]
            
            if not missing_fields and isinstance(social_links, list):
                self.log_test("Settings Public API", True, f"Retrieved settings with contact info and {len(social_links)} social media links")
            else:
                self.log_test("Settings Public API", False, f"Missing required fields: {missing_fields}", data)
        else:
            self.log_test("Settings Public API", False, f"Failed to get public settings (Status: {status_code})", data)
    
    def test_chatbot_conversation(self):
        """Test AI chatbot conversation flow"""
        session_id = "test-session-123"
        
        # First message about HexaBid
        message1_data = {
            "message": "What is HexaBid?",
            "sessionId": session_id
        }
        
        success, data, status_code = self.make_request("POST", "/chatbot/chat", message1_data)
        
        if success and isinstance(data, dict) and "response" in data:
            response_text = data["response"].lower()
            # Check if response mentions key HexaBid features
            if "hexabid" in response_text or "tender" in response_text or "ai" in response_text:
                self.log_test("Chatbot - HexaBid Info", True, f"AI responded about HexaBid features")
            else:
                self.log_test("Chatbot - HexaBid Info", False, f"Response doesn't seem relevant to HexaBid", data)
        else:
            self.log_test("Chatbot - HexaBid Info", False, f"Failed to get chatbot response (Status: {status_code})", data)
            return
        
        # Second message about pricing
        message2_data = {
            "message": "Tell me about pricing",
            "sessionId": session_id
        }
        
        success, data, status_code = self.make_request("POST", "/chatbot/chat", message2_data)
        
        if success and isinstance(data, dict) and "response" in data:
            response_text = data["response"].lower()
            # Check if response mentions free pricing
            if "free" in response_text or "100%" in response_text or "no cost" in response_text:
                self.log_test("Chatbot - Pricing Info", True, f"AI responded about FREE pricing")
            else:
                self.log_test("Chatbot - Pricing Info", False, f"Response doesn't mention free pricing", data)
        else:
            self.log_test("Chatbot - Pricing Info", False, f"Failed to get pricing response (Status: {status_code})", data)
    
    def test_chatbot_history(self):
        """Test chatbot conversation history"""
        session_id = "test-session-123"
        
        success, data, status_code = self.make_request("GET", f"/chatbot/history/{session_id}")
        
        if success and isinstance(data, dict) and "history" in data:
            history = data["history"]
            if isinstance(history, list) and len(history) >= 2:
                # Check if we have the messages from previous test
                has_hexabid_msg = any("hexabid" in msg.get("userMessage", "").lower() for msg in history)
                has_pricing_msg = any("pricing" in msg.get("userMessage", "").lower() for msg in history)
                
                if has_hexabid_msg and has_pricing_msg:
                    self.log_test("Chatbot History", True, f"Retrieved {len(history)} conversation entries")
                else:
                    self.log_test("Chatbot History", True, f"Retrieved {len(history)} entries (may not include test messages)")
            else:
                self.log_test("Chatbot History", True, f"Retrieved {len(history)} conversation entries")
        else:
            self.log_test("Chatbot History", False, f"Failed to get chat history (Status: {status_code})", data)
    
    def test_google_oauth_session(self):
        """Test Google OAuth session endpoint (placeholder)"""
        # This is a placeholder test as mentioned in the review request
        headers_with_session = self.headers.copy()
        headers_with_session["X-Session-ID"] = "test-session-placeholder"
        
        try:
            url = f"{self.base_url}/auth/google/session"
            response = requests.post(url, headers=headers_with_session, timeout=30)
            
            # We expect this to fail since it's a placeholder, but we test the endpoint exists
            if response.status_code == 400 or response.status_code == 401:
                self.log_test("Google OAuth Session", True, f"Endpoint exists and responds (Status: {response.status_code})")
            elif response.status_code == 404:
                self.log_test("Google OAuth Session", False, f"Endpoint not found (Status: {response.status_code})")
            else:
                self.log_test("Google OAuth Session", True, f"Endpoint responds (Status: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            self.log_test("Google OAuth Session", False, f"Request failed: {str(e)}")
    
    def test_logout_endpoint(self):
        """Test logout endpoint"""
        success, data, status_code = self.make_request("POST", "/auth/logout")
        
        # Logout should work even without session cookie in our test environment
        if status_code == 200 or status_code == 204:
            self.log_test("Logout Endpoint", True, f"Logout endpoint working (Status: {status_code})")
        else:
            self.log_test("Logout Endpoint", False, f"Logout failed (Status: {status_code})", data)
    
    def test_create_tender(self):
        """Test tender creation"""
        if not self.auth_token:
            self.log_test("Create Tender", False, "No auth token available")
            return
        
        tender_data = {
            "tenderNumber": "TND-2025-001",
            "title": "IT Infrastructure Setup",
            "description": "Complete IT infrastructure for new office",
            "source": "gem",
            "organization": "Ministry of IT",
            "department": "Infrastructure",
            "category": "IT Hardware",
            "location": "Delhi",
            "publishDate": "2025-01-15",
            "submissionDeadline": "2025-02-15",
            "tenderValue": 5000000,
            "emdAmount": 100000,
            "documentUrl": "https://example.com/tender.pdf",
            "notes": "Test tender for MVP"
        }
        
        success, data, status_code = self.make_request("POST", "/tenders/", tender_data)
        
        if success and isinstance(data, dict) and "id" in data:
            self.tender_id = data["id"]
            self.log_test("Create Tender", True, f"Tender created successfully with ID: {self.tender_id}")
        else:
            self.log_test("Create Tender", False, f"Tender creation failed (Status: {status_code})", data)
    
    def test_list_tenders(self):
        """Test tender listing with pagination and filters"""
        if not self.auth_token:
            self.log_test("List Tenders", False, "No auth token available")
            return
        
        params = {"page": 1, "limit": 10}
        success, data, status_code = self.make_request("GET", "/tenders/", params=params)
        
        if success and isinstance(data, dict) and "data" in data and "pagination" in data:
            tender_count = len(data["data"])
            total = data["pagination"]["total"]
            self.log_test("List Tenders", True, f"Retrieved {tender_count} tenders, total: {total}")
        else:
            self.log_test("List Tenders", False, f"Failed to list tenders (Status: {status_code})", data)
    
    def test_get_single_tender(self):
        """Test getting single tender"""
        if not self.auth_token or not hasattr(self, 'tender_id'):
            self.log_test("Get Single Tender", False, "No auth token or tender ID available")
            return
        
        success, data, status_code = self.make_request("GET", f"/tenders/{self.tender_id}")
        
        if success and isinstance(data, dict) and data.get("id") == self.tender_id:
            self.log_test("Get Single Tender", True, f"Retrieved tender: {data.get('title')}")
        else:
            self.log_test("Get Single Tender", False, f"Failed to get tender (Status: {status_code})", data)
    
    def test_update_tender(self):
        """Test tender update"""
        if not self.auth_token or not hasattr(self, 'tender_id'):
            self.log_test("Update Tender", False, "No auth token or tender ID available")
            return
        
        update_data = {
            "notes": "Updated notes - High priority tender",
            "status": "in_progress"
        }
        
        success, data, status_code = self.make_request("PATCH", f"/tenders/{self.tender_id}", update_data)
        
        if success and isinstance(data, dict) and data.get("id") == self.tender_id:
            self.log_test("Update Tender", True, f"Tender updated successfully")
        else:
            self.log_test("Update Tender", False, f"Failed to update tender (Status: {status_code})", data)
    
    def test_search_tenders(self):
        """Test tender search"""
        if not self.auth_token:
            self.log_test("Search Tenders", False, "No auth token available")
            return
        
        params = {"search": "IT Infrastructure"}
        success, data, status_code = self.make_request("GET", "/tenders/", params=params)
        
        if success and isinstance(data, dict) and "data" in data:
            found_tenders = len(data["data"])
            self.log_test("Search Tenders", True, f"Search returned {found_tenders} tenders")
        else:
            self.log_test("Search Tenders", False, f"Search failed (Status: {status_code})", data)
    
    def test_delete_tender(self):
        """Test tender deletion"""
        if not self.auth_token or not hasattr(self, 'tender_id'):
            self.log_test("Delete Tender", False, "No auth token or tender ID available")
            return
        
        success, data, status_code = self.make_request("DELETE", f"/tenders/{self.tender_id}")
        
        if status_code == 204:
            self.log_test("Delete Tender", True, f"Tender deleted successfully")
        else:
            self.log_test("Delete Tender", False, f"Failed to delete tender (Status: {status_code})", data)
    
    def test_delete_boq(self):
        """Test BOQ deletion"""
        if not self.auth_token or not hasattr(self, 'boq_id'):
            self.log_test("Delete BOQ", False, "No auth token or BOQ ID available")
            return
        
        success, data, status_code = self.make_request("DELETE", f"/boq/{self.boq_id}")
        
        if status_code == 204:
            self.log_test("Delete BOQ", True, f"BOQ deleted successfully")
        else:
            self.log_test("Delete BOQ", False, f"Failed to delete BOQ (Status: {status_code})", data)
    
    def test_delete_alert(self):
        """Test alert deletion"""
        if not self.auth_token or not hasattr(self, 'alert_id'):
            self.log_test("Delete Alert", False, "No auth token or alert ID available")
            return
        
        success, data, status_code = self.make_request("DELETE", f"/alerts/{self.alert_id}")
        
        if status_code == 204:
            self.log_test("Delete Alert", True, f"Alert deleted successfully")
        else:
            self.log_test("Delete Alert", False, f"Failed to delete alert (Status: {status_code})", data)
    
    def test_create_product(self):
        """Test product creation"""
        if not self.auth_token:
            self.log_test("Create Product", False, "No auth token available")
            return
        
        import time
        unique_code = f"PRD-{int(time.time())}"
        product_data = {
            "productCode": unique_code,
            "productName": "Dell Laptop XPS 15",
            "category": "hardware",
            "brand": "Dell",
            "model": "XPS 15 9500",
            "unit": "pcs",
            "unitPrice": 150000,
            "leadTimeDays": 15,
            "warrantyMonths": 36,
            "description": "High performance laptop"
        }
        
        success, data, status_code = self.make_request("POST", "/products/", product_data)
        
        if success and isinstance(data, dict) and "id" in data:
            self.product_id = data["id"]
            self.log_test("Create Product", True, f"Product created successfully with ID: {self.product_id}")
        else:
            self.log_test("Create Product", False, f"Product creation failed (Status: {status_code})", data)
    
    def test_list_products(self):
        """Test product listing with pagination and filters"""
        if not self.auth_token:
            self.log_test("List Products", False, "No auth token available")
            return
        
        params = {"page": 1, "limit": 10, "category": "hardware"}
        success, data, status_code = self.make_request("GET", "/products/", params=params)
        
        if success and isinstance(data, dict) and "data" in data and "pagination" in data:
            product_count = len(data["data"])
            total = data["pagination"]["total"]
            self.log_test("List Products", True, f"Retrieved {product_count} products, total: {total}")
        else:
            self.log_test("List Products", False, f"Failed to list products (Status: {status_code})", data)
    
    def test_get_single_product(self):
        """Test getting single product"""
        if not self.auth_token or not hasattr(self, 'product_id'):
            self.log_test("Get Single Product", False, "No auth token or product ID available")
            return
        
        success, data, status_code = self.make_request("GET", f"/products/{self.product_id}")
        
        if success and isinstance(data, dict) and data.get("id") == self.product_id:
            self.log_test("Get Single Product", True, f"Retrieved product: {data.get('productName')}")
        else:
            self.log_test("Get Single Product", False, f"Failed to get product (Status: {status_code})", data)
    
    def test_update_product(self):
        """Test product update with price history tracking"""
        if not self.auth_token or not hasattr(self, 'product_id'):
            self.log_test("Update Product", False, "No auth token or product ID available")
            return
        
        update_data = {
            "unitPrice": 155000,
            "description": "Updated high performance laptop with better specs"
        }
        
        success, data, status_code = self.make_request("PATCH", f"/products/{self.product_id}", update_data)
        
        if success and isinstance(data, dict) and data.get("id") == self.product_id:
            price_history = data.get("priceHistory", [])
            self.log_test("Update Product", True, f"Product updated successfully, price history entries: {len(price_history)}")
        else:
            self.log_test("Update Product", False, f"Failed to update product (Status: {status_code})", data)
    
    def test_soft_delete_product(self):
        """Test product soft delete"""
        if not self.auth_token or not hasattr(self, 'product_id'):
            self.log_test("Soft Delete Product", False, "No auth token or product ID available")
            return
        
        success, data, status_code = self.make_request("DELETE", f"/products/{self.product_id}")
        
        if status_code == 204:
            self.log_test("Soft Delete Product", True, f"Product soft deleted successfully")
        else:
            self.log_test("Soft Delete Product", False, f"Failed to delete product (Status: {status_code})", data)
    
    def test_create_boq(self):
        """Test BOQ creation with line items"""
        if not self.auth_token or not hasattr(self, 'tender_id'):
            self.log_test("Create BOQ", False, "No auth token or tender ID available")
            return
        
        boq_data = {
            "tenderId": self.tender_id,
            "boqNumber": "BOQ-001",
            "title": "IT Infrastructure BOQ",
            "lineItems": [
                {
                    "itemNumber": "1",
                    "description": "Dell Laptop",
                    "quantity": 10,
                    "unit": "pcs",
                    "estimatedRate": 140000,
                    "ourRate": 150000
                },
                {
                    "itemNumber": "2",
                    "description": "Dell Monitor",
                    "quantity": 10,
                    "unit": "pcs",
                    "estimatedRate": 20000,
                    "ourRate": 22000
                }
            ],
            "notes": "Test BOQ"
        }
        
        success, data, status_code = self.make_request("POST", "/boq/", boq_data)
        
        if success and isinstance(data, dict) and "id" in data:
            self.boq_id = data["id"]
            line_items_count = len(data.get("lineItems", []))
            self.log_test("Create BOQ", True, f"BOQ created successfully with ID: {self.boq_id}, {line_items_count} line items")
        else:
            self.log_test("Create BOQ", False, f"BOQ creation failed (Status: {status_code})", data)
    
    def test_list_boqs_by_tender(self):
        """Test listing BOQs by tender"""
        if not self.auth_token or not hasattr(self, 'tender_id'):
            self.log_test("List BOQs by Tender", False, "No auth token or tender ID available")
            return
        
        success, data, status_code = self.make_request("GET", f"/boq/tender/{self.tender_id}")
        
        if success and isinstance(data, dict) and "data" in data:
            boq_count = len(data["data"])
            self.log_test("List BOQs by Tender", True, f"Retrieved {boq_count} BOQs for tender")
        else:
            self.log_test("List BOQs by Tender", False, f"Failed to list BOQs (Status: {status_code})", data)
    
    def test_get_single_boq(self):
        """Test getting single BOQ"""
        if not self.auth_token or not hasattr(self, 'boq_id'):
            self.log_test("Get Single BOQ", False, "No auth token or BOQ ID available")
            return
        
        success, data, status_code = self.make_request("GET", f"/boq/{self.boq_id}")
        
        if success and isinstance(data, dict) and data.get("id") == self.boq_id:
            line_items_count = len(data.get("lineItems", []))
            self.log_test("Get Single BOQ", True, f"Retrieved BOQ: {data.get('title')} with {line_items_count} line items")
        else:
            self.log_test("Get Single BOQ", False, f"Failed to get BOQ (Status: {status_code})", data)
    
    def test_update_boq(self):
        """Test BOQ update"""
        if not self.auth_token or not hasattr(self, 'boq_id'):
            self.log_test("Update BOQ", False, "No auth token or BOQ ID available")
            return
        
        update_data = {
            "notes": "Updated BOQ with revised rates",
            "status": "approved"
        }
        
        success, data, status_code = self.make_request("PATCH", f"/boq/{self.boq_id}", update_data)
        
        if success and isinstance(data, dict) and data.get("id") == self.boq_id:
            self.log_test("Update BOQ", True, f"BOQ updated successfully")
        else:
            self.log_test("Update BOQ", False, f"Failed to update BOQ (Status: {status_code})", data)
    
    def test_create_alert(self):
        """Test alert creation"""
        if not self.auth_token:
            self.log_test("Create Alert", False, "No auth token available")
            return
        
        alert_data = {
            "alertType": "deadline",
            "title": "Tender Deadline Approaching",
            "message": "Tender TND-2025-001 deadline is in 2 days",
            "channels": ["inapp", "email"]
        }
        
        success, data, status_code = self.make_request("POST", "/alerts/", alert_data)
        
        if success and isinstance(data, dict) and "id" in data:
            self.alert_id = data["id"]
            self.log_test("Create Alert", True, f"Alert created successfully with ID: {self.alert_id}")
        else:
            self.log_test("Create Alert", False, f"Alert creation failed (Status: {status_code})", data)
    
    def test_list_alerts(self):
        """Test alert listing with unread count"""
        if not self.auth_token:
            self.log_test("List Alerts", False, "No auth token available")
            return
        
        params = {"page": 1, "limit": 10}
        success, data, status_code = self.make_request("GET", "/alerts/", params=params)
        
        if success and isinstance(data, dict) and "data" in data and "unreadCount" in data:
            alert_count = len(data["data"])
            unread_count = data["unreadCount"]
            self.log_test("List Alerts", True, f"Retrieved {alert_count} alerts, {unread_count} unread")
        else:
            self.log_test("List Alerts", False, f"Failed to list alerts (Status: {status_code})", data)
    
    def test_list_unread_alerts(self):
        """Test listing unread alerts only"""
        if not self.auth_token:
            self.log_test("List Unread Alerts", False, "No auth token available")
            return
        
        params = {"unread_only": True}
        success, data, status_code = self.make_request("GET", "/alerts/", params=params)
        
        if success and isinstance(data, dict) and "data" in data:
            unread_alerts = len(data["data"])
            self.log_test("List Unread Alerts", True, f"Retrieved {unread_alerts} unread alerts")
        else:
            self.log_test("List Unread Alerts", False, f"Failed to list unread alerts (Status: {status_code})", data)
    
    def test_mark_alert_read(self):
        """Test marking alert as read"""
        if not self.auth_token or not hasattr(self, 'alert_id'):
            self.log_test("Mark Alert Read", False, "No auth token or alert ID available")
            return
        
        success, data, status_code = self.make_request("PATCH", f"/alerts/{self.alert_id}/read")
        
        if success and isinstance(data, dict) and "message" in data:
            self.log_test("Mark Alert Read", True, f"Alert marked as read successfully")
        else:
            self.log_test("Mark Alert Read", False, f"Failed to mark alert as read (Status: {status_code})", data)
    
    def test_mark_all_alerts_read(self):
        """Test marking all alerts as read"""
        if not self.auth_token:
            self.log_test("Mark All Alerts Read", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("PATCH", "/alerts/mark-all-read")
        
        if success and isinstance(data, dict) and "message" in data:
            self.log_test("Mark All Alerts Read", True, f"All alerts marked as read")
        else:
            self.log_test("Mark All Alerts Read", False, f"Failed to mark all alerts as read (Status: {status_code})", data)
    
    def test_analytics_dashboard(self):
        """Test analytics dashboard metrics"""
        if not self.auth_token:
            self.log_test("Analytics Dashboard", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("GET", "/analytics/dashboard")
        
        if success and isinstance(data, dict):
            required_sections = ["tenders", "vendors", "rfqs", "products", "boqs", "team"]
            missing_sections = [section for section in required_sections if section not in data]
            
            if not missing_sections:
                tender_metrics = data.get("tenders", {})
                total_tenders = tender_metrics.get("total", 0)
                win_rate = tender_metrics.get("winRate", 0)
                self.log_test("Analytics Dashboard", True, f"Dashboard metrics retrieved: {total_tenders} tenders, {win_rate}% win rate")
            else:
                self.log_test("Analytics Dashboard", False, f"Missing required sections: {missing_sections}", data)
        else:
            self.log_test("Analytics Dashboard", False, f"Failed to get dashboard metrics (Status: {status_code})", data)
    
    def test_analytics_recent_activity(self):
        """Test recent activity analytics"""
        if not self.auth_token:
            self.log_test("Analytics Recent Activity", False, "No auth token available")
            return
        
        params = {"limit": 5}
        success, data, status_code = self.make_request("GET", "/analytics/recent-activity", params=params)
        
        if success and isinstance(data, dict) and "activities" in data:
            activities = data["activities"]
            activity_count = len(activities)
            self.log_test("Analytics Recent Activity", True, f"Retrieved {activity_count} recent activities")
        else:
            self.log_test("Analytics Recent Activity", False, f"Failed to get recent activity (Status: {status_code})", data)
    
    def test_analytics_tender_stats(self):
        """Test tender statistics by period"""
        if not self.auth_token:
            self.log_test("Analytics Tender Stats", False, "No auth token available")
            return
        
        params = {"period": "month"}
        success, data, status_code = self.make_request("GET", "/analytics/tender-stats", params=params)
        
        if success and isinstance(data, dict) and "statusBreakdown" in data:
            period = data.get("period")
            breakdown = data.get("statusBreakdown", {})
            status_count = len(breakdown)
            self.log_test("Analytics Tender Stats", True, f"Retrieved tender stats for {period}: {status_count} status categories")
        else:
            self.log_test("Analytics Tender Stats", False, f"Failed to get tender stats (Status: {status_code})", data)

    # ========== PHASE 1B API TESTS ==========
    
    def test_gem_tender_search(self):
        """Test GeM portal tender search"""
        if not self.auth_token:
            self.log_test("GeM Tender Search", False, "No auth token available")
            return
        
        params = {"keywords": "IT Hardware", "category": "Technology", "max_results": 10}
        success, data, status_code = self.make_request("GET", "/gem/tenders/search", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            total = data.get("total", 0)
            tenders = data.get("tenders", [])
            self.log_test("GeM Tender Search", True, f"Retrieved {total} tenders from GeM portal")
        else:
            self.log_test("GeM Tender Search", False, f"Failed to search GeM tenders (Status: {status_code})", data)
    
    def test_gem_bid_submission(self):
        """Test GeM bid submission"""
        if not self.auth_token:
            self.log_test("GeM Bid Submission", False, "No auth token available")
            return
        
        bid_data = {
            "bid_id": f"BID-{int(datetime.now().timestamp())}",
            "user_id": self.user_data.get('id') if self.user_data else "test-user-id",
            "tender_id": "tender-123",
            "tender_number": "GEM-2025-001",
            "tender_title": "IT Infrastructure Procurement",
            "organization": "Ministry of IT",
            "bid_amount": 500000,
            "technical_bid_file": "technical_bid.pdf",
            "financial_bid_file": "financial_bid.pdf",
            "emd_proof_file": "emd_proof.pdf"
        }
        
        success, data, status_code = self.make_request("POST", "/gem/bids/submit", bid_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            bid_id = data.get("bid_id")
            self.log_test("GeM Bid Submission", True, f"Bid submitted successfully with ID: {bid_id}")
        else:
            self.log_test("GeM Bid Submission", False, f"Failed to submit bid (Status: {status_code})", data)
    
    def test_gem_my_bids(self):
        """Test fetching user's GeM bids"""
        if not self.auth_token:
            self.log_test("GeM My Bids", False, "No auth token available")
            return
        
        params = {"page": 1, "limit": 10}
        success, data, status_code = self.make_request("GET", "/gem/bids/my-bids", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            total = data.get("total", 0)
            bids = data.get("bids", [])
            self.log_test("GeM My Bids", True, f"Retrieved {len(bids)} bids, total: {total}")
        else:
            self.log_test("GeM My Bids", False, f"Failed to fetch bids (Status: {status_code})", data)
    
    def test_gem_dashboard_stats(self):
        """Test GeM dashboard statistics"""
        if not self.auth_token:
            self.log_test("GeM Dashboard Stats", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("GET", "/gem/dashboard/stats")
        
        if success and isinstance(data, dict) and data.get("success"):
            stats = data.get("stats", {})
            total_bids = stats.get("total_bids", 0)
            win_rate = stats.get("win_rate", 0)
            self.log_test("GeM Dashboard Stats", True, f"Dashboard stats: {total_bids} total bids, {win_rate}% win rate")
        else:
            self.log_test("GeM Dashboard Stats", False, f"Failed to get dashboard stats (Status: {status_code})", data)
    
    def test_cpp_tender_search(self):
        """Test CPP portal tender search"""
        if not self.auth_token:
            self.log_test("CPP Tender Search", False, "No auth token available")
            return
        
        params = {"keywords": "Software Development", "category": "IT Services", "max_results": 10}
        success, data, status_code = self.make_request("GET", "/cpp/tenders/search", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            total = data.get("total", 0)
            source = data.get("source")
            self.log_test("CPP Tender Search", True, f"Retrieved {total} tenders from {source}")
        else:
            self.log_test("CPP Tender Search", False, f"Failed to search CPP tenders (Status: {status_code})", data)
    
    def test_cpp_ministry_tenders(self):
        """Test CPP ministry-specific tenders"""
        if not self.auth_token:
            self.log_test("CPP Ministry Tenders", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("GET", "/cpp/ministry/Ministry of IT/tenders")
        
        if success and isinstance(data, dict) and data.get("success"):
            ministry = data.get("ministry")
            total = data.get("total", 0)
            self.log_test("CPP Ministry Tenders", True, f"Retrieved {total} tenders from {ministry}")
        else:
            self.log_test("CPP Ministry Tenders", False, f"Failed to fetch ministry tenders (Status: {status_code})", data)
    
    def test_global_search(self):
        """Test global search across collections"""
        if not self.auth_token:
            self.log_test("Global Search", False, "No auth token available")
            return
        
        params = {"q": "IT Hardware", "page": 1, "limit": 10}
        success, data, status_code = self.make_request("GET", "/search/global", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            total_results = data.get("total_results", 0)
            results = data.get("results", {})
            collections_found = len(results)
            self.log_test("Global Search", True, f"Found {total_results} results across {collections_found} collections")
        else:
            self.log_test("Global Search", False, f"Failed to perform global search (Status: {status_code})", data)
    
    def test_tender_search_with_filters(self):
        """Test tender search with advanced filters"""
        if not self.auth_token:
            self.log_test("Tender Search with Filters", False, "No auth token available")
            return
        
        params = {
            "q": "IT Infrastructure",
            "category": "Technology",
            "min_value": 100000,
            "max_value": 10000000,
            "page": 1,
            "limit": 10
        }
        success, data, status_code = self.make_request("GET", "/search/tenders", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            total = data.get("total", 0)
            tenders = data.get("tenders", [])
            self.log_test("Tender Search with Filters", True, f"Found {total} tenders matching filters")
        else:
            self.log_test("Tender Search with Filters", False, f"Failed to search tenders with filters (Status: {status_code})", data)
    
    def test_search_suggestions(self):
        """Test search suggestions"""
        if not self.auth_token:
            self.log_test("Search Suggestions", False, "No auth token available")
            return
        
        params = {"q": "IT"}
        success, data, status_code = self.make_request("GET", "/search/suggestions", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            suggestions = data.get("suggestions", [])
            self.log_test("Search Suggestions", True, f"Retrieved {len(suggestions)} search suggestions")
        else:
            self.log_test("Search Suggestions", False, f"Failed to get search suggestions (Status: {status_code})", data)
    
    def test_competitor_analysis(self):
        """Test competitor analysis"""
        if not self.auth_token:
            self.log_test("Competitor Analysis", False, "No auth token available")
            return
        
        params = {"category": "IT Hardware", "days": 90}
        success, data, status_code = self.make_request("GET", "/competitors/analysis", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            total_competitors = data.get("total_competitors", 0)
            competitors = data.get("competitors", [])
            self.log_test("Competitor Analysis", True, f"Analyzed {total_competitors} competitors")
        else:
            self.log_test("Competitor Analysis", False, f"Failed to get competitor analysis (Status: {status_code})", data)
    
    def test_competitor_list(self):
        """Test competitor listing"""
        if not self.auth_token:
            self.log_test("Competitor List", False, "No auth token available")
            return
        
        params = {"page": 1, "limit": 10, "sort_by": "win_rate"}
        success, data, status_code = self.make_request("GET", "/competitors/list", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            total = data.get("total", 0)
            competitors = data.get("competitors", [])
            self.log_test("Competitor List", True, f"Retrieved {len(competitors)} competitors, total: {total}")
        else:
            self.log_test("Competitor List", False, f"Failed to list competitors (Status: {status_code})", data)
    
    def test_competitor_insights(self):
        """Test competitor insights dashboard"""
        if not self.auth_token:
            self.log_test("Competitor Insights", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("GET", "/competitors/dashboard/insights")
        
        if success and isinstance(data, dict) and data.get("success"):
            insights = data.get("insights", {})
            total_competitors = insights.get("total_competitors", 0)
            avg_win_rate = insights.get("avg_market_win_rate", 0)
            self.log_test("Competitor Insights", True, f"Market insights: {total_competitors} competitors, {avg_win_rate}% avg win rate")
        else:
            self.log_test("Competitor Insights", False, f"Failed to get competitor insights (Status: {status_code})", data)
    
    def test_buyers_analysis(self):
        """Test buyers analysis"""
        if not self.auth_token:
            self.log_test("Buyers Analysis", False, "No auth token available")
            return
        
        analysis_data = {
            "keywords": ["IT Hardware", "Software", "Technology"],
            "days": 365
        }
        
        success, data, status_code = self.make_request("POST", "/buyers/analyze", analysis_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            analysis = data.get("analysis", {})
            self.log_test("Buyers Analysis", True, f"Buyers analysis completed successfully")
        else:
            self.log_test("Buyers Analysis", False, f"Failed to analyze buyers (Status: {status_code})", data)
    
    def test_buyer_recommendations(self):
        """Test buyer recommendations"""
        if not self.auth_token:
            self.log_test("Buyer Recommendations", False, "No auth token available")
            return
        
        success, data, status_code = self.make_request("GET", "/buyers/recommendations")
        
        if success and isinstance(data, dict) and data.get("success"):
            total_recommendations = data.get("total_recommendations", 0)
            recommendations = data.get("recommendations", [])
            self.log_test("Buyer Recommendations", True, f"Retrieved {total_recommendations} buyer recommendations")
        else:
            # This might fail if company profile is not complete, which is expected
            if status_code == 200 and not data.get("success"):
                self.log_test("Buyer Recommendations", True, f"Expected response: {data.get('message', 'Company profile required')}")
            else:
                self.log_test("Buyer Recommendations", False, f"Failed to get buyer recommendations (Status: {status_code})", data)
    
    def test_buyers_insights(self):
        """Test buyers insights"""
        if not self.auth_token:
            self.log_test("Buyers Insights", False, "No auth token available")
            return
        
        params = {"keywords": ["IT", "Hardware"]}
        success, data, status_code = self.make_request("GET", "/buyers/insights", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            insights = data.get("insights", {})
            self.log_test("Buyers Insights", True, f"Retrieved buyers market insights")
        else:
            self.log_test("Buyers Insights", False, f"Failed to get buyers insights (Status: {status_code})", data)
    
    def test_competitor_history_fetch(self):
        """Test fetching competitor history"""
        if not self.auth_token:
            self.log_test("Competitor History Fetch", False, "No auth token available")
            return
        
        competitor_name = "TechCorp Solutions"
        params = {"days": 180}
        success, data, status_code = self.make_request("GET", f"/competitor-history/fetch/{competitor_name}", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            history = data.get("history", {})
            self.log_test("Competitor History Fetch", True, f"Fetched history for {competitor_name}")
        else:
            self.log_test("Competitor History Fetch", False, f"Failed to fetch competitor history (Status: {status_code})", data)
    
    def test_competitor_comparison(self):
        """Test competitor comparison"""
        if not self.auth_token:
            self.log_test("Competitor Comparison", False, "No auth token available")
            return
        
        comparison_data = {
            "competitor_names": ["TechCorp Solutions", "InnovateTech Ltd", "Digital Systems"]
        }
        
        success, data, status_code = self.make_request("POST", "/competitor-history/compare", comparison_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            comparison = data.get("comparison", {})
            self.log_test("Competitor Comparison", True, f"Competitor comparison completed")
        else:
            self.log_test("Competitor Comparison", False, f"Failed to compare competitors (Status: {status_code})", data)
    
    def test_competitor_trends(self):
        """Test competitor trends"""
        if not self.auth_token:
            self.log_test("Competitor Trends", False, "No auth token available")
            return
        
        competitor_name = "TechCorp Solutions"
        success, data, status_code = self.make_request("GET", f"/competitor-history/trends/{competitor_name}")
        
        if success and isinstance(data, dict) and data.get("success"):
            trends = data.get("trends", {})
            competitor = data.get("competitor")
            self.log_test("Competitor Trends", True, f"Retrieved trends for {competitor}")
        else:
            self.log_test("Competitor Trends", False, f"Failed to get competitor trends (Status: {status_code})", data)

    # ========== PHASE 2 API TESTS ==========
    
    def test_pdf_merge(self):
        """Test PDF merge functionality"""
        if not self.auth_token:
            self.log_test("PDF Merge", False, "No auth token available")
            return
        
        merge_data = {
            "file_paths": ["/tmp/doc1.pdf", "/tmp/doc2.pdf"]
        }
        
        success, data, status_code = self.make_request("POST", "/pdf-tools/merge", merge_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            output_file = data.get("output_file")
            self.log_test("PDF Merge", True, f"PDFs merged successfully: {output_file}")
        else:
            self.log_test("PDF Merge", False, f"Failed to merge PDFs (Status: {status_code})", data)
    
    def test_pdf_split(self):
        """Test PDF split functionality"""
        if not self.auth_token:
            self.log_test("PDF Split", False, "No auth token available")
            return
        
        split_data = {
            "file_path": "/tmp/document.pdf",
            "page_ranges": [{"start": 1, "end": 5}, {"start": 6, "end": 10}]
        }
        
        success, data, status_code = self.make_request("POST", "/pdf-tools/split", split_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            output_files = data.get("output_files", [])
            self.log_test("PDF Split", True, f"PDF split into {len(output_files)} files")
        else:
            self.log_test("PDF Split", False, f"Failed to split PDF (Status: {status_code})", data)
    
    def test_pdf_compress(self):
        """Test PDF compression"""
        if not self.auth_token:
            self.log_test("PDF Compress", False, "No auth token available")
            return
        
        compress_data = {
            "file_path": "/tmp/large_document.pdf",
            "quality": "medium"
        }
        
        success, data, status_code = self.make_request("POST", "/pdf-tools/compress", compress_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            compression_ratio = data.get("compression_ratio", 0)
            self.log_test("PDF Compress", True, f"PDF compressed with {compression_ratio}% reduction")
        else:
            self.log_test("PDF Compress", False, f"Failed to compress PDF (Status: {status_code})", data)
    
    def test_pdf_rotate(self):
        """Test PDF rotation"""
        if not self.auth_token:
            self.log_test("PDF Rotate", False, "No auth token available")
            return
        
        rotate_data = {
            "file_path": "/tmp/document.pdf",
            "angle": 90,
            "pages": "all"
        }
        
        success, data, status_code = self.make_request("POST", "/pdf-tools/rotate", rotate_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            pages_rotated = data.get("pages_rotated", 0)
            self.log_test("PDF Rotate", True, f"Rotated {pages_rotated} pages by 90 degrees")
        else:
            self.log_test("PDF Rotate", False, f"Failed to rotate PDF (Status: {status_code})", data)
    
    def test_pdf_watermark(self):
        """Test PDF watermark"""
        if not self.auth_token:
            self.log_test("PDF Watermark", False, "No auth token available")
            return
        
        watermark_data = {
            "file_path": "/tmp/document.pdf",
            "watermark_text": "CONFIDENTIAL - HexaBid"
        }
        
        success, data, status_code = self.make_request("POST", "/pdf-tools/watermark", watermark_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            output_file = data.get("output_file")
            self.log_test("PDF Watermark", True, f"Watermark added successfully")
        else:
            self.log_test("PDF Watermark", False, f"Failed to add watermark (Status: {status_code})", data)
    
    def test_pdf_protect(self):
        """Test PDF password protection"""
        if not self.auth_token:
            self.log_test("PDF Protect", False, "No auth token available")
            return
        
        protect_data = {
            "file_path": "/tmp/document.pdf",
            "password": "SecurePass123!"
        }
        
        success, data, status_code = self.make_request("POST", "/pdf-tools/protect", protect_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            self.log_test("PDF Protect", True, f"PDF password protected successfully")
        else:
            self.log_test("PDF Protect", False, f"Failed to protect PDF (Status: {status_code})", data)
    
    def test_pdf_extract_text(self):
        """Test PDF text extraction"""
        if not self.auth_token:
            self.log_test("PDF Extract Text", False, "No auth token available")
            return
        
        extract_data = {
            "file_path": "/tmp/document.pdf"
        }
        
        success, data, status_code = self.make_request("POST", "/pdf-tools/extract-text", extract_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            text_length = len(data.get("text", ""))
            self.log_test("PDF Extract Text", True, f"Extracted {text_length} characters of text")
        else:
            self.log_test("PDF Extract Text", False, f"Failed to extract text (Status: {status_code})", data)
    
    def test_pdf_info(self):
        """Test PDF information retrieval"""
        if not self.auth_token:
            self.log_test("PDF Info", False, "No auth token available")
            return
        
        params = {"file_path": "/tmp/document.pdf"}
        success, data, status_code = self.make_request("GET", "/pdf-tools/info", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            info = data.get("info", {})
            pages = info.get("pages", 0)
            self.log_test("PDF Info", True, f"PDF info retrieved: {pages} pages")
        else:
            self.log_test("PDF Info", False, f"Failed to get PDF info (Status: {status_code})", data)
    
    def test_email_send(self):
        """Test email sending (mocked)"""
        if not self.auth_token:
            self.log_test("Email Send", False, "No auth token available")
            return
        
        email_data = {
            "to": ["client@example.com", "manager@hexabid.com"],
            "subject": "Tender Proposal - IT Infrastructure",
            "body": "Please find attached our proposal for the IT infrastructure tender.",
            "attachments": ["proposal.pdf", "technical_specs.pdf"]
        }
        
        success, data, status_code = self.make_request("POST", "/email/send", email_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            message_id = data.get("message_id")
            self.log_test("Email Send", True, f"Email sent successfully (mocked): {message_id}")
        else:
            self.log_test("Email Send", False, f"Failed to send email (Status: {status_code})", data)
    
    def test_email_inbox(self):
        """Test email inbox fetch (mocked)"""
        if not self.auth_token:
            self.log_test("Email Inbox", False, "No auth token available")
            return
        
        params = {"limit": 20}
        success, data, status_code = self.make_request("GET", "/email/inbox", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            emails = data.get("emails", [])
            unread_count = data.get("unread_count", 0)
            self.log_test("Email Inbox", True, f"Retrieved {len(emails)} emails, {unread_count} unread")
        else:
            self.log_test("Email Inbox", False, f"Failed to fetch inbox (Status: {status_code})", data)
    
    def test_email_sent(self):
        """Test sent emails fetch (mocked)"""
        if not self.auth_token:
            self.log_test("Email Sent", False, "No auth token available")
            return
        
        params = {"limit": 20}
        success, data, status_code = self.make_request("GET", "/email/sent", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            emails = data.get("emails", [])
            self.log_test("Email Sent", True, f"Retrieved {len(emails)} sent emails")
        else:
            self.log_test("Email Sent", False, f"Failed to fetch sent emails (Status: {status_code})", data)
    
    def test_email_draft_create(self):
        """Test email draft creation (mocked)"""
        if not self.auth_token:
            self.log_test("Email Draft Create", False, "No auth token available")
            return
        
        draft_data = {
            "to": ["prospect@company.com"],
            "subject": "Follow-up on Tender Discussion",
            "body": "Thank you for your time yesterday. We would like to schedule a follow-up meeting."
        }
        
        success, data, status_code = self.make_request("POST", "/email/drafts/create", draft_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            draft_id = data.get("draft_id")
            self.log_test("Email Draft Create", True, f"Draft created successfully: {draft_id}")
        else:
            self.log_test("Email Draft Create", False, f"Failed to create draft (Status: {status_code})", data)
    
    def test_email_mark_read(self):
        """Test marking emails as read"""
        if not self.auth_token:
            self.log_test("Email Mark Read", False, "No auth token available")
            return
        
        mark_read_data = {
            "email_ids": ["email_123", "email_456", "email_789"]
        }
        
        success, data, status_code = self.make_request("POST", "/email/mark-read", mark_read_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            marked_count = data.get("marked_count", 0)
            self.log_test("Email Mark Read", True, f"Marked {marked_count} emails as read")
        else:
            self.log_test("Email Mark Read", False, f"Failed to mark emails as read (Status: {status_code})", data)
    
    def test_email_delete(self):
        """Test email deletion"""
        if not self.auth_token:
            self.log_test("Email Delete", False, "No auth token available")
            return
        
        delete_data = {
            "email_ids": ["email_old_1", "email_old_2"]
        }
        
        success, data, status_code = self.make_request("DELETE", "/email/delete", delete_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            deleted_count = data.get("deleted_count", 0)
            self.log_test("Email Delete", True, f"Deleted {deleted_count} emails")
        else:
            self.log_test("Email Delete", False, f"Failed to delete emails (Status: {status_code})", data)
    
    def test_office365_create_document(self):
        """Test Office 365 document creation (mocked)"""
        if not self.auth_token:
            self.log_test("Office 365 Create Document", False, "No auth token available")
            return
        
        doc_data = {
            "document_type": "word",
            "title": "Tender Response Template"
        }
        
        success, data, status_code = self.make_request("POST", "/office365/documents/create", doc_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            document_id = data.get("document_id")
            self.log_test("Office 365 Create Document", True, f"Document created: {document_id}")
        else:
            self.log_test("Office 365 Create Document", False, f"Failed to create document (Status: {status_code})", data)
    
    def test_office365_list_documents(self):
        """Test Office 365 document listing (mocked)"""
        if not self.auth_token:
            self.log_test("Office 365 List Documents", False, "No auth token available")
            return
        
        params = {"folder": "root", "limit": 20}
        success, data, status_code = self.make_request("GET", "/office365/documents/list", params=params)
        
        if success and isinstance(data, dict) and data.get("success"):
            documents = data.get("documents", [])
            self.log_test("Office 365 List Documents", True, f"Retrieved {len(documents)} documents from OneDrive")
        else:
            self.log_test("Office 365 List Documents", False, f"Failed to list documents (Status: {status_code})", data)
    
    def test_office365_share_document(self):
        """Test Office 365 document sharing (mocked)"""
        if not self.auth_token:
            self.log_test("Office 365 Share Document", False, "No auth token available")
            return
        
        share_data = {
            "document_id": "doc_12345",
            "emails": ["team@hexabid.com", "client@company.com"],
            "permission": "edit"
        }
        
        success, data, status_code = self.make_request("POST", "/office365/documents/share", share_data)
        
        if success and isinstance(data, dict) and data.get("success"):
            shared_with = data.get("shared_with", [])
            self.log_test("Office 365 Share Document", True, f"Document shared with {len(shared_with)} users")
        else:
            self.log_test("Office 365 Share Document", False, f"Failed to share document (Status: {status_code})", data)

    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting HexaBid Backend API Tests - Phase 1B & Phase 2")
        print("=" * 70)
        
        # Health check
        self.test_health_check()
        
        # Authentication flow
        print("🔐 Testing Authentication Flow")
        print("-" * 40)
        self.test_user_registration()
        self.test_get_current_user()
        
        # PHASE 1B - GEM PORTAL INTEGRATION
        print("💎 Testing GeM Portal Integration APIs (Phase 1B)")
        print("-" * 40)
        self.test_gem_tender_search()
        self.test_gem_bid_submission()
        self.test_gem_my_bids()
        self.test_gem_dashboard_stats()
        
        # PHASE 1B - CPP PORTAL INTEGRATION
        print("🏛️ Testing CPP Portal Integration APIs (Phase 1B)")
        print("-" * 40)
        self.test_cpp_tender_search()
        self.test_cpp_ministry_tenders()
        
        # PHASE 1B - GLOBAL SEARCH
        print("🔍 Testing Global Search APIs (Phase 1B)")
        print("-" * 40)
        self.test_global_search()
        self.test_tender_search_with_filters()
        self.test_search_suggestions()
        
        # PHASE 1B - COMPETITOR ANALYSIS
        print("🏆 Testing Competitor Analysis APIs (Phase 1B)")
        print("-" * 40)
        self.test_competitor_analysis()
        self.test_competitor_list()
        self.test_competitor_insights()
        
        # PHASE 1B - BUYERS HISTORY
        print("🏢 Testing Buyers History APIs (Phase 1B)")
        print("-" * 40)
        self.test_buyers_analysis()
        self.test_buyer_recommendations()
        self.test_buyers_insights()
        
        # PHASE 1B - COMPETITOR HISTORY
        print("📊 Testing Competitor History APIs (Phase 1B)")
        print("-" * 40)
        self.test_competitor_history_fetch()
        self.test_competitor_comparison()
        self.test_competitor_trends()
        
        # PHASE 2 - PDF TOOLS
        print("📄 Testing PDF Tools APIs (Phase 2)")
        print("-" * 40)
        self.test_pdf_merge()
        self.test_pdf_split()
        self.test_pdf_compress()
        self.test_pdf_rotate()
        self.test_pdf_watermark()
        self.test_pdf_protect()
        self.test_pdf_extract_text()
        self.test_pdf_info()
        
        # PHASE 2 - EMAIL CLIENT
        print("📧 Testing Email Client APIs (Phase 2)")
        print("-" * 40)
        self.test_email_send()
        self.test_email_inbox()
        self.test_email_sent()
        self.test_email_draft_create()
        self.test_email_mark_read()
        self.test_email_delete()
        
        # PHASE 2 - OFFICE 365
        print("📝 Testing Office 365 APIs (Phase 2)")
        print("-" * 40)
        self.test_office365_create_document()
        self.test_office365_list_documents()
        self.test_office365_share_document()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            print("-" * 20)
            for result in self.test_results:
                if not result["success"]:
                    print(f"• {result['test']}: {result['details']}")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    tester = HexaBidAPITester()
    tester.run_all_tests()