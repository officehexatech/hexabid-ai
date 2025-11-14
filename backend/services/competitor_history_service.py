import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class CompetitorHistoryService:
    """Service to fetch and analyze real competitor bidding history"""
    
    def __init__(self):
        pass
    
    def fetch_competitor_history_from_gem(self, competitor_name: str, days: int = 180) -> Dict[str, Any]:
        """
        Fetch competitor bidding history from GeM portal
        Mock implementation - would use actual GeM API in production
        """
        logger.info(f"Fetching competitor history for: {competitor_name}")
        
        return {
            'competitor_name': competitor_name,
            'data_source': 'gem.gov.in',
            'period_days': days,
            'last_updated': datetime.now().isoformat(),
            'bidding_history': self._generate_bidding_history(competitor_name, days),
            'statistics': self._calculate_statistics(competitor_name)
        }
    
    def _generate_bidding_history(self, competitor_name: str, days: int) -> List[Dict[str, Any]]:
        """Generate mock bidding history"""
        history = []
        base_date = datetime.now()
        
        # Generate 20-30 historical bids
        num_bids = random.randint(20, 30)
        
        for i in range(num_bids):
            bid_date = base_date - timedelta(days=random.randint(1, days))
            
            bid = {
                'bid_id': f'GEM/BID/{bid_date.year}/{random.randint(100000, 999999)}',
                'tender_id': f'GEM/{bid_date.year}/{random.randint(10000, 99999)}',
                'tender_title': f'Procurement of {random.choice(["IT Hardware", "Software", "Services", "Equipment"])}',
                'organization': random.choice(['Railways', 'AIIMS', 'IIT', 'DRDO', 'Ministry']),
                'bid_amount': random.randint(500000, 10000000),
                'bid_date': bid_date.strftime('%Y-%m-%d'),
                'result': random.choice(['Won', 'Lost', 'Under Evaluation', 'Technically Disqualified']),
                'rank': random.randint(1, 8) if random.random() > 0.3 else None,
                'total_bidders': random.randint(3, 15),
                'winning_amount': random.randint(480000, 9500000) if random.random() > 0.5 else None,
                'discount_offered': f"{random.randint(5, 25)}%",
                'category': random.choice(['IT Hardware', 'IT Software', 'Consulting', 'Supply'])
            }
            history.append(bid)
        
        # Sort by date (most recent first)
        history.sort(key=lambda x: x['bid_date'], reverse=True)
        
        return history
    
    def _calculate_statistics(self, competitor_name: str) -> Dict[str, Any]:
        """Calculate competitive statistics"""
        # Mock statistics
        total_bids = random.randint(50, 150)
        won_bids = int(total_bids * random.uniform(0.15, 0.35))
        
        return {
            'total_bids': total_bids,
            'won_bids': won_bids,
            'lost_bids': total_bids - won_bids,
            'win_rate': round((won_bids / total_bids) * 100, 2),
            'avg_bid_value': random.randint(800000, 5000000),
            'avg_discount': f"{random.randint(10, 20)}%",
            'active_categories': ['IT Hardware', 'Software', 'Services'],
            'preferred_buyers': [
                {'name': 'Indian Railways', 'bids': random.randint(5, 15)},
                {'name': 'AIIMS', 'bids': random.randint(3, 10)},
                {'name': 'IIT System', 'bids': random.randint(2, 8)}
            ],
            'pricing_strategy': random.choice(['Aggressive', 'Competitive', 'Premium']),
            'response_rate': f"{random.randint(75, 95)}%",
            'technical_qualification_rate': f"{random.randint(80, 98)}%"
        }
    
    def compare_with_competitors(self, our_data: Dict, competitor_list: List[str]) -> Dict[str, Any]:
        """Compare our performance with competitors"""
        competitor_data = []
        
        for comp_name in competitor_list[:5]:  # Limit to 5 competitors
            comp_history = self.fetch_competitor_history_from_gem(comp_name)
            competitor_data.append({
                'name': comp_name,
                'stats': comp_history['statistics']
            })
        
        # Market position analysis
        our_win_rate = our_data.get('win_rate', 0)
        avg_competitor_win_rate = sum(c['stats']['win_rate'] for c in competitor_data) / len(competitor_data) if competitor_data else 0
        
        return {
            'our_performance': our_data,
            'competitors': competitor_data,
            'market_position': {
                'our_win_rate': our_win_rate,
                'market_avg_win_rate': round(avg_competitor_win_rate, 2),
                'position': 'Above Average' if our_win_rate > avg_competitor_win_rate else 'Below Average',
                'improvement_potential': round(abs(our_win_rate - avg_competitor_win_rate), 2)
            },
            'recommendations': self._generate_recommendations(our_data, competitor_data)
        }
    
    def _generate_recommendations(self, our_data: Dict, competitor_data: List[Dict]) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        if len(competitor_data) == 0:
            return recommendations
        
        # Analyze pricing
        our_avg_bid = our_data.get('avg_bid_value', 0)
        competitor_avg = sum(c['stats']['avg_bid_value'] for c in competitor_data) / len(competitor_data)
        
        if our_avg_bid > competitor_avg * 1.1:
            recommendations.append("Consider more competitive pricing - your bids are 10%+ above market average")
        
        # Analyze win rate
        our_win_rate = our_data.get('win_rate', 0)
        best_competitor_win_rate = max(c['stats']['win_rate'] for c in competitor_data)
        
        if our_win_rate < best_competitor_win_rate * 0.8:
            recommendations.append(f"Focus on improving win rate - top competitor achieves {best_competitor_win_rate}%")
        
        # Category recommendations
        recommendations.append("Diversify into categories where competition is lower")
        recommendations.append("Focus on buyers with historical success")
        
        return recommendations

# Global instance
competitor_history_service = CompetitorHistoryService()
