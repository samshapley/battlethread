#!/usr/bin/env python3
"""
Example usage of Wikipedia Battle downloaders.
Shows how to use both API and dump processing approaches.
"""

from wikipedia_downloader import WikipediaBattleDownloader
from wikipedia_dump_processor import WikipediaDumpProcessor


def example_api_download():
    """Example: Download 'Battle of' articles using the API."""
    print("=== API Download Example ===\n")
    
    # Create downloader instance
    downloader = WikipediaBattleDownloader(
        prefix="Battle of",
        output_dir="battles_from_api"
    )
    
    # Option 1: Download all battles (this will take time due to rate limiting)
    # downloader.download_all_battles()
    
    # Option 2: Download just a few for demonstration
    print("Fetching first 10 battle titles...")
    titles = []
    for title in downloader.get_all_page_titles():
        titles.append(title)
        if len(titles) >= 10:
            break
    
    print(f"Found titles: {titles[:5]}...")  # Show first 5
    
    # Download the first batch
    print("\nDownloading first 5 articles...")
    articles = downloader.download_articles_batch(titles[:5])
    
    for title, content in articles.items():
        downloader.save_article(title, content)
        print(f"✓ Saved: {title} ({len(content)} characters)")
    
    print("\nAPI download example complete!")


def example_dump_processing():
    """Example: Process a Wikipedia dump file."""
    print("\n=== Dump Processing Example ===\n")
    
    # Create processor instance
    processor = WikipediaDumpProcessor(
        prefix="Battle of",
        output_dir="battles_from_dump"
    )
    
    # Note: You need to download a dump file first
    dump_file = "enwiki-latest-pages-articles.xml.bz2"
    
    print("To use dump processing:")
    print("1. Download a Wikipedia dump:")
    print("   wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles1.xml.bz2")
    print("   (Note: This is a smaller partial dump ~250MB)")
    print("\n2. Run the processor:")
    print(f"   processor.process_dump('{dump_file}', save_plain_text=True)")
    
    # Simulate processing a few articles from a dump
    print("\nSimulated dump processing output:")
    sample_battles = [
        ("Battle of Hastings", "The '''Battle of Hastings''' was fought on 14 October 1066..."),
        ("Battle of Waterloo", "The '''Battle of Waterloo''' was fought on Sunday, 18 June 1815..."),
        ("Battle of Gettysburg", "The '''Battle of Gettysburg''' was fought July 1–3, 1863...")
    ]
    
    for title, content_snippet in sample_battles:
        print(f"✓ Would extract: {title}")


def compare_methods():
    """Compare different methods for obtaining Wikipedia data."""
    print("\n=== Method Comparison ===\n")
    
    comparison = """
    | Method | Best For | Speed | Rate Limits | Storage |
    |--------|----------|-------|-------------|---------|
    | API | Small datasets (<1000) | Slow | 90/min | Minimal |
    | Dumps | Large datasets (>10k) | Fast* | None | Large |
    | Enterprise | Production use | Fast | None† | Minimal |
    
    * Fast processing, but initial download is slow
    † Paid tiers have no limits
    
    For "Battle of" articles (~5000-10000 articles):
    - API approach: ~2-3 hours (with rate limiting)
    - Dump approach: ~30 min download + 5 min processing
    - Enterprise: ~5 minutes (with paid access)
    """
    
    print(comparison)


def main():
    """Run examples."""
    print("Wikipedia 'Battle of' Articles Download Examples\n")
    
    # Show API example
    example_api_download()
    
    # Show dump processing example
    example_dump_processing()
    
    # Show comparison
    compare_methods()
    
    print("\n=== Quick Start ===")
    print("\nTo download all Battle articles using the API:")
    print("  python wikipedia_downloader.py")
    print("\nTo process a dump file:")
    print("  python wikipedia_dump_processor.py --dump-file enwiki-latest-pages-articles.xml.bz2")
    print("\nCheck the generated documentation (wikipedia_data_methods.md) for more options!")


if __name__ == "__main__":
    main()