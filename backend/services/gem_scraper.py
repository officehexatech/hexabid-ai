import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re
import time

logger = logging.getLogger(__name__)

class GEMPortalScraper:
    """Scraper for GeM (Government e-Marketplace) portal"""
    
    BASE_URL = "https://gem.gov.in"
    SEARCH_URL = "https://gem.gov.in/search"
    BID_URL = "https://gem.gov.in/bid"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_tenders(self, keywords: str, category: str = None, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search for tenders on GeM portal
        Note: This is a mock implementation as actual GeM API requires authentication
        """
        logger.info(f"Searching GeM for tenders: {keywords}")
        
        # Mock data for development - In production, this would use actual GeM API
        mock_tenders = self._generate_mock_gem_tenders(keywords, category, max_results)
        
        return mock_tenders
    
    def _generate_mock_gem_tenders(self, keywords: str, category: str, count: int) -> List[Dict[str, Any]]:
        """Generate mock tender data for testing"""
        categories = ['IT Hardware', 'IT Software', 'Office Equipment', 'Furniture', 'Vehicles', 'Medical Equipment']
        organizations = ['Ministry of Defence', 'Railways', 'AIIMS Delhi', 'IIT Delhi', 'DRDO', 'ISRO']
        
        tenders = []
        base_date = datetime.now()
        
        for i in range(min(count, 20)):
            tender = {
                'tender_number': f'GEM/{base_date.year}/{100000 + i}',
                'title': f'{keywords} - {categories[i % len(categories)]} Procurement',
                'organization': organizations[i % len(organizations)],
                'department': 'Procurement Division',
                'category': category or categories[i % len(categories)],
                'location': ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad'][i % 4],
                'publish_date': (base_date - timedelta(days=i*2)).strftime('%Y-%m-%d'),
                'submission_deadline': (base_date + timedelta(days=15+i)).strftime('%Y-%m-%d'),
                'tender_value': 1000000 + (i * 500000),
                'emd_amount': 20000 + (i * 10000),
                'source': 'gem',
                'document_url': f'https://gem.gov.in/tender/{100000 + i}',
                'status': 'open',
                'description': f'Procurement of {keywords} as per specifications',
                'estimated_bid_value': 800000 + (i * 400000)
            }
            tenders.append(tender)
        
        return tenders
    
    def get_tender_details(self, tender_number: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information about a specific tender"""
        logger.info(f"Fetching tender details: {tender_number}")
        
        # Mock implementation
        if 'GEM' in tender_number:
            return {
                'tender_number': tender_number,
                'title': 'Mock Tender Details',
                'organization': 'Government Organization',
                'detailed_description': 'Full tender description with technical specifications',
                'technical_requirements': [
                    'Requirement 1: Technical specification A',
                    'Requirement 2: Technical specification B',
                    'Requirement 3: Compliance requirement C'
                ],
                'eligibility_criteria': [
                    'Registered vendor on GeM',
                    'Minimum 3 years experience',
                    'Annual turnover > 1 Cr'
                ],
                'documents_required': [
                    'Technical bid',
                    'Financial bid',
                    'EMD proof',
                    'Company registration',
                    'GST certificate'
                ],
                'evaluation_criteria': 'L1 (Lowest bidder)',
                'payment_terms': '30 days from delivery',
                'delivery_period': '60 days from order'
            }
        
        return None
    
    def track_bid_status(self, bid_id: str) -> Dict[str, Any]:
        """Track the status of a submitted bid"""
        logger.info(f"Tracking bid status: {bid_id}")
        
        # Mock statuses
        statuses = ['submitted', 'under_evaluation', 'technical_approved', 'financial_opened', 'awarded', 'rejected']
        
        return {
            'bid_id': bid_id,
            'status': statuses[hash(bid_id) % len(statuses)],
            'last_updated': datetime.now().isoformat(),
            'remarks': 'Bid is under evaluation by the tender committee',
            'evaluation_stage': 'Technical evaluation',
            'ranking': None  # Will be available after evaluation
        }
    
    def get_bid_results(self, tender_number: str) -> Optional[Dict[str, Any]]:
        """Get results/winners for a tender"""
        logger.info(f"Fetching bid results: {tender_number}")
        
        # Mock results
        return {
            'tender_number': tender_number,
            'result_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'awarded',
            'winner': {
                'company_name': 'ABC Technologies Pvt Ltd',
                'bid_amount': 850000,
                'rank': 1
            },
            'total_bidders': 5,
            'our_bid': {
                'rank': 2,
                'bid_amount': 875000,
                'status': 'technically_qualified',
                'remarks': 'Technically qualified but L2 bidder'
            },
            'all_bids': [
                {'rank': 1, 'company': 'ABC Technologies', 'amount': 850000},
                {'rank': 2, 'company': 'Your Company', 'amount': 875000},
                {'rank': 3, 'company': 'XYZ Corp', 'amount': 920000}
            ]
        }
    
    def get_competitor_bids(self, category: str = None, days: int = 90) -> List[Dict[str, Any]]:
        """Get historical bid data for competitor analysis"""
        logger.info(f"Fetching competitor bids for category: {category}")
        
        competitors = [
            'ABC Technologies Pvt Ltd',
            'XYZ Corporation',
            'Tech Solutions India',
            'Digital Systems Ltd',
            'Innovative Tech Co'
        ]
        
        competitor_data = []
        for comp in competitors:
            competitor_data.append({
                'company_name': comp,
                'total_bids': hash(comp) % 50 + 10,
                'won_bids': hash(comp) % 20 + 5,
                'win_rate': ((hash(comp) % 20 + 5) / (hash(comp) % 50 + 10)) * 100,
                'avg_bid_amount': 800000 + (hash(comp) % 500000),
                'categories': [category] if category else ['IT Hardware', 'Software'],
                'recent_wins': [
                    {
                        'tender_number': f'GEM/2025/{hash(comp) % 10000}',
                        'title': 'Recent tender win',
                        'amount': 900000,
                        'date': (datetime.now() - timedelta(days=i*10)).strftime('%Y-%m-%d')
                    }
                    for i in range(3)
                ]
            })
        
        return competitor_data

# Global instance
gem_scraper = GEMPortalScraper()
