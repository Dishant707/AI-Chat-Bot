"""Analyze website technology stack"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urlparse

def analyze_tech_stack(url):
    """Analyze the technology stack of a website."""
    
    print(f"🔍 Analyzing: {url}\n")
    
    results = {
        'url': url,
        'frontend': [],
        'backend': [],
        'analytics': [],
        'cdn': [],
        'hosting': [],
        'other': []
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Analyze HTML structure
        print("📄 HTML Analysis:")
        print("=" * 50)
        
        # Check meta tags
        meta_generator = soup.find('meta', attrs={'name': 'generator'})
        if meta_generator:
            results['frontend'].append(f"Generator: {meta_generator.get('content')}")
            print(f"✓ Generator: {meta_generator.get('content')}")
        
        # Check for frameworks
        print("\n🎨 Frontend Frameworks:")
        print("-" * 50)
        
        # React
        if soup.find(id=lambda x: x and ('react' in str(x).lower() or 'root' in str(x).lower())):
            results['frontend'].append('React (likely)')
            print("✓ React (detected root div)")
        
        # Vue
        if soup.find(attrs={'data-v-': True}) or soup.find(id='app'):
            results['frontend'].append('Vue.js (likely)')
            print("✓ Vue.js")
        
        # Next.js
        if soup.find(id='__next') or soup.find(id='__nuxt'):
            results['frontend'].append('Next.js/Nuxt.js')
            print("✓ Next.js/Nuxt.js")
        
        # Angular
        if soup.find(attrs={'ng-app': True}) or soup.find('app-root'):
            results['frontend'].append('Angular')
            print("✓ Angular")
        
        # Analyze scripts
        print("\n📦 JavaScript Libraries:")
        print("-" * 50)
        
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script.get('src', '')
            
            # Check for common libraries
            if 'react' in src.lower():
                results['frontend'].append('React')
                print(f"✓ React: {src[:80]}")
            elif 'vue' in src.lower():
                results['frontend'].append('Vue.js')
                print(f"✓ Vue.js: {src[:80]}")
            elif 'angular' in src.lower():
                results['frontend'].append('Angular')
                print(f"✓ Angular: {src[:80]}")
            elif 'jquery' in src.lower():
                results['frontend'].append('jQuery')
                print(f"✓ jQuery: {src[:80]}")
            elif 'bootstrap' in src.lower():
                results['frontend'].append('Bootstrap')
                print(f"✓ Bootstrap: {src[:80]}")
            elif 'tailwind' in src.lower():
                results['frontend'].append('Tailwind CSS')
                print(f"✓ Tailwind CSS: {src[:80]}")
            elif 'gtag' in src or 'google-analytics' in src or 'googletagmanager' in src:
                results['analytics'].append('Google Analytics')
                print(f"✓ Google Analytics: {src[:80]}")
            elif 'cdn' in src.lower():
                cdn_name = urlparse(src).netloc
                results['cdn'].append(cdn_name)
                print(f"✓ CDN: {cdn_name}")
        
        # Check for CSS frameworks
        print("\n🎨 CSS Frameworks:")
        print("-" * 50)
        
        stylesheets = soup.find_all('link', rel='stylesheet')
        for style in stylesheets:
            href = style.get('href', '')
            if 'bootstrap' in href.lower():
                results['frontend'].append('Bootstrap')
                print(f"✓ Bootstrap")
            elif 'tailwind' in href.lower():
                results['frontend'].append('Tailwind CSS')
                print(f"✓ Tailwind CSS")
            elif 'font' in href.lower():
                results['frontend'].append('Web Fonts')
                print(f"✓ Web Fonts: {href[:80]}")
        
        # Check headers for backend tech
        print("\n🔧 Backend/Server Info:")
        print("-" * 50)
        
        server = response.headers.get('Server', 'Not disclosed')
        results['backend'].append(f"Server: {server}")
        print(f"✓ Server: {server}")
        
        x_powered_by = response.headers.get('X-Powered-By', 'Not disclosed')
        if x_powered_by != 'Not disclosed':
            results['backend'].append(f"Powered by: {x_powered_by}")
            print(f"✓ Powered by: {x_powered_by}")
        
        # Check for specific technologies in HTML
        html_content = str(soup)
        
        print("\n🔍 Additional Technologies:")
        print("-" * 50)
        
        tech_patterns = {
            'WordPress': r'wp-content|wp-includes',
            'Shopify': r'cdn\.shopify\.com|Shopify\.theme',
            'Wix': r'wixsite\.com|wix\.com',
            'Squarespace': r'squarespace',
            'Webflow': r'webflow',
            'Vercel': r'vercel',
            'Netlify': r'netlify',
            'Firebase': r'firebase',
            'AWS': r'amazonaws\.com|cloudfront',
            'Cloudflare': r'cloudflare',
            'Stripe': r'stripe',
            'PayPal': r'paypal',
            'Intercom': r'intercom',
            'Hotjar': r'hotjar',
            'Segment': r'segment'
        }
        
        for tech, pattern in tech_patterns.items():
            if re.search(pattern, html_content, re.IGNORECASE):
                results['other'].append(tech)
                print(f"✓ {tech}")
        
        # Check for AI/ML indicators
        if 'ai' in url.lower() or 'machine learning' in html_content.lower() or 'artificial intelligence' in html_content.lower():
            results['other'].append('AI/ML Features')
            print(f"✓ AI/ML Features detected")
        
        # Clean up duplicates
        for key in results:
            if isinstance(results[key], list):
                results[key] = list(set(results[key]))
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python tech_analyzer.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    results = analyze_tech_stack(url)
    
    if results:
        print("\n" + "=" * 50)
        print("📊 SUMMARY")
        print("=" * 50)
        
        for category, items in results.items():
            if items and category != 'url':
                print(f"\n{category.upper()}:")
                for item in items:
                    print(f"  • {item}")
        
        # Save to file
        filename = f"tech_stack_{urlparse(url).netloc.replace('.', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {filename}")


if __name__ == "__main__":
    main()
