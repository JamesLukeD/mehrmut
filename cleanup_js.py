#!/usr/bin/env python3
"""
JavaScript Cleanup Script for Mehrmut Website
Removes unused JavaScript functions, variables, and optimizes code
"""

import re
import os
import glob
import json
from pathlib import Path

def extract_js_from_html(html_files):
    """Extract all JavaScript code from HTML files"""
    all_js_code = ""
    js_functions = set()
    js_variables = set()
    js_event_handlers = set()
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract inline JavaScript
            script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
            for script in script_matches:
                if script.strip():
                    all_js_code += script + "\n"
            
            # Extract event handlers
            event_patterns = [
                r'onclick=["\']([^"\']*)["\']',
                r'onload=["\']([^"\']*)["\']',
                r'onchange=["\']([^"\']*)["\']',
                r'onsubmit=["\']([^"\']*)["\']',
                r'onmouseover=["\']([^"\']*)["\']',
                r'onmouseout=["\']([^"\']*)["\']'
            ]
            
            for pattern in event_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    js_event_handlers.add(match.strip())
                    all_js_code += match + "\n"
        
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
    
    return all_js_code, js_functions, js_variables, js_event_handlers

def analyze_javascript(js_code):
    """Analyze JavaScript code to find functions, variables, and usage"""
    analysis = {
        'functions': {},
        'variables': {},
        'event_listeners': [],
        'dom_queries': [],
        'api_calls': [],
        'dependencies': []
    }
    
    # Find function declarations
    function_patterns = [
        r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(',
        r'const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function',
        r'let\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function',
        r'var\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function',
        r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:\s*function',  # Object methods
        r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\([^)]*\)\s*=>'  # Arrow functions
    ]
    
    for pattern in function_patterns:
        matches = re.findall(pattern, js_code)
        for match in matches:
            function_name = match if isinstance(match, str) else match[0]
            analysis['functions'][function_name] = {
                'defined': True,
                'called': False,
                'calls': []
            }
    
    # Find variable declarations
    variable_patterns = [
        r'var\s+([a-zA-Z_$][a-zA-Z0-9_$]*)',
        r'let\s+([a-zA-Z_$][a-zA-Z0-9_$]*)',
        r'const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)'
    ]
    
    for pattern in variable_patterns:
        matches = re.findall(pattern, js_code)
        for match in matches:
            analysis['variables'][match] = {
                'defined': True,
                'used': False
            }
    
    # Find function calls
    function_call_pattern = r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
    function_calls = re.findall(function_call_pattern, js_code)
    
    for call in function_calls:
        if call in analysis['functions']:
            analysis['functions'][call]['called'] = True
    
    # Find DOM queries
    dom_patterns = [
        r'document\.getElementById\s*\(["\']([^"\']*)["\']',
        r'document\.querySelector\s*\(["\']([^"\']*)["\']',
        r'document\.querySelectorAll\s*\(["\']([^"\']*)["\']',
        r'document\.getElementsByClassName\s*\(["\']([^"\']*)["\']',
        r'document\.getElementsByTagName\s*\(["\']([^"\']*)["\']'
    ]
    
    for pattern in dom_patterns:
        matches = re.findall(pattern, js_code)
        analysis['dom_queries'].extend(matches)
    
    # Find event listeners
    event_listener_pattern = r'addEventListener\s*\(\s*["\']([^"\']*)["\']'
    event_listeners = re.findall(event_listener_pattern, js_code)
    analysis['event_listeners'] = event_listeners
    
    return analysis

def check_dom_usage(html_files, dom_queries):
    """Check if DOM queries are actually used in HTML"""
    used_queries = set()
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for query in dom_queries:
                # Check for ID usage
                if re.search(rf'id=["\'][^"\']*{re.escape(query)}[^"\']*["\']', content, re.IGNORECASE):
                    used_queries.add(query)
                # Check for class usage
                elif re.search(rf'class=["\'][^"\']*{re.escape(query)}[^"\']*["\']', content, re.IGNORECASE):
                    used_queries.add(query)
                # Check for tag usage
                elif f'<{query}' in content.lower():
                    used_queries.add(query)
        
        except Exception as e:
            print(f"Error checking DOM usage in {html_file}: {e}")
    
    return used_queries

def optimize_javascript(js_code):
    """Optimize JavaScript code"""
    optimized = js_code
    
    # Remove console.log statements (optional - keep for debugging)
    # optimized = re.sub(r'console\.log\([^)]*\);\s*', '', optimized)
    
    # Remove empty lines
    optimized = re.sub(r'\n\s*\n', '\n', optimized)
    
    # Remove trailing whitespace
    optimized = '\n'.join(line.rstrip() for line in optimized.split('\n'))
    
    # Remove comments (basic - be careful with this)
    optimized = re.sub(r'//[^\n]*', '', optimized)
    optimized = re.sub(r'/\*.*?\*/', '', optimized, flags=re.DOTALL)
    
    return optimized

