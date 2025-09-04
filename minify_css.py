#!/usr/bin/env python3
"""
CSS Minifier - Creates a minified version for production
"""

import re
import os

def minify_css(css_content):
    """Minify CSS by removing unnecessary whitespace and comments"""
    
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Remove unnecessary whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    
    # Remove whitespace around specific characters
    css_content = re.sub(r'\s*{\s*', '{', css_content)
    css_content = re.sub(r'\s*}\s*', '}', css_content)
    css_content = re.sub(r'\s*:\s*', ':', css_content)
    css_content = re.sub(r'\s*;\s*', ';', css_content)
    css_content = re.sub(r'\s*,\s*', ',', css_content)
    
    # Remove trailing semicolons before closing braces
    css_content = re.sub(r';+}', '}', css_content)
    
    # Remove leading and trailing whitespace
    css_content = css_content.strip()
    
    return css_content

def create_minified_version():
    """Create a minified version of styles.css"""
    css_file = "styles.css"
    minified_file = "styles.min.css"
    
    if not os.path.exists(css_file):
        print(f"CSS file '{css_file}' not found!")
        return
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        print(f"Error reading CSS file: {e}")
        return
    
    original_size = len(css_content)
    
    # Minify
    minified_css = minify_css(css_content)
    minified_size = len(minified_css)
    
    reduction = original_size - minified_size
    percentage = (reduction / original_size) * 100 if original_size > 0 else 0
    
    try:
        with open(minified_file, 'w', encoding='utf-8') as f:
            f.write(minified_css)
        
        print(f"Minified CSS created: {minified_file}")
        print(f"Original size: {original_size} bytes")
        print(f"Minified size: {minified_size} bytes")
        print(f"Size reduction: {reduction} bytes ({percentage:.1f}%)")
        
    except Exception as e:
        print(f"Error writing minified CSS: {e}")

if __name__ == "__main__":
    create_minified_version()
