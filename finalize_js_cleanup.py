#!/usr/bin/env python3
"""
Final JavaScript Cleanup - Replace all inline JS with external file
"""

import re
import os
import glob

def update_html_file(html_file, js_filename):
    """Update HTML file to use external JavaScript"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove all script blocks
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove multiple empty lines that might be left behind
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Add external script reference before closing body tag
        if '</body>' in content:
            # Check if script is already included
            if js_filename not in content:
                script_tag = f'    <script src="{js_filename}"></script>\n  </body>'
                content = content.replace('</body>', script_tag)
        
        # Only update if content changed
        if content != original_content:
            # Create backup
            backup_file = html_file + '.js_backup'
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write updated file
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Updated {html_file} (backup: {backup_file})")
        else:
            print(f"- No changes needed for {html_file}")
        
    except Exception as e:
        print(f"✗ Error updating {html_file}: {e}")

def minify_js_file(js_file):
    """Create minified version of JavaScript file"""
    try:
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Minify
        minified = content
        
        # Remove comments
        minified = re.sub(r'//[^\n]*', '', minified)
        minified = re.sub(r'/\*.*?\*/', '', minified, flags=re.DOTALL)
        
        # Remove unnecessary whitespace
        minified = re.sub(r'\s+', ' ', minified)
        minified = re.sub(r'\s*([{}();,:])\s*', r'\1', minified)
        minified = re.sub(r'\s*([=+\-*/!<>])\s*', r'\1', minified)
        
        # Clean up
        minified = minified.strip()
        
        # Save minified version
        minified_file = js_file.replace('.js', '.min.js')
        with open(minified_file, 'w', encoding='utf-8') as f:
            f.write(minified)
        
        original_size = len(content)
        minified_size = len(minified)
        reduction = ((original_size - minified_size) / original_size) * 100
        
        print(f"✓ Created {minified_file}")
        print(f"  Original: {original_size} bytes")
        print(f"  Minified: {minified_size} bytes ({reduction:.1f}% reduction)")
        
    except Exception as e:
        print(f"✗ Error minifying {js_file}: {e}")

def main():
    """Main function"""
    js_file = 'scripts_clean.js'
    
    if not os.path.exists(js_file):
        print(f"JavaScript file '{js_file}' not found!")
        return
    
    # Find all HTML files
    html_files = []
    for pattern in ["*.html", "projects/*.html", "articles/*.html"]:
        html_files.extend(glob.glob(pattern))
    
    print(f"Found {len(html_files)} HTML files to update")
    print(f"Using JavaScript file: {js_file}")
    
    response = input(f"\nUpdate all HTML files to use external JavaScript? (y/n): ")
    
    if response.lower() == 'y':
        print(f"\nUpdating HTML files...")
        
        for html_file in html_files:
            update_html_file(html_file, js_file)
        
        print(f"\nCreating minified JavaScript...")
        minify_js_file(js_file)
        
        print(f"\n=== JavaScript Cleanup Complete ===")
        print(f"✓ Updated {len(html_files)} HTML files")
        print(f"✓ Created clean external JavaScript file: {js_file}")
        print(f"✓ Created minified version for production")
        print(f"\nBenefits:")
        print(f"- Removed duplicate JavaScript code")
        print(f"- Faster page loading (cached external file)")
        print(f"- Easier maintenance (single JS file)")
        print(f"- Better organization and readability")
        
    else:
        print("Update cancelled.")

if __name__ == "__main__":
    main()
