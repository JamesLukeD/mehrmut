#!/usr/bin/env python3
"""
Script to update HTML files to use external JavaScript
Run this script to replace inline JavaScript with external file reference
"""

import re
import os

def update_html_file(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove existing script blocks
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        
        # Add external script reference before closing body tag
        if '</body>' in content:
            script_tag = f'    <script src="scripts.js"></script>\n  </body>'
            content = content.replace('</body>', script_tag)
        
        # Create backup
        backup_file = html_file + '.backup'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(open(html_file, 'r').read())
        
        # Write updated file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {html_file} (backup: {backup_file})")
        
    except Exception as e:
        print(f"Error updating {html_file}: {e}")

def main():
    html_files = ['articles.html', 'contact.html', 'fairbuy.html', 'index.html', 'projects/Patenschaften.html', 'projects/projekte.html', 'projects/Gesundheit.html', 'projects/fair-work.html', 'projects/Infrastrukturprojekte.html', 'projects/abagore.html', 'projects/Bildungsprojekte.html', 'articles/articles.html', 'articles/articles-page-2.html']
    
    response = input(f"Update {len(html_files)} HTML files to use external JavaScript? (y/n): ")
    if response.lower() == 'y':
        for html_file in html_files:
            update_html_file(html_file)
        print("HTML files updated successfully!")
    else:
        print("HTML update cancelled.")

if __name__ == "__main__":
    main()
