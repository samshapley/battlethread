#!/usr/bin/env python3
"""
Wikipedia "Battle of" Articles Downloader
Downloads all Wikipedia articles that start with "Battle of" using the Wikipedia API.
Implements proper rate limiting and error handling.
"""

import json
import time
import os
from datetime import datetime
import requests
from typing import List, Dict, Generator
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WikipediaBattleDownloader:
    """Downloads Wikipedia articles starting with a specific prefix."""
    
    def __init__(self, prefix: str = "Battle of", output_dir: str = "wikipedia_battles", output_format: str = "wiki"):
        self.prefix = prefix
        self.output_dir = output_dir
        self.output_format = output_format.lower()  # 'wiki' or 'json'
        self.base_url = "https://en.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WikipediaBattleDownloader/1.0 (your-email@example.com)'
        })
        
        # Rate limiting settings
        self.requests_per_minute = 85  # Stay under 90/min limit
        self.last_request_time = 0
        self.min_request_interval = 60.0 / self.requests_per_minute
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize JSON converter if needed
        if self.output_format == 'json':
            from wikipedia_to_json import WikipediaToJsonConverter
            self.json_converter = WikipediaToJsonConverter()
        
    def _rate_limit(self):
        """Implement rate limiting to avoid hitting API limits."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()
    
    def _make_request(self, params: Dict) -> Dict:
        """Make an API request with error handling and retries."""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                self._rate_limit()
                response = self.session.get(self.base_url, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
                    
    def get_all_page_titles(self) -> Generator[str, None, None]:
        """Get all page titles starting with the specified prefix."""
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'allpages',
            'apprefix': self.prefix,
            'aplimit': 500  # Maximum allowed
        }
        
        total_count = 0
        
        while True:
            logger.info(f"Fetching page titles... (found {total_count} so far)")
            data = self._make_request(params)
            
            pages = data.get('query', {}).get('allpages', [])
            for page in pages:
                yield page['title']
                total_count += 1
            
            # Check for continuation
            if 'continue' in data:
                params['apcontinue'] = data['continue']['apcontinue']
            else:
                logger.info(f"Finished fetching titles. Total found: {total_count}")
                break
    
    def download_articles_batch(self, titles: List[str]) -> Dict[str, str]:
        """Download a batch of articles (max 50 at a time)."""
        if len(titles) > 50:
            raise ValueError("Cannot download more than 50 articles at once")
            
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'revisions',
            'titles': '|'.join(titles),
            'rvprop': 'content',
            'rvslots': 'main'
        }
        
        data = self._make_request(params)
        articles = {}
        
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'revisions' in page_data:
                title = page_data['title']
                content = page_data['revisions'][0]['slots']['main']['*']
                articles[title] = content
                
        return articles
    
    def save_article(self, title: str, content: str, json_format: str = "full"):
        """Save an article to disk in the specified format."""
        # Clean title for filename
        safe_title = title.replace('/', '_').replace(':', '_')
        
        if self.output_format == 'json':
            # Convert to JSON
            json_data = self.json_converter.convert_to_json(content, title, json_format)
            filename = os.path.join(self.output_dir, f"{safe_title}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
        else:
            # Save as wiki markup (default)
            filename = os.path.join(self.output_dir, f"{safe_title}.wiki")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
        logger.debug(f"Saved: {title} -> {filename}")
    
    def download_all_battles(self, json_format: str = "full"):
        """Main method to download all battle articles."""
        logger.info(f"Starting download of all '{self.prefix}' articles...")
        logger.info(f"Output format: {self.output_format}")
        start_time = time.time()
        
        # Collect all titles
        all_titles = list(self.get_all_page_titles())
        logger.info(f"Found {len(all_titles)} articles to download")
        
        # Download in batches
        batch_size = 50
        downloaded_count = 0
        failed_titles = []
        
        for i in range(0, len(all_titles), batch_size):
            batch = all_titles[i:i + batch_size]
            logger.info(f"Downloading batch {i//batch_size + 1}/{(len(all_titles) + batch_size - 1)//batch_size}")
            
            try:
                articles = self.download_articles_batch(batch)
                
                for title, content in articles.items():
                    self.save_article(title, content, json_format)
                    downloaded_count += 1
                    
            except Exception as e:
                logger.error(f"Failed to download batch: {e}")
                failed_titles.extend(batch)
        
        # Summary
        elapsed_time = time.time() - start_time
        logger.info(f"\nDownload complete!")
        logger.info(f"Total articles found: {len(all_titles)}")
        logger.info(f"Successfully downloaded: {downloaded_count}")
        logger.info(f"Failed: {len(failed_titles)}")
        logger.info(f"Time elapsed: {elapsed_time:.2f} seconds")
        
        if failed_titles:
            logger.info(f"\nFailed titles:")
            for title in failed_titles[:10]:  # Show first 10
                logger.info(f"  - {title}")
            if len(failed_titles) > 10:
                logger.info(f"  ... and {len(failed_titles) - 10} more")
                
        # Save metadata
        metadata = {
            'download_date': datetime.now().isoformat(),
            'prefix': self.prefix,
            'total_articles': len(all_titles),
            'downloaded': downloaded_count,
            'failed': len(failed_titles),
            'failed_titles': failed_titles,
            'output_format': self.output_format
        }
        
        with open(os.path.join(self.output_dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Download Wikipedia articles with a specific prefix"
    )
    parser.add_argument(
        '--prefix',
        default='Battle of',
        help='Article prefix to download (default: "Battle of")'
    )
    parser.add_argument(
        '--output-dir',
        default='wikipedia_battles',
        help='Output directory for articles'
    )
    parser.add_argument(
        '--format',
        choices=['wiki', 'json'],
        default='wiki',
        help='Output format (default: wiki)'
    )
    parser.add_argument(
        '--json-format',
        choices=['full', 'simple', 'structured', 'raw'],
        default='full',
        help='JSON format type if --format=json (default: full)'
    )
    
    args = parser.parse_args()
    
    downloader = WikipediaBattleDownloader(
        prefix=args.prefix,
        output_dir=args.output_dir,
        output_format=args.format
    )
    
    try:
        downloader.download_all_battles(json_format=args.json_format)
    except KeyboardInterrupt:
        logger.info("\nDownload interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()