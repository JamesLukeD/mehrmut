#!/usr/bin/env python3
"""
Advanced CSS Cleanup and Optimization Script
Removes duplicates, minifies, and organizes CSS
"""

import re
import os
from collections import defaultdict

def remove_duplicate_rules(css_content):
    """Remove duplicate CSS rules"""
    print("Removing duplicate CSS rules...")
    
    # Parse rules with their properties
    rule_pattern = r'([^{}]+)\s*\{([^{}]*)\}'
    rules = {}
    rule_order = []
    
    matches = re.finditer(rule_pattern, css_content, re.DOTALL)
    
    for match in matches:
        selector = match.group(1).strip()
        properties = match.group(2).strip()
        
        # Normalize selector (remove extra whitespace)
        normalized_selector = ' '.join(selector.split())
        
        if normalized_selector and properties:
            if normalized_selector in rules:
                print(f"  Found duplicate selector: {normalized_selector}")
                # Keep the last occurrence (overrides earlier ones)
                rules[normalized_selector] = properties
            else:
                rules[normalized_selector] = properties
                rule_order.append(normalized_selector)
    
    # Rebuild CSS
    cleaned_css = ""
    for selector in rule_order:
        if selector in rules:
            cleaned_css += f"{selector} {{\n  {rules[selector]}\n}}\n\n"
    
    return cleaned_css

def remove_empty_rules(css_content):
    """Remove CSS rules with no properties"""
    print("Removing empty CSS rules...")
    
    # Remove rules that have empty or whitespace-only content
    cleaned = re.sub(r'[^{}]+\{\s*\}', '', css_content)
    
    return cleaned

def optimize_properties(css_content):
    """Optimize CSS properties (remove duplicates within rules)"""
    print("Optimizing CSS properties...")
    
    def optimize_rule_properties(match):
        selector = match.group(1)
        properties_block = match.group(2)
        
        # Parse individual properties
        properties = {}
        prop_pattern = r'([^:;]+):\s*([^;]+);?'
        
        for prop_match in re.finditer(prop_pattern, properties_block):
            prop_name = prop_match.group(1).strip()
            prop_value = prop_match.group(2).strip()
            
            if prop_name and prop_value:
                # Keep the last occurrence of each property
                properties[prop_name] = prop_value
        
        # Rebuild properties block
        if properties:
            optimized_props = ';\n  '.join([f"{name}: {value}" for name, value in properties.items()])
            return f"{selector} {{\n  {optimized_props};\n}}"
        else:
            return ""
    
    # Apply optimization to each rule
    rule_pattern = r'([^{}]+)\s*\{([^{}]*)\}'
    optimized = re.sub(rule_pattern, optimize_rule_properties, css_content, flags=re.DOTALL)
    
    return optimized

def organize_css_sections(css_content):
    """Organize CSS into logical sections"""
    print("Organizing CSS sections...")
    
    sections = {
        'reset': [],
        'base': [],
        'layout': [],
        'components': [],
        'utilities': [],
        'responsive': []
    }
    
    # Define patterns for different sections
    section_patterns = {
        'reset': [r'^\*\s*{', r'^html\s*{', r'^body\s*{', r'box-sizing'],
        'base': [r'^[a-z]+\s*{', r'^a\s*{', r'^img\s*{', r'^p\s*{', r'^h[1-6]\s*{'],
        'layout': [r'\.header', r'\.footer', r'\.nav', r'\.main', r'\.container'],
        'components': [r'\.btn', r'\.card', r'\.modal', r'\.dropdown'],
        'responsive': [r'@media']
    }
    
    # Parse rules
    rule_pattern = r'([^{}]+)\s*\{([^{}]*)\}'
    rules = re.findall(rule_pattern, css_content, re.DOTALL)
    
    for selector, properties in rules:
        selector = selector.strip()
        properties = properties.strip()
        
        if not selector or not properties:
            continue
        
        # Categorize rule
        categorized = False
        for section, patterns in section_patterns.items():
            for pattern in patterns:
                if re.search(pattern, selector, re.IGNORECASE):
                    sections[section].append((selector, properties))
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            sections['utilities'].append((selector, properties))
    
    # Rebuild CSS with sections
    organized_css = ""
    
    section_headers = {
        'reset': '/* === RESET & BASE === */',
        'base': '/* === BASE ELEMENTS === */',
        'layout': '/* === LAYOUT === */',
        'components': '/* === COMPONENTS === */',
        'utilities': '/* === UTILITIES === */',
        'responsive': '/* === RESPONSIVE === */'
    }
    
    for section_name, section_rules in sections.items():
        if section_rules:
            organized_css += f"\n{section_headers[section_name]}\n"
            for selector, properties in section_rules:
                organized_css += f"{selector} {{\n  {properties}\n}}\n\n"
    
    return organized_css

def format_css(css_content):
    """Format CSS for better readability"""
    print("Formatting CSS...")
    
    # Normalize whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    
    # Format rules
    def format_rule(match):
        selector = match.group(1).strip()
        properties = match.group(2).strip()
        
        # Format properties
        formatted_props = re.sub(r';\s*', ';\n  ', properties)
        formatted_props = re.sub(r'{\s*', '', formatted_props)
        formatted_props = re.sub(r'\s*}', '', formatted_props)
        
        if formatted_props and not formatted_props.endswith(';'):
            formatted_props += ';'
        
        return f"{selector} {{\n  {formatted_props}\n}}"
    
    rule_pattern = r'([^{}]+)\s*\{([^{}]*)\}'
    formatted = re.sub(rule_pattern, format_rule, css_content)
    
    # Clean up extra newlines
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)
    
    return formatted

def advanced_cleanup(css_file):
    """Perform advanced CSS cleanup"""
    print(f"Advanced cleanup of: {css_file}")
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        print(f"Error reading CSS file: {e}")
        return
    
    original_size = len(css_content)
    print(f"Original size: {original_size} bytes")
    
    # Apply optimizations
    css_content = remove_empty_rules(css_content)
    css_content = optimize_properties(css_content)
    css_content = remove_duplicate_rules(css_content)
    css_content = format_css(css_content)
    
    new_size = len(css_content)
    reduction = original_size - new_size
    percentage = (reduction / original_size) * 100 if original_size > 0 else 0
    
    print(f"Optimized size: {new_size} bytes")
    print(f"Size reduction: {reduction} bytes ({percentage:.1f}%)")
    
    # Create backup
    backup_file = css_file + '.advanced_backup'
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(open(css_file, 'r').read())
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        return
    
    # Write optimized CSS
    try:
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("Advanced cleanup completed!")
    except Exception as e:
        print(f"Error writing optimized CSS: {e}")

def main():
    """Main function for advanced cleanup"""
    css_file = "styles.css"
    
    if not os.path.exists(css_file):
        print(f"CSS file '{css_file}' not found!")
        return
    
    response = input("Perform advanced CSS cleanup? This will:\n"
                    "- Remove duplicate rules\n"
                    "- Optimize properties\n"
                    "- Remove empty rules\n"
                    "- Format for readability\n"
                    "Continue? (y/n): ")
    
    if response.lower() == 'y':
        advanced_cleanup(css_file)
    else:
        print("Advanced cleanup cancelled.")

if __name__ == "__main__":
    main()
