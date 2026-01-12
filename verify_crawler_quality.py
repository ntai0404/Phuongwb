#!/usr/bin/env python3
"""Verify crawler quality - check for ads, content completeness"""

import sys
import os

# Mock environment for psycopg2
os.environ['PGHOST'] = 'localhost'
os.environ['PGPORT'] = '5432'
os.environ['PGDATABASE'] = 'newsdb'
os.environ['PGUSER'] = 'postgres'
os.environ['PGPASSWORD'] = 'postgres'

print("=" * 100)
print("CRAWLER QUALITY VERIFICATION")
print("=" * 100)

# Use docker to query
import subprocess

def run_query(query):
    cmd = [
        'docker', 'exec', 'phuong-postgres',
        'psql', '-U', 'postgres', '-d', 'newsdb',
        '-c', query, '-t'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

# 1. Check newest article
print("\n1. CHECKING NEWEST ARTICLE (after universal crawler deployment)")
print("-" * 100)

newest = run_query("""
    SELECT id, title, fetched_at, LENGTH(content) as len
    FROM articles 
    WHERE content IS NOT NULL AND content != ''
    ORDER BY fetched_at DESC LIMIT 1
""")
print(newest)

# 2. Count HTML elements
print("\n2. HTML ELEMENT COUNT")
print("-" * 100)

elements = run_query("""
    SELECT 
        (LENGTH(content) - LENGTH(REPLACE(content, '<p>', ''))) / 3 as paragraphs,
        (LENGTH(content) - LENGTH(REPLACE(content, '<img', ''))) / 4 as images,
        (LENGTH(content) - LENGTH(REPLACE(content, '<video', ''))) / 6 as videos,
        (LENGTH(content) - LENGTH(REPLACE(content, '<iframe', ''))) / 7 as iframes
    FROM articles 
    WHERE content IS NOT NULL 
    ORDER BY fetched_at DESC LIMIT 1
""")
print(f"Paragraphs | Images | Videos | Iframes")
print(elements)

# 3. Check for JavaScript/ads leakage
print("\n3. CHECKING FOR ADS/JAVASCRIPT CODE LEAKAGE")
print("-" * 100)

js_check = run_query("""
    SELECT 
        SUM(CASE WHEN content LIKE '%runinit%' THEN 1 ELSE 0 END) as runinit_count,
        SUM(CASE WHEN content LIKE '%taboola%' THEN 1 ELSE 0 END) as taboola_count,
        SUM(CASE WHEN content LIKE '%mutexAds%' THEN 1 ELSE 0 END) as mutexads_count,
        SUM(CASE WHEN content LIKE '%window.%' THEN 1 ELSE 0 END) as window_count,
        SUM(CASE WHEN content LIKE '%function()%' OR content LIKE '%function ()%' THEN 1 ELSE 0 END) as function_count
    FROM articles 
    WHERE fetched_at > NOW() - INTERVAL '2 hours'
""")
print("runinit | taboola | mutexAds | window. | function()")
print(js_check)

# 4. Content length distribution
print("\n4. CONTENT LENGTH DISTRIBUTION (last 10 articles)")
print("-" * 100)

lengths = run_query("""
    SELECT 
        CASE 
            WHEN LENGTH(content) < 200 THEN 'Too Short (<200)'
            WHEN LENGTH(content) < 1000 THEN 'Short (200-1000)'
            WHEN LENGTH(content) < 3000 THEN 'Medium (1000-3000)'
            ELSE 'Good (>3000)'
        END as category,
        COUNT(*) as count
    FROM articles 
    WHERE content IS NOT NULL
    AND fetched_at > NOW() - INTERVAL '2 hours'
    GROUP BY 1
    ORDER BY 1
""")
print(lengths)

# 5. Sample content preview
print("\n5. SAMPLE CONTENT PREVIEW (newest article, first 500 chars)")
print("-" * 100)

preview = run_query("""
    SELECT LEFT(content, 500)
    FROM articles 
    WHERE content IS NOT NULL
    ORDER BY fetched_at DESC LIMIT 1
""")
print(preview)

print("\n" + "=" * 100)
print("SUMMARY:")
print("✓ Check paragraphs count - should be > 5 for full articles")
print("✓ Check images count - should have at least 1-2 images")
print("✓ Check ads leakage - all counts should be 0")
print("✓ Check content length - most should be 'Good (>3000)' or 'Medium'")
print("=" * 100)
