# BattleThread

A minimalist, high-performance timeline visualization of historical battles from Wikipedia, spanning from 3000 BC to modern times.

![BattleThread Timeline](https://github.com/user-attachments/screenshot.png)

## Overview

BattleThread is a web application that presents 25,000+ Wikipedia battle articles in an elegant, scrollable vertical timeline. The project combines Wikipedia data processing capabilities with a performant frontend that uses virtual scrolling to handle massive datasets smoothly.

## Features

### 🚀 Core Features
- **Virtual Scrolling**: Smoothly browse through thousands of battles without performance degradation
- **Minimalist Design**: Clean, focused interface with battles on the left, leaving space for future enhancements
- **Smart Date Parsing**: Handles various date formats from Wikipedia (BC/AD, approximate dates, date ranges)
- **Search Functionality**: Quickly filter battles by name or date
- **Century Grouping**: Battles organized by century for easy navigation
- **Minimap Navigation**: Visual overview and quick navigation through the entire timeline

### 📊 Data Processing
- **Wikipedia Integration**: Tools to download and process Wikipedia battle articles
- **JSON Conversion**: Convert wiki markup to structured JSON in multiple formats
- **Batch Processing**: Handle thousands of articles efficiently
- **Date Normalization**: Intelligent parsing of historical dates

## Project Structure

```
battlethread/
├── index.html              # Main application HTML
├── styles/
│   └── timeline.css        # Minimalist styling
├── js/
│   ├── timeline.js         # Main application logic
│   └── virtual-scroll.js   # Virtual scrolling implementation
├── data/
│   └── battles_timeline.json  # Processed battle data
├── server.py               # Python web server
├── create_sample_data.py   # Generate sample battle data
├── wikipedia_downloader.py # Download Wikipedia articles via API
├── wikipedia_dump_processor.py # Process Wikipedia XML dumps
├── wikipedia_to_json.py    # Convert wiki markup to JSON
└── requirements.txt        # Python dependencies
```

## Quick Start

### Running the Timeline

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Sample Data** (if not already present):
   ```bash
   python create_sample_data.py
   ```

3. **Start the Server**:
   ```bash
   python server.py
   ```

4. **Access the Application**:
   - Local: http://localhost:8080
   - The server will display a public URL when accessed

### Processing Wikipedia Data

#### Option 1: Download via API (Current Data)
```bash
# Download all battle articles
python wikipedia_downloader.py

# Or download as JSON
python wikipedia_downloader.py --format json --json-format structured
```

#### Option 2: Process Wikipedia Dumps (Bulk Data)
```bash
# Download a Wikipedia dump first
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

# Process the dump
python wikipedia_dump_processor.py --dump-file enwiki-latest-pages-articles.xml.bz2
```

#### Convert Wiki to JSON
```bash
# Convert a single file
python wikipedia_to_json.py "Battle of Waterloo.wiki" -f structured

# Batch convert directory
python wikipedia_to_json.py battles_directory/ -b -f full
```

## JSON Output Formats

The Wikipedia to JSON converter supports four formats:

1. **raw**: Original wiki markup wrapped in JSON
2. **simple**: Plain text with metadata (word count, categories)
3. **structured**: Parsed sections and infobox data
4. **full**: Complete data including all above formats

## Architecture

### Frontend
- **Virtual Scrolling**: Only renders visible items for optimal performance
- **Variable Height Support**: Handles different item types (battles vs century markers)
- **Cache-busting**: Prevents browser caching issues during development

### Backend
- **Rate-limited API Access**: Respects Wikipedia's 90 requests/minute limit
- **Efficient Data Processing**: Streaming XML parser for large dumps
- **Flexible Data Pipeline**: Multiple input/output format options

## Development

### Adding New Features
The application is designed for extensibility:
- Right panel is reserved for battle details, maps, and descriptions
- Data structure supports additional metadata
- Modular JavaScript architecture

### Performance Considerations
- Virtual scrolling handles 25,000+ items smoothly
- Minimal DOM manipulation
- Efficient data structures with pre-calculated positions

## Data Statistics

- **Total Wikipedia Battle Articles**: ~25,411
- **Date Range**: 3000 BC to present
- **Data Processing**: 
  - API: ~6-7 hours for full dataset
  - Dump: ~30 min download + 5 min processing

## Requirements

- Python 3.6+
- Modern web browser
- ~1GB disk space for full dataset

## License

This project processes Wikipedia content, which is available under the Creative Commons Attribution-ShareAlike License. 

## Acknowledgments

- Wikipedia contributors for the comprehensive battle documentation
- Virtual scrolling implementation inspired by modern web best practices

## Future Enhancements

- [ ] Interactive maps showing battle locations
- [ ] Detailed battle information panel
- [ ] Battle outcome visualization
- [ ] Participant country/empire filtering
- [ ] Statistical analysis dashboard
- [ ] Mobile responsive design