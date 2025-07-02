#!/usr/bin/env python3
"""
Wikipedia to JSON Converter
Converts Wikipedia articles from wiki markup format to various JSON formats.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import os


class WikipediaToJsonConverter:
    """Convert Wikipedia wiki markup to JSON in various formats."""
    
    def __init__(self):
        self.infobox_pattern = re.compile(r'\{\{Infobox[^}]*\}\}', re.DOTALL)
        self.section_pattern = re.compile(r'^(=+)\s*(.+?)\s*\1\s*$', re.MULTILINE)
        self.link_pattern = re.compile(r'\[\[(?:[^|]+\|)?([^\]]+)\]\]')
        self.reference_pattern = re.compile(r'<ref[^>]*>.*?</ref>', re.DOTALL)
        self.template_pattern = re.compile(r'\{\{[^}]+\}\}')
        
    def extract_infobox_data(self, wiki_text: str) -> Dict[str, Any]:
        """Extract structured data from infoboxes."""
        infobox_match = self.infobox_pattern.search(wiki_text)
        if not infobox_match:
            return {}
            
        infobox_text = infobox_match.group(0)
        data = {}
        
        # Extract key-value pairs from infobox
        lines = infobox_text.split('\n')
        for line in lines:
            if '=' in line and '|' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lstrip('|').strip()
                    value = parts[1].strip()
                    # Clean up the value
                    value = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'\2', value)
                    value = re.sub(r'\[\[([^\]]+)\]\]', r'\1', value)
                    value = re.sub(r'\{\{[^}]+\}\}', '', value)
                    data[key] = value.strip()
        
        return data
    
    def extract_sections(self, wiki_text: str) -> List[Dict[str, str]]:
        """Extract sections and their content."""
        sections = []
        section_matches = list(self.section_pattern.finditer(wiki_text))
        
        for i, match in enumerate(section_matches):
            level = len(match.group(1))
            title = match.group(2)
            start_pos = match.end()
            
            # Find the end position (start of next section or end of text)
            if i < len(section_matches) - 1:
                end_pos = section_matches[i + 1].start()
            else:
                end_pos = len(wiki_text)
            
            content = wiki_text[start_pos:end_pos].strip()
            
            # Clean up content
            content = self.reference_pattern.sub('', content)
            content = self.link_pattern.sub(r'\1', content)
            content = re.sub(r"'''?", '', content)
            content = re.sub(r'\n\s*\n', '\n\n', content)
            
            sections.append({
                'title': title,
                'level': level,
                'content': content.strip()
            })
        
        return sections
    
    def extract_metadata(self, wiki_text: str) -> Dict[str, Any]:
        """Extract metadata from the article."""
        metadata = {}
        
        # Extract categories
        categories = re.findall(r'\[\[Category:([^\]]+)\]\]', wiki_text)
        metadata['categories'] = categories
        
        # Count references
        references = self.reference_pattern.findall(wiki_text)
        metadata['reference_count'] = len(references)
        
        # Extract external links
        external_links = re.findall(r'\[http[^\s\]]+', wiki_text)
        metadata['external_link_count'] = len(external_links)
        
        # Character and word count
        plain_text = self.wiki_to_plain_text(wiki_text)
        metadata['character_count'] = len(wiki_text)
        metadata['word_count'] = len(plain_text.split())
        
        return metadata
    
    def wiki_to_plain_text(self, wiki_text: str) -> str:
        """Convert wiki markup to plain text."""
        # Remove templates
        text = re.sub(r'\{\{[^}]+\}\}', '', wiki_text)
        
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
        
        # Remove headers markup
        text = re.sub(r'^=+\s*(.+?)\s*=+$', r'\1', text, flags=re.MULTILINE)
        
        # Remove tables
        text = re.sub(r'\{\|.*?\|\}', '', text, flags=re.DOTALL)
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def convert_to_json(self, wiki_text: str, title: str = "Unknown", 
                       format_type: str = "full") -> Dict[str, Any]:
        """
        Convert wiki markup to JSON.
        
        Args:
            wiki_text: The wiki markup text
            title: The article title
            format_type: Type of JSON format:
                - "full": Complete structured data
                - "simple": Just plain text and metadata
                - "structured": Sections and infobox only
                - "raw": Original wiki markup in JSON
        """
        if format_type == "raw":
            return {
                "title": title,
                "format": "wiki_markup",
                "content": wiki_text,
                "timestamp": datetime.now().isoformat()
            }
        
        elif format_type == "simple":
            return {
                "title": title,
                "format": "simple",
                "content": self.wiki_to_plain_text(wiki_text),
                "metadata": self.extract_metadata(wiki_text),
                "timestamp": datetime.now().isoformat()
            }
        
        elif format_type == "structured":
            return {
                "title": title,
                "format": "structured",
                "infobox": self.extract_infobox_data(wiki_text),
                "sections": self.extract_sections(wiki_text),
                "timestamp": datetime.now().isoformat()
            }
        
        else:  # full format
            return {
                "title": title,
                "format": "full",
                "infobox": self.extract_infobox_data(wiki_text),
                "sections": self.extract_sections(wiki_text),
                "plain_text": self.wiki_to_plain_text(wiki_text),
                "metadata": self.extract_metadata(wiki_text),
                "original_markup": wiki_text,
                "timestamp": datetime.now().isoformat()
            }
    
    def convert_file(self, input_path: str, output_path: str = None, 
                    format_type: str = "full"):
        """Convert a wiki file to JSON."""
        # Extract title from filename
        title = os.path.basename(input_path).replace('.wiki', '')
        
        # Read the wiki file
        with open(input_path, 'r', encoding='utf-8') as f:
            wiki_text = f.read()
        
        # Convert to JSON
        json_data = self.convert_to_json(wiki_text, title, format_type)
        
        # Determine output path
        if output_path is None:
            output_path = input_path.replace('.wiki', f'_{format_type}.json')
        
        # Save JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def batch_convert(self, input_dir: str, output_dir: str = None, 
                     format_type: str = "full"):
        """Convert all wiki files in a directory to JSON."""
        if output_dir is None:
            output_dir = f"{input_dir}_json"
        
        os.makedirs(output_dir, exist_ok=True)
        
        converted_files = []
        
        for filename in os.listdir(input_dir):
            if filename.endswith('.wiki'):
                input_path = os.path.join(input_dir, filename)
                output_filename = filename.replace('.wiki', f'_{format_type}.json')
                output_path = os.path.join(output_dir, output_filename)
                
                self.convert_file(input_path, output_path, format_type)
                converted_files.append(output_path)
                print(f"✓ Converted: {filename} -> {output_filename}")
        
        return converted_files


def main():
    """Example usage of the converter."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert Wikipedia wiki markup files to JSON"
    )
    parser.add_argument(
        'input',
        help='Input file or directory path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file or directory path'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['full', 'simple', 'structured', 'raw'],
        default='full',
        help='JSON format type (default: full)'
    )
    parser.add_argument(
        '-b', '--batch',
        action='store_true',
        help='Batch convert all .wiki files in directory'
    )
    
    args = parser.parse_args()
    
    converter = WikipediaToJsonConverter()
    
    if args.batch:
        converted = converter.batch_convert(args.input, args.output, args.format)
        print(f"\nConverted {len(converted)} files")
    else:
        output_path = converter.convert_file(args.input, args.output, args.format)
        print(f"Converted to: {output_path}")


if __name__ == "__main__":
    main()