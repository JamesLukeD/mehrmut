#!/usr/bin/env python3
"""
CSS Cleanup Script for Mehrmut Website
Removes unused CSS rules by analyzing HTML files
"""

import re
import os
import glob
from pathlib import Path

def extract_classes_from_html(html_files):
    """Extract all CSS classes used in HTML files"""
    used_classes = set()
    used_ids = set()
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find class attributes
            class_matches = re.findall(r'class=["\']([^"\']*)["\']', content, re.IGNORECASE)
            for match in class_matches:
                classes = match.strip().split()
                used_classes.update(classes)
            
            # Find id attributes
            id_matches = re.findall(r'id=["\']([^"\']*)["\']', content, re.IGNORECASE)
            for match in id_matches:
                used_ids.add(match.strip())
                
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
    
    return used_classes, used_ids

def parse_css_rules(css_content):
    """Parse CSS and extract selectors"""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Find all CSS rules
    rules = []
    rule_pattern = r'([^{}]+)\s*\{([^{}]*)\}'
    
    matches = re.finditer(rule_pattern, css_content, re.DOTALL)
    
    for match in matches:
        selector = match.group(1).strip()
        properties = match.group(2).strip()
        
        # Skip empty rules
        if properties:
            rules.append({
                'selector': selector,
                'properties': properties,
                'full_rule': match.group(0)
            })
    
    return rules

def is_selector_used(selector, used_classes, used_ids):
    """Check if a CSS selector is used in the HTML"""
    # Always keep certain selectors
    keep_selectors = [
        '*', 'html', 'body', 'a', 'img', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'li', 'ol', 'div', 'span', 'section', 'header', 'footer', 'nav',
        'main', 'article', 'aside', 'button', 'input', 'form', 'table', 'tr', 'td', 'th'
    ]
    
    # Check for pseudo-selectors and media queries
    if (':' in selector or '@' in selector or 
        any(keep in selector.lower() for keep in keep_selectors)):
        return True
    
    # Split multiple selectors
    selectors = [s.strip() for s in selector.split(',')]
    
    for sel in selectors:
        # Remove pseudo-classes and pseudo-elements for checking
        clean_sel = re.sub(r':[a-zA-Z-]+(\([^)]*\))?', '', sel)
        clean_sel = re.sub(r'::[a-zA-Z-]+', '', clean_sel)
        
        # Check for class selectors
        class_matches = re.findall(r'\.([a-zA-Z0-9_-]+)', clean_sel)
        for class_name in class_matches:
            if class_name in used_classes:
                return True
        
        # Check for ID selectors
        id_matches = re.findall(r'#([a-zA-Z0-9_-]+)', clean_sel)
        for id_name in id_matches:
            if id_name in used_ids:
                return True
        
        # Check for element selectors (keep them)
        if re.match(r'^[a-zA-Z][a-zA-Z0-9]*(\s|$)', clean_sel.strip()):
            return True
    
    return False

def cleanup_css(css_file, html_files):
    """Remove unused CSS rules"""
    print(f"Analyzing CSS file: {css_file}")
    
    # Extract used classes and IDs from HTML
    print("Extracting classes and IDs from HTML files...")
    used_classes, used_ids = extract_classes_from_html(html_files)
    
    print(f"Found {len(used_classes)} unique classes")
    print(f"Found {len(used_ids)} unique IDs")
    
    # Read CSS file
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        print(f"Error reading CSS file: {e}")
        return
    
    # Parse CSS rules
    print("Parsing CSS rules...")
    rules = parse_css_rules(css_content)
    print(f"Found {len(rules)} CSS rules")
    
    # Check which rules are used
    used_rules = []
    unused_rules = []
    
    for rule in rules:
        if is_selector_used(rule['selector'], used_classes, used_ids):
            used_rules.append(rule)
        else:
            unused_rules.append(rule)
    
    print(f"Used rules: {len(used_rules)}")
    print(f"Unused rules: {len(unused_rules)}")
    
    if unused_rules:
        print("\nUnused CSS rules:")
        for rule in unused_rules[:10]:  # Show first 10
            print(f"  - {rule['selector']}")
        if len(unused_rules) > 10:
            print(f"  ... and {len(unused_rules) - 10} more")
    
    # Create cleaned CSS
    cleaned_css = ""
    current_pos = 0
    
    # Rebuild CSS with only used rules
    for rule in used_rules:
        # Find the rule in original CSS to preserve formatting
        rule_start = css_content.find(rule['full_rule'], current_pos)
        if rule_start != -1:
            # Add any content before this rule (comments, etc.)
            before_rule = css_content[current_pos:rule_start]
            cleaned_css += before_rule
            
            # Add the rule
            cleaned_css += rule['full_rule']
            current_pos = rule_start + len(rule['full_rule'])
    
    # Add any remaining content
    cleaned_css += css_content[current_pos:]
    
    # Create backup
    backup_file = css_file + '.backup'
    print(f"\nCreating backup: {backup_file}")
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
    except Exception as e:
        print(f"Error creating backup: {e}")
        return
    
    # Write cleaned CSS
    try:
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_css)
        print(f"CSS cleaned successfully!")
        print(f"Removed {len(unused_rules)} unused rules")
        
        # Calculate size reduction
        old_size = len(css_content)
        new_size = len(cleaned_css)
        reduction = old_size - new_size
        percentage = (reduction / old_size) * 100 if old_size > 0 else 0
        
        print(f"Size reduction: {reduction} bytes ({percentage:.1f}%)")
        
    except Exception as e:
        print(f"Error writing cleaned CSS: {e}")

def main():
    """Main function"""
    # Find all HTML files
    html_files = []
    
    # Current directory HTML files
    html_files.extend(glob.glob("*.html"))
    
    # Projects directory HTML files
    if os.path.exists("projects"):
        html_files.extend(glob.glob("projects/*.html"))
    
    # Articles directory HTML files
    if os.path.exists("articles"):
        html_files.extend(glob.glob("articles/*.html"))
    
    print(f"Found {len(html_files)} HTML files:")
    for html_file in html_files:
        print(f"  - {html_file}")
    
    if not html_files:
        print("No HTML files found!")
        return
    
    # Find CSS file
    css_file = "styles.css"
    if not os.path.exists(css_file):
        print(f"CSS file '{css_file}' not found!")
        return
    
    # Run cleanup
    cleanup_css(css_file, html_files)

if __name__ == "__main__":
    main()
