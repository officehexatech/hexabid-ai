import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class BuyersHistoryService:
    """Service to track and analyze buyer history based on company profile keywords"""
    
    def __init__(self):
        self.buyer_profiles = {}
    
    def analyze_buyers_for_keywords(self, keywords: List[str], days: int = 365) -> Dict[str, Any]:
        """
        Analyze buyer organizations based on keywords from company profile
        Returns historical buying patterns and tender preferences
        """
        logger.info(f"Analyzing buyer history for keywords: {keywords}")
        
        buyers = self._generate_buyer_profiles(keywords, days)
        
        return {
            'keywords_analyzed': keywords,
            'time_period_days': days,
            'total_buyers_found': len(buyers),
            'buyers': buyers,
            'insights': self._generate_insights(buyers, keywords)
        }
    
    def _generate_buyer_profiles(self, keywords: List[str], days: int) -> List[Dict[str, Any]]:
        """Generate mock buyer profiles based on keywords"""
        organizations = [
            'Indian Railways', 'AIIMS Delhi', 'IIT Bombay', 'DRDO',
            'Ministry of Defence', 'BHEL', 'NTPC', 'Coal India',
            'Oil India', 'SAIL', 'HAL', 'BEL', 'ISRO'
        ]
        
        buyers = []
        base_date = datetime.now()
        
        for i, org in enumerate(organizations[:10]):
            # Calculate frequency based on keyword relevance
            relevance_score = random.randint(60, 95)
            
            buyer = {
                'organization_name': org,
                'buyer_id': f'BYR{1000 + i}',
                'relevance_score': relevance_score,
                'total_tenders_posted': random.randint(15, 50),
                'avg_tender_value': random.randint(1000000, 10000000),
                'preferred_categories': random.sample(keywords, min(len(keywords), 3)),
                'tender_frequency': random.choice(['Weekly', 'Bi-weekly', 'Monthly']),
                'avg_response_time': f"{random.randint(15, 45)} days",
                'success_rate_with_us': random.randint(20, 60) if i < 5 else 0,
                'recent_tenders': [
                    {
                        'tender_id': f'TND{base_date.year}/{random.randint(10000, 99999)}',
                        'title': f"{random.choice(keywords)} procurement",
                        'value': random.randint(500000, 5000000),
                        'posted_date': (base_date - timedelta(days=random.randint(1, days))).strftime('%Y-%m-%d'),
                        'status': random.choice(['Open', 'Awarded', 'Under Evaluation'])
                    }
                    for _ in range(3)
                ],
                'contact_info': {
                    'email': f"procurement@{org.lower().replace(' ', '')}.gov.in",
                    'phone': f"+91-11-{random.randint(20000000, 29999999)}"
                },
                'procurement_patterns': {
                    'peak_months': random.sample(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 3),
                    'avg_emd_percentage': f"{random.randint(2, 5)}%",
                    'payment_terms': random.choice(['30 days', '45 days', '60 days', '90 days']),
                    'preferred_bid_type': random.choice(['L1', 'QCBS', 'Technical-Commercial'])
                }
            }
            buyers.append(buyer)
        
        # Sort by relevance score
        buyers.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return buyers
    
    def _generate_insights(self, buyers: List[Dict], keywords: List[str]) -> Dict[str, Any]:
        """Generate actionable insights from buyer data"""
        if not buyers:
            return {}
        
        total_tenders = sum(b['total_tenders_posted'] for b in buyers)
        avg_value = sum(b['avg_tender_value'] for b in buyers) / len(buyers)
        
        # Find most active buyer
        most_active = max(buyers, key=lambda x: x['total_tenders_posted'])
        
        # Find buyer with best success rate
        buyers_with_history = [b for b in buyers if b['success_rate_with_us'] > 0]
        best_success = max(buyers_with_history, key=lambda x: x['success_rate_with_us']) if buyers_with_history else None
        
        return {
            'total_opportunities': total_tenders,
            'avg_tender_value': round(avg_value, 2),
            'most_active_buyer': most_active['organization_name'],
            'best_success_rate_buyer': best_success['organization_name'] if best_success else None,
            'recommended_targets': [b['organization_name'] for b in buyers[:3]],
            'keyword_coverage': {
                keyword: sum(1 for b in buyers if keyword in b['preferred_categories'])
                for keyword in keywords
            }
        }
    
    def get_buyer_recommendations(self, company_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get recommended buyers based on company profile"""
        keywords = company_profile.get('keywords', [])
        categories = company_profile.get('categories', [])
        
        all_keywords = keywords + categories
        
        if not all_keywords:
            return []
        
        result = self.analyze_buyers_for_keywords(all_keywords)
        return result['buyers'][:5]  # Top 5 recommendations

# Global instance
buyers_history_service = BuyersHistoryService()
