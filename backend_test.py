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
BASE_URL = "https://tender-master-4.preview.emergentagent.com/api"
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
                response = requests.delete(url, headers=self.headers, timeout=30)
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
        user_data = {
            "email": "john.doe@hexabid.com",
            "password": "SecurePass123!",
            "fullName": "John Doe",
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
        
        success, data, status_code = self.make_request("POST", "/rfq", rfq_data)
        
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
        success, data, status_code = self.make_request("GET", "/rfq", params=params)
        
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
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting HexaBid Backend API Tests")
        print("=" * 50)
        
        # Health check
        self.test_health_check()
        
        # Authentication flow
        print("🔐 Testing Authentication Flow")
        print("-" * 30)
        self.test_user_registration()
        # Note: We'll use the token from registration for subsequent tests
        # In a real scenario, you might want to test login separately
        self.test_get_current_user()
        
        # Vendors API
        print("🏢 Testing Vendors API")
        print("-" * 30)
        self.test_create_vendor()
        self.test_list_vendors()
        self.test_get_single_vendor()
        self.test_update_vendor()
        self.test_search_vendors()
        
        # Company Profile API
        print("🏛️ Testing Company Profile API")
        print("-" * 30)
        self.test_create_company_profile()
        self.test_get_company_profile()
        self.test_update_company_profile()
        
        # Team Management
        print("👥 Testing Team Management")
        print("-" * 30)
        self.test_invite_team_member()
        self.test_list_team_members()
        
        # RFQ API
        print("📋 Testing RFQ API")
        print("-" * 30)
        self.test_create_rfq()
        self.test_list_rfqs()
        self.test_get_rfq_details()
        
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