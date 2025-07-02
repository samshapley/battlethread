#!/usr/bin/env python3
"""
Process Wikipedia battle data for BattleThread timeline.
Extracts dates, normalizes them, and creates an optimized dataset.
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class BattleDateProcessor:
    """Process battle dates from Wikipedia data."""
    
    def __init__(self):
        # Date patterns in order of preference (most specific to least)
        self.date_patterns = [
            # Full date: "12 September 490 BC"
            (r'(\d{1,2})\s+(\w+)\s+(\d{1,4})\s*(?:BC|BCE)', 'full_date_bc'),
            (r'(\d{1,2})\s+(\w+)\s+(\d{1,4})(?:\s*(?:AD|CE))?', 'full_date_ad'),
            
            # Month and year: "September 490 BC"
            (r'(\w+)\s+(\d{1,4})\s*(?:BC|BCE)', 'month_year_bc'),
            (r'(\w+)\s+(\d{1,4})(?:\s*(?:AD|CE))?', 'month_year_ad'),
            
            # Year only: "490 BC", "1066"
            (r'(\d{1,4})\s*(?:BC|BCE)', 'year_bc'),
            (r'(\d{3,4})(?:\s*(?:AD|CE))?', 'year_ad'),
            
            # Date ranges: "1-3 July 1863"
            (r'(\d{1,2})[-–]\d{1,2}\s+(\w+)\s+(\d{4})', 'date_range'),
            
            # Circa dates: "c. 732", "around 1415"
            (r'(?:c\.|circa|around)\s*(\d{1,4})\s*(?:BC|BCE)?', 'circa'),
        ]
        
        self.month_map = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        
    def extract_date(self, date_str: str) -> Optional[Dict]:
        """Extract and normalize date from string."""
        if not date_str:
            return None
            
        # Clean the string
        date_str = date_str.strip()
        # Remove references like <ref>
        date_str = re.sub(r'<[^>]+>', '', date_str)
        date_str = re.sub(r'\([^)]+\)', '', date_str)
        
        for pattern, pattern_type in self.date_patterns:
            match = re.search(pattern, date_str, re.IGNORECASE)
            if match:
                return self.parse_match(match, pattern_type, date_str)
        
        return None
    
    def parse_match(self, match, pattern_type: str, original: str) -> Dict:
        """Parse regex match into structured date data."""
        result = {
            'original': original,
            'confidence': 'low',
            'display': original,
            'sortKey': 0,
            'year': None,
            'era': 'AD'
        }
        
        try:
            if pattern_type == 'full_date_bc':
                day, month, year = match.groups()
                result['year'] = -int(year)
                result['confidence'] = 'high'
                result['era'] = 'BC'
                result['display'] = f"{day} {month} {year} BC"
                
            elif pattern_type == 'full_date_ad':
                day, month, year = match.groups()
                result['year'] = int(year)
                result['confidence'] = 'high'
                result['display'] = f"{day} {month} {year}"
                
            elif pattern_type == 'month_year_bc':
                month, year = match.groups()
                result['year'] = -int(year)
                result['confidence'] = 'medium'
                result['era'] = 'BC'
                result['display'] = f"{month} {year} BC"
                
            elif pattern_type == 'month_year_ad':
                month, year = match.groups()
                result['year'] = int(year)
                result['confidence'] = 'medium'
                result['display'] = f"{month} {year}"
                
            elif pattern_type == 'year_bc':
                year = match.group(1)
                result['year'] = -int(year)
                result['confidence'] = 'medium'
                result['era'] = 'BC'
                result['display'] = f"{year} BC"
                
            elif pattern_type == 'year_ad':
                year = match.group(1)
                result['year'] = int(year)
                result['confidence'] = 'medium'
                result['display'] = f"{year}"
                
            elif pattern_type == 'date_range':
                start_day, month, year = match.groups()
                result['year'] = int(year)
                result['confidence'] = 'high'
                result['display'] = match.group(0)
                
            elif pattern_type == 'circa':
                year = match.group(1)
                is_bc = 'BC' in original.upper() or 'BCE' in original.upper()
                result['year'] = -int(year) if is_bc else int(year)
                result['confidence'] = 'low'
                result['era'] = 'BC' if is_bc else 'AD'
                result['display'] = f"c. {year} {'BC' if is_bc else ''}"
            
            # Calculate sort key (for chronological ordering)
            if result['year']:
                # Add 10000 to handle negative years
                result['sortKey'] = result['year'] + 10000
                
        except Exception as e:
            logger.warning(f"Error parsing date: {e}")
            
        return result
    
    def process_battle(self, battle_data: Dict, filename: str) -> Optional[Dict]:
        """Process a single battle's data."""
        # Extract battle name from filename
        battle_name = filename.replace('.json', '').replace('_structured', '')
        battle_name = battle_name.replace('_', ' ')
        
        # Try to get date from infobox
        date_str = None
        if 'infobox' in battle_data:
            date_str = battle_data['infobox'].get('date', '')
        
        # Parse the date
        date_info = self.extract_date(date_str) if date_str else None
        
        if not date_info:
            logger.warning(f"No date found for {battle_name}")
            return None
            
        return {
            'id': filename.replace('.json', ''),
            'name': battle_name,
            'date': date_info,
            'categories': battle_data.get('metadata', {}).get('categories', [])
        }


def main():
    """Process all battle data and create timeline dataset."""
    processor = BattleDateProcessor()
    battles = []
    
    # First, download a sample of battles for testing
    logger.info("Downloading sample battles for timeline...")
    
    from wikipedia_downloader import WikipediaBattleDownloader
    from wikipedia_to_json import WikipediaToJsonConverter
    
    downloader = WikipediaBattleDownloader(output_dir='battlethread/data/battles')
    converter = WikipediaToJsonConverter()
    
    # Get first 500 battles for MVP
    titles = []
    for title in downloader.get_all_page_titles():
        titles.append(title)
        if len(titles) >= 500:  # Start with 500 for testing
            break
    
    logger.info(f"Processing {len(titles)} battles...")
    
    # Download in batches
    batch_size = 50
    for i in range(0, len(titles), batch_size):
        batch = titles[i:i + batch_size]
        try:
            articles = downloader.download_articles_batch(batch)
            for title, content in articles.items():
                # Convert to structured JSON
                json_data = converter.convert_to_json(content, title, 'structured')
                
                # Process the battle data
                safe_title = title.replace('/', '_').replace(':', '_')
                battle_info = processor.process_battle(json_data, safe_title)
                
                if battle_info:
                    battles.append(battle_info)
                    logger.info(f"Processed: {title} - {battle_info['date']['display']}")
                    
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
    
    # Sort battles by date
    battles.sort(key=lambda b: b['date']['sortKey'])
    
    # Create indexed dataset
    dataset = {
        'battles': battles,
        'metadata': {
            'total': len(battles),
            'dateRange': {
                'earliest': battles[0]['date']['year'] if battles else None,
                'latest': battles[-1]['date']['year'] if battles else None
            },
            'generated': datetime.now().isoformat()
        }
    }
    
    # Save the dataset
    os.makedirs('battlethread/data', exist_ok=True)
    with open('battlethread/data/battles_timeline.json', 'w') as f:
        json.dump(dataset, f, indent=2)
    
    logger.info(f"Created timeline dataset with {len(battles)} battles")
    logger.info(f"Date range: {dataset['metadata']['dateRange']}")


if __name__ == "__main__":
    main()