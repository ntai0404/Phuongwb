import sys
sys.path.insert(0, '/app/src')
from web_crawler import ArticleCrawler

urls = [
    'https://vnexpress.net/dau-tran-vong-play-off-aff-cup-4677152.html',
]

crawler = ArticleCrawler()
for url in urls:
    url_name = url.split('/')[-1]
    print(f'\nTesting: {url_name}')
    print('='*100)
    result = crawler.crawl_article(url)
    
    if result and result.get('success'):
        content = result.get('content', '')
        lines = content.split('\n')
        print(f'Got {len(lines)} lines, {len(content)} chars')
        print()
        
        # Show first 20 lines
        for i, line in enumerate(lines[:20]):
            if line.strip():
                preview = line[:95]
                print(f'{i+1:2}. {preview}')
        
        print()
        
        # Check for bad patterns
        js_check = ['(function', 'window.', 'arfasync', 'taboola', 'GMT', 'Indochina']
        found = [ind for ind in js_check if ind.lower() in content.lower()]
        if found:
            print(f'WARNING - Found patterns: {found}')
        else:
            print('SUCCESS - No bad patterns found!')
    else:
        print('FAILED - Crawl returned None')
