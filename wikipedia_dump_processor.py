#!/usr/bin/env python3
"""
Wikipedia Dump Processor for Battle Articles
Processes Wikipedia XML dumps to extract articles starting with "Battle of".
More efficient for large-scale data extraction than API approach.
"""

import xml.etree.ElementTree as ET
import bz2
import os
import json
import logging
from typing import Iterator, Tuple, Optional
import re
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WikipediaDumpProcessor:
    """Process Wikipedia XML dumps to extract specific articles."""
    
    def __init__(self, prefix: str = "Battle of", output_dir: str = "wikipedia_battles_dump"):
        self.prefix = prefix
        self.output_dir = output_dir
        self.namespace = "{http://www.mediawiki.org/xml/export-0.10/}"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
    def parse_dump(self, dump_path: str) -> Iterator[Tuple[str, str]]:
        """
        Parse Wikipedia XML dump and yield (title, content) for matching articles.
        
        Args:
            dump_path: Path to the Wikipedia dump file (can be .xml or .xml.bz2)
            
        Yields:
            Tuple of (title, content) for articles matching the prefix
        """
        # Determine if file is compressed
        if dump_path.endswith('.bz2'):
            logger.info("Opening compressed dump file...")
            file_obj = bz2.BZ2File(dump_path, 'rb')
        else:
            logger.info("Opening uncompressed dump file...")
            file_obj = open(dump_path, 'rb')
            
        try:
            # Use iterative parsing for memory efficiency
            context = ET.iterparse(file_obj, events=('start', 'end'))
            context = iter(context)
            event, root = next(context)
            
            title = None
            text = None
            page_count = 0
            matched_count = 0
            
            for event, elem in context:
                if event == 'end' and elem.tag == f"{self.namespace}page":
                    page_count += 1
                    
                    # Extract title
                    title_elem = elem.find(f"{self.namespace}title")
                    if title_elem is not None and title_elem.text:
                        title = title_elem.text
                        
                        # Check if title matches our prefix
                        if title.startswith(self.prefix):
                            # Extract text content
                            revision = elem.find(f"{self.namespace}revision")
                            if revision is not None:
                                text_elem = revision.find(f"{self.namespace}text")
                                if text_elem is not None and text_elem.text:
                                    text = text_elem.text
                                    matched_count += 1
                                    
                                    if matched_count % 10 == 0:
                                        logger.info(f"Found {matched_count} matching articles...")
                                    
                                    yield title, text
                    
                    # Clear the element to save memory
                    elem.clear()
                    root.clear()
                    
                    if page_count % 10000 == 0:
                        logger.info(f"Processed {page_count} pages, found {matched_count} matches")
                        
        finally:
            file_obj.close()
            
        logger.info(f"Finished processing. Total pages: {page_count}, Matches: {matched_count}")
    
    def save_article(self, title: str, content: str):
        """Save an article to disk."""
        # Clean title for filename
        safe_title = title.replace('/', '_').replace(':', '_')
        filename = os.path.join(self.output_dir, f"{safe_title}.wiki")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def extract_plain_text(self, wiki_markup: str) -> str:
        """
        Convert wiki markup to plain text (basic conversion).
        
        Args:
            wiki_markup: Wikipedia markup text
            
        Returns:
            Plain text version
        """
        # Remove templates
        text = re.sub(r'\{\{[^}]+\}\}', '', wiki_markup)
        
        # Remove references
        text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
        text = re.sub(r'<ref[^>]*\/>', '', text)
        
        # Remove HTML comments
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        
        # Remove wiki links but keep text
        text = re.sub(r'\[\[(?:[^|]+\|)?([^\]]+)\]\]', r'\1', text)
        
        # Remove external links but keep text
        text = re.sub(r'\[http[^\s]+ ([^\]]+)\]', r'\1', text)
        
        # Remove formatting
        text = re.sub(r"'''?", '', text)
        
        # Remove headers
        text = re.sub(r'^=+.*?=+$', '', text, flags=re.MULTILINE)
        
        # Remove tables
        text = re.sub(r'\{\|.*?\|\}', '', text, flags=re.DOTALL)
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def process_dump(self, dump_path: str, save_plain_text: bool = False):
        """
        Process a Wikipedia dump file and extract matching articles.
        
        Args:
            dump_path: Path to the dump file
            save_plain_text: If True, also save plain text versions
        """
        logger.info(f"Processing dump: {dump_path}")
        start_time = datetime.now()
        
        metadata = {
            'dump_file': os.path.basename(dump_path),
            'prefix': self.prefix,
            'process_date': start_time.isoformat(),
            'articles': []
        }
        
        for title, content in self.parse_dump(dump_path):
            # Save wiki markup
            self.save_article(title, content)
            
            # Optionally save plain text
            if save_plain_text:
                plain_text = self.extract_plain_text(content)
                safe_title = title.replace('/', '_').replace(':', '_')
                plain_filename = os.path.join(self.output_dir, f"{safe_title}.txt")
                with open(plain_filename, 'w', encoding='utf-8') as f:
                    f.write(plain_text)
            
            metadata['articles'].append({
                'title': title,
                'size': len(content)
            })
        
        # Save metadata
        metadata['total_articles'] = len(metadata['articles'])
        metadata['process_time'] = (datetime.now() - start_time).total_seconds()
        
        with open(os.path.join(self.output_dir, 'dump_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Processing complete. Extracted {len(metadata['articles'])} articles")
        logger.info(f"Time elapsed: {metadata['process_time']:.2f} seconds")


def download_dump_file(date: str = "latest") -> str:
    """
    Download Wikipedia dump file (stub implementation).
    In practice, you would implement wget/curl download here.
    
    Args:
        date: Date string (YYYYMMDD) or "latest"
        
    Returns:
        Path to downloaded file
    """
    # Example URL format:
    # https://dumps.wikimedia.org/enwiki/20240101/enwiki-20240101-pages-articles.xml.bz2
    
    if date == "latest":
        # In practice, you'd need to check the latest available dump
        logger.info("Would download latest dump from dumps.wikimedia.org")
    else:
        logger.info(f"Would download dump from date: {date}")
    
    # Placeholder - in practice, implement actual download
    return "enwiki-pages-articles.xml.bz2"


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Process Wikipedia dumps to extract Battle articles"
    )
    parser.add_argument(
        '--dump-file',
        help='Path to Wikipedia dump file (XML or XML.bz2)'
    )
    parser.add_argument(
        '--prefix',
        default='Battle of',
        help='Article prefix to match (default: "Battle of")'
    )
    parser.add_argument(
        '--plain-text',
        action='store_true',
        help='Also save plain text versions of articles'
    )
    parser.add_argument(
        '--output-dir',
        default='wikipedia_battles_dump',
        help='Output directory for extracted articles'
    )
    
    args = parser.parse_args()
    
    processor = WikipediaDumpProcessor(
        prefix=args.prefix,
        output_dir=args.output_dir
    )
    
    if args.dump_file:
        processor.process_dump(args.dump_file, save_plain_text=args.plain_text)
    else:
        logger.info("No dump file specified. Use --dump-file to specify a Wikipedia dump.")
        logger.info("\nTo download a dump, visit:")
        logger.info("https://dumps.wikimedia.org/enwiki/")
        logger.info("\nExample command:")
        logger.info("wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2")


if __name__ == "__main__":
    main()