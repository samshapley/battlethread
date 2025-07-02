#!/usr/bin/env python3
"""
Demonstration of Wikipedia to JSON conversion with different format options.
"""

import json
from wikipedia_downloader import WikipediaBattleDownloader
from wikipedia_to_json import WikipediaToJsonConverter


def demo_json_conversion():
    """Demonstrate different JSON conversion formats."""
    print("=== Wikipedia to JSON Conversion Demo ===\n")
    
    # Download a sample article
    downloader = WikipediaBattleDownloader(output_dir='demo_battles')
    converter = WikipediaToJsonConverter()
    
    # Get a smaller battle article for demonstration
    sample_title = 'Battle of Marathon'
    
    print(f"1. Downloading '{sample_title}' article...")
    try:
        articles = downloader.download_articles_batch([sample_title])
        if sample_title in articles:
            wiki_text = articles[sample_title]
            downloader.save_article(sample_title, wiki_text)
            print(f"   ✓ Downloaded ({len(wiki_text):,} characters)\n")
        else:
            print("   ✗ Failed to download article\n")
            return
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
        return
    
    # Show different JSON formats
    formats = ['raw', 'simple', 'structured', 'full']
    
    for format_type in formats:
        print(f"2. Converting to '{format_type}' JSON format...")
        
        json_data = converter.convert_to_json(wiki_text, sample_title, format_type)
        
        # Save to file
        output_file = f'demo_battles/{sample_title}_{format_type}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Show preview based on format type
        print(f"   Preview of '{format_type}' format:")
        print("   " + "-" * 50)
        
        if format_type == 'raw':
            print(f"   - Title: {json_data['title']}")
            print(f"   - Format: {json_data['format']}")
            print(f"   - Content length: {len(json_data['content'])} characters")
            print(f"   - First 200 chars: {json_data['content'][:200]}...")
            
        elif format_type == 'simple':
            print(f"   - Title: {json_data['title']}")
            print(f"   - Plain text length: {len(json_data['content'])} characters")
            print(f"   - Word count: {json_data['metadata']['word_count']}")
            print(f"   - Categories: {len(json_data['metadata']['categories'])}")
            print(f"   - References: {json_data['metadata']['reference_count']}")
            print(f"   - First 200 chars of text: {json_data['content'][:200]}...")
            
        elif format_type == 'structured':
            print(f"   - Title: {json_data['title']}")
            print(f"   - Infobox fields: {len(json_data['infobox'])}")
            if json_data['infobox']:
                print("   - Sample infobox data:")
                for key, value in list(json_data['infobox'].items())[:3]:
                    print(f"     • {key}: {value[:50]}..." if len(value) > 50 else f"     • {key}: {value}")
            print(f"   - Sections: {len(json_data['sections'])}")
            if json_data['sections']:
                print("   - Section titles:")
                for section in json_data['sections'][:5]:
                    print(f"     • {section['title']} (level {section['level']})")
                    
        else:  # full format
            print(f"   - Title: {json_data['title']}")
            print(f"   - Has infobox: {'Yes' if json_data['infobox'] else 'No'}")
            print(f"   - Sections: {len(json_data['sections'])}")
            print(f"   - Plain text length: {len(json_data['plain_text'])} chars")
            print(f"   - Original markup length: {len(json_data['original_markup'])} chars")
            print(f"   - Categories: {json_data['metadata']['categories'][:3]}...")
            
        print(f"   - Saved to: {output_file}")
        print()
    
    # Show file sizes comparison
    print("3. JSON File Sizes Comparison:")
    print("   " + "-" * 50)
    import os
    for format_type in formats:
        filename = f'demo_battles/{sample_title}_{format_type}.json'
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   - {format_type:12s} format: {size:,} bytes")
    
    print("\n4. Sample JSON Structure (structured format):")
    print("   " + "-" * 50)
    # Show a prettified sample of the structured format
    structured_sample = {
        "title": json_data['title'],
        "format": "structured",
        "infobox": dict(list(json_data['infobox'].items())[:2]) if format_type == 'structured' else "...",
        "sections": [
            {
                "title": s['title'],
                "level": s['level'],
                "content": s['content'][:100] + "..."
            } for s in json_data['sections'][:2]
        ] if format_type == 'structured' else "...",
        "timestamp": json_data['timestamp']
    }
    print(json.dumps(structured_sample, indent=4))


if __name__ == "__main__":
    demo_json_conversion()