def minify_javascript(js_code):
    """Minify JavaScript code"""
    minified = js_code
    
    # Remove comments
    minified = re.sub(r'//[^\n]*', '', minified)
    minified = re.sub(r'/\*.*?\*/', '', minified, flags=re.DOTALL)
    
    # Remove unnecessary whitespace
    minified = re.sub(r'\s+', ' ', minified)
    
    # Remove whitespace around operators and punctuation
    minified = re.sub(r'\s*([{}();,:])\s*', r'\1', minified)
    minified = re.sub(r'\s*([=+\-*/])\s*', r'\1', minified)
    
    # Remove leading/trailing whitespace
    minified = minified.strip()
    
    return minified

def extract_and_analyze_js(html_files):
    """Extract and analyze all JavaScript"""
    print("Extracting JavaScript from HTML files...")
    
    all_js_code, functions, variables, event_handlers = extract_js_from_html(html_files)
    
    if not all_js_code.strip():
        print("No JavaScript found in HTML files.")
        return None
    
    print(f"Found {len(all_js_code)} characters of JavaScript code")
    
    # Analyze the JavaScript
    print("Analyzing JavaScript usage...")
    analysis = analyze_javascript(all_js_code)
    
    # Check DOM usage
    used_dom_queries = check_dom_usage(html_files, analysis['dom_queries'])
    
    # Print analysis results
    print(f"\n=== JavaScript Analysis ===")
    print(f"Functions found: {len(analysis['functions'])}")
    print(f"Variables found: {len(analysis['variables'])}")
    print(f"DOM queries found: {len(analysis['dom_queries'])}")
    print(f"Event listeners found: {len(analysis['event_listeners'])}")
    
    # Check for unused functions
    unused_functions = [name for name, info in analysis['functions'].items() 
                       if not info['called'] and name not in ['DOMContentLoaded']]
    
    if unused_functions:
        print(f"\nPotentially unused functions:")
        for func in unused_functions:
            print(f"  - {func}")
    
    # Check for unused DOM queries
    unused_dom_queries = set(analysis['dom_queries']) - used_dom_queries
    if unused_dom_queries:
        print(f"\nUnused DOM queries:")
        for query in unused_dom_queries:
            print(f"  - {query}")
    
    return {
        'code': all_js_code,
        'analysis': analysis,
        'used_dom_queries': used_dom_queries,
        'unused_functions': unused_functions,
        'unused_dom_queries': unused_dom_queries
    }

def create_optimized_js_files(js_data):
    """Create optimized JavaScript files"""
    if not js_data:
        return
    
    original_code = js_data['code']
    
    # Create optimized version
    optimized_code = optimize_javascript(original_code)
    
    # Create minified version
    minified_code = minify_javascript(original_code)
    
    # Save files
    with open('extracted_javascript.js', 'w', encoding='utf-8') as f:
        f.write(original_code)
    
    with open('optimized_javascript.js', 'w', encoding='utf-8') as f:
        f.write(optimized_code)
    
    with open('minified_javascript.js', 'w', encoding='utf-8') as f:
        f.write(minified_code)
    
    # Save analysis report
    report = {
        'functions': js_data['analysis']['functions'],
        'variables': js_data['analysis']['variables'],
        'dom_queries': js_data['analysis']['dom_queries'],
        'unused_functions': js_data['unused_functions'],
        'unused_dom_queries': list(js_data['unused_dom_queries']),
        'recommendations': []
    }
    
    # Add recommendations
    if js_data['unused_functions']:
        report['recommendations'].append("Consider removing unused functions to reduce file size")
    
    if js_data['unused_dom_queries']:
        report['recommendations'].append("Review unused DOM queries - they might indicate dead code")
    
    with open('js_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Print size comparison
    original_size = len(original_code)
    optimized_size = len(optimized_code)
    minified_size = len(minified_code)
    
    print(f"\n=== File Sizes ===")
    print(f"Original: {original_size} bytes")
    print(f"Optimized: {optimized_size} bytes ({((original_size - optimized_size) / original_size * 100):.1f}% reduction)")
    print(f"Minified: {minified_size} bytes ({((original_size - minified_size) / original_size * 100):.1f}% reduction)")
    
    print(f"\nFiles created:")
    print(f"  - extracted_javascript.js (original code)")
    print(f"  - optimized_javascript.js (optimized)")
    print(f"  - minified_javascript.js (minified)")
    print(f"  - js_analysis_report.json (analysis report)")

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
    
    print(f"Found {len(html_files)} HTML files to analyze")
    
    if not html_files:
        print("No HTML files found!")
        return
    
    # Extract and analyze JavaScript
    js_data = extract_and_analyze_js(html_files)
    
    if js_data:
        create_optimized_js_files(js_data)
    else:
        print("No JavaScript code found to optimize.")

if __name__ == "__main__":
    main()
