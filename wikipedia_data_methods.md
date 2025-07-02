# Common Ways to Obtain Wikipedia Data

This guide covers the various methods available for obtaining Wikipedia data, from small-scale queries to bulk downloads of the entire database.

## 1. MediaWiki API

The official API for accessing Wikipedia content programmatically.

### Advantages:
- Real-time data access
- Fine-grained control over queries
- No need to download large files
- Supports various output formats (JSON, XML)

### Disadvantages:
- Rate limited (90 requests/minute without bot flag)
- Not suitable for bulk downloads
- Requires multiple requests for large datasets

### Key Endpoints:
- **Query API**: `action=query` - Main endpoint for content retrieval
- **AllPages**: `list=allpages` - List pages by prefix or namespace
- **Search**: `list=search` - Full-text search
- **Revisions**: `prop=revisions` - Get page content and history

### Example Use Cases:
```python
# Get all pages starting with "Battle of"
https://en.wikipedia.org/w/api.php?action=query&list=allpages&apprefix=Battle%20of&format=json

# Get content of specific pages
https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Battle%20of%20Waterloo&rvprop=content&format=json
```

## 2. Wikipedia Database Dumps

Complete snapshots of Wikipedia databases in various formats.

### Types of Dumps:

#### a) Pages Articles (XML)
- **Location**: `https://dumps.wikimedia.org/enwiki/`
- **Format**: Compressed XML (`.xml.bz2`)
- **Contains**: All article content with revision history
- **Size**: ~20GB compressed, ~90GB uncompressed
- **Frequency**: Monthly

#### b) SQL Dumps
- **Format**: SQL files for direct database import
- **Tables**: page, revision, text, user, etc.
- **Use Case**: Setting up a local Wikipedia mirror

#### c) Abstract Dumps
- **Format**: XML with article summaries
- **Size**: Much smaller than full dumps
- **Use Case**: Quick overview of articles

### Download Example:
```bash
# Download latest articles dump
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

# Download specific date
wget https://dumps.wikimedia.org/enwiki/20240101/enwiki-20240101-pages-articles.xml.bz2
```

## 3. Wikimedia Enterprise

Commercial API service with enhanced features.

### Features:
- **Snapshot API**: NDJSON format dumps
- **Realtime API**: Stream of changes
- **On-demand API**: Individual article retrieval
- **Free Tier**: 5,000 monthly requests + bi-monthly snapshots

### Advantages:
- Structured JSON format
- Better performance
- No rate limits (paid tiers)
- Enterprise support

### Access:
- Sign up at: `https://enterprise.wikimedia.com/`
- Free tier available for non-commercial use

## 4. Third-Party Tools and Libraries

### Python Libraries:

#### wikipedia-api
```python
import wikipediaapi
wiki = wikipediaapi.Wikipedia('en')
page = wiki.page('Python (programming language)')
print(page.text)
```

#### pywikibot
```python
import pywikibot
site = pywikibot.Site('en', 'wikipedia')
page = pywikibot.Page(site, 'Battle of Waterloo')
print(page.text)
```

#### mwparserfromhell
```python
import mwparserfromhell
wikicode = mwparserfromhell.parse(wiki_text)
# Parse wiki markup to extract specific elements
```

### Other Languages:
- **Java**: WikiAPI, JWBF
- **JavaScript**: wiki.js, nodemw
- **R**: WikipediR, WikidataR
- **Ruby**: wikipedia-client

## 5. Alternative Data Sources

### Wikidata
- Structured data about Wikipedia entities
- SPARQL endpoint for queries
- JSON/RDF dumps available
- URL: `https://www.wikidata.org/`

### DBpedia
- Structured Wikipedia data as RDF
- SPARQL endpoint
- Pre-processed datasets
- URL: `https://www.dbpedia.org/`

### Kiwix
- Offline Wikipedia archives
- ZIM format for compression
- Includes media files
- URL: `https://www.kiwix.org/`

### HuggingFace Datasets
- Pre-processed Wikipedia datasets
- Machine learning ready formats
- Various languages and versions
- Example: `wikipedia` dataset on HuggingFace

## 6. Specialized Access Methods

### Wiki Replicas
- Read-only database replicas
- SQL access via Wikimedia Cloud
- Real-time data
- Requires Wikimedia developer account

### EventStreams
- Real-time feed of changes
- Server-Sent Events (SSE) format
- URL: `https://stream.wikimedia.org/`
- Use cases: Monitoring edits, vandalism detection

### Analytics Dumps
- Pageview statistics
- Edit history analytics
- User activity data
- URL: `https://dumps.wikimedia.org/other/`

## 7. Best Practices and Considerations

### Choosing the Right Method:

1. **Small datasets (<1000 pages)**: Use MediaWiki API
2. **Medium datasets (1000-50000 pages)**: Use API with batching or specialized dumps
3. **Large datasets (>50000 pages)**: Use database dumps
4. **Real-time needs**: Use EventStreams or Wikimedia Enterprise
5. **Structured data**: Use Wikidata or DBpedia

### Legal and Ethical Considerations:
- Wikipedia content is under CC BY-SA license
- Respect rate limits and server resources
- Include proper attribution
- Check robots.txt for scraping policies
- Use User-Agent headers with contact info

### Performance Tips:
- Cache API responses
- Use compression when downloading
- Process dumps in streaming fashion
- Consider using database indexes for large datasets
- Parallel processing for dump parsing

## 8. Example: Combining Methods

For comprehensive data collection, you might combine multiple methods:

```python
# 1. Use API for recent changes
recent_battles = get_recent_battles_via_api()

# 2. Use dumps for historical data
historical_battles = process_dump_for_battles()

# 3. Use Wikidata for structured metadata
battle_metadata = query_wikidata_for_battles()

# 4. Merge and deduplicate
all_battles = merge_data_sources(recent_battles, historical_battles, battle_metadata)
```

## Conclusion

The choice of method depends on your specific needs:
- **Volume**: How much data do you need?
- **Freshness**: Do you need real-time or historical data?
- **Format**: Do you need raw wiki markup or structured data?
- **Resources**: What are your computational and storage capabilities?
- **Budget**: Can you afford commercial services?

For downloading all "Battle of" articles specifically, the most suitable approaches are:
1. **API approach** (shown in `wikipedia_downloader.py`) for up-to-date data
2. **Dump processing** (shown in `wikipedia_dump_processor.py`) for comprehensive historical data
3. **Wikimedia Enterprise** for production use with better performance