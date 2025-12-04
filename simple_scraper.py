"""Simple web scraper using BeautifulSoup and Requests"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import json
import os
from datetime import datetime


def scrape_webpage(url):
    """Scrape a single webpage and extract text content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get title
        title = soup.find('title')
        title = title.get_text() if title else url
        
        # Get main content
        main_content = soup.find('main') or soup.find('article') or soup.body
        
        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = '\n'.join(lines)
        
        return {
            'url': url,
            'title': title,
            'content': text,
            'length': len(text),
            'timestamp': datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None


def get_links(url, base_url):
    """Get all internal links from a webpage."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include links from the same domain
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                # Remove fragments
                full_url = full_url.split('#')[0]
                links.add(full_url)
        
        return links
    except Exception as e:
        print(f"Error getting links from {url}: {str(e)}")
        return set()


def scrape_website(start_url, max_pages=10, max_depth=2):
    """Scrape multiple pages from a website."""
    visited = set()
    to_visit = [(start_url, 0)]
    results = []
    
    print(f"🕷️  Starting to scrape: {start_url}")
    print(f"   Max pages: {max_pages}, Max depth: {max_depth}\n")
    
    while to_visit and len(visited) < max_pages:
        url, depth = to_visit.pop(0)
        
        if url in visited or depth > max_depth:
            continue
        
        print(f"📄 Scraping [{len(visited)+1}/{max_pages}]: {url}")
        
        # Scrape the page
        data = scrape_webpage(url)
        if data:
            results.append(data)
            visited.add(url)
            
            # Get links if we haven't reached max depth
            if depth < max_depth:
                new_links = get_links(url, start_url)
                for link in new_links:
                    if link not in visited:
                        to_visit.append((link, depth + 1))
    
    print(f"\n✅ Scraped {len(results)} pages successfully!")
    return results


def save_results(results, output_format='json'):
    """Save scraped results to file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if output_format == 'json':
        filename = f'scraped_data_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    elif output_format == 'txt':
        filename = f'scraped_data_{timestamp}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(f"URL: {result['url']}\n")
                f.write(f"Title: {result['title']}\n")
                f.write(f"{'='*80}\n")
                f.write(result['content'])
                f.write(f"\n\n{'='*80}\n\n")
    
    elif output_format == 'markdown':
        filename = f'scraped_data_{timestamp}.md'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Scraped Documentation\n\n")
            f.write(f"**Scraped at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total pages:** {len(results)}\n\n")
            f.write("---\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"## {i}. {result['title']}\n\n")
                f.write(f"**URL:** {result['url']}\n\n")
                f.write(result['content'])
                f.write(f"\n\n---\n\n")
    
    print(f"💾 Saved results to: {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(
        description='Simple web scraper using BeautifulSoup'
    )
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument(
        '--max-pages', 
        type=int, 
        default=10, 
        help='Maximum number of pages to scrape (default: 10)'
    )
    parser.add_argument(
        '--max-depth', 
        type=int, 
        default=2, 
        help='Maximum crawl depth (default: 2)'
    )
    parser.add_argument(
        '--format', 
        choices=['json', 'txt', 'markdown'], 
        default='markdown',
        help='Output format (default: markdown)'
    )
    parser.add_argument(
        '--single',
        action='store_true',
        help='Scrape only the single URL (no following links)'
    )
    
    args = parser.parse_args()
    
    if args.single:
        # Scrape single page
        print(f"🕷️  Scraping single page: {args.url}\n")
        result = scrape_webpage(args.url)
        if result:
            results = [result]
            save_results(results, args.format)
        else:
            print("❌ Failed to scrape the page")
    else:
        # Scrape multiple pages
        results = scrape_website(
            args.url, 
            max_pages=args.max_pages,
            max_depth=args.max_depth
        )
        
        if results:
            save_results(results, args.format)
        else:
            print("❌ No pages were scraped successfully")


if __name__ == "__main__":
    main()
