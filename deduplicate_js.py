#!/usr/bin/env python3
"""
Advanced JavaScript Deduplication and Optimization Script
Removes duplicate code blocks and creates a consolidated JavaScript file
"""

import re
import os
import hashlib
from collections import defaultdict

def extract_js_blocks_from_html(html_files):
    """Extract JavaScript blocks with their source files"""
    js_blocks = []
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract script blocks
            script_pattern = r'<script[^>]*>(.*?)</script>'
            matches = re.finditer(script_pattern, content, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                script_content = match.group(1).strip()
                if script_content:
                    js_blocks.append({
                        'content': script_content,
                        'source_file': html_file,
                        'hash': hashlib.md5(script_content.encode()).hexdigest()
                    })
        
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
    
    return js_blocks

def find_duplicate_blocks(js_blocks):
    """Find duplicate JavaScript blocks"""
    hash_to_blocks = defaultdict(list)
    
    for block in js_blocks:
        hash_to_blocks[block['hash']].append(block)
    
    duplicates = {h: blocks for h, blocks in hash_to_blocks.items() if len(blocks) > 1}
    unique_blocks = {h: blocks[0] for h, blocks in hash_to_blocks.items()}
    
    return duplicates, unique_blocks

def consolidate_javascript(unique_blocks):
    """Consolidate unique JavaScript blocks into one file"""
    consolidated_js = ""
    
    # Group by functionality
    dom_ready_blocks = []
    function_definitions = []
    event_listeners = []
    other_code = []
    
    for block_hash, block in unique_blocks.items():
        content = block['content']
        
        if 'DOMContentLoaded' in content:
            dom_ready_blocks.append(content)
        elif re.search(r'function\s+\w+', content):
            function_definitions.append(content)
        elif 'addEventListener' in content:
            event_listeners.append(content)
        else:
            other_code.append(content)
    
    # Build consolidated JavaScript
    consolidated_js += "/* === FUNCTION DEFINITIONS === */\n"
    for func in function_definitions:
        consolidated_js += func + "\n\n"
    
    consolidated_js += "/* === OTHER CODE === */\n"
    for code in other_code:
        consolidated_js += code + "\n\n"
    
    consolidated_js += "/* === EVENT LISTENERS === */\n"
    for listener in event_listeners:
        consolidated_js += listener + "\n\n"
    
    # Merge DOM ready blocks
    if dom_ready_blocks:
        consolidated_js += "/* === DOM READY === */\n"
        consolidated_js += "document.addEventListener('DOMContentLoaded', function() {\n"
        
        for dom_block in dom_ready_blocks:
            # Extract content from DOMContentLoaded wrapper
            inner_content = re.search(r'DOMContentLoaded["\'],\s*function\s*\(\s*\)\s*\{(.*?)\}\s*\);', 
                                    dom_block, re.DOTALL)
            if inner_content:
                # Clean up the extracted content
                content = inner_content.group(1).strip()
                # Remove extra indentation
                lines = content.split('\n')
                min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
                cleaned_lines = [line[min_indent:] if line.strip() else line for line in lines]
                consolidated_js += '\n'.join(cleaned_lines) + "\n\n"
        
        consolidated_js += "});\n"
    
    return consolidated_js

def optimize_consolidated_js(js_code):
    """Optimize the consolidated JavaScript"""
    optimized = js_code
    
    # Remove duplicate variable declarations
    var_declarations = {}
    
    # Find all variable declarations
    var_patterns = [
        (r'const\s+(\w+)\s*=', 'const'),
        (r'let\s+(\w+)\s*=', 'let'),
        (r'var\s+(\w+)\s*=', 'var')
    ]
    
    for pattern, var_type in var_patterns:
        matches = re.finditer(pattern, optimized)
        for match in matches:
            var_name = match.group(1)
            if var_name in var_declarations:
                print(f"  Found duplicate variable declaration: {var_name}")
            var_declarations[var_name] = var_type
    
    # Remove empty functions
    optimized = re.sub(r'function\s+\w+\s*\(\s*\)\s*\{\s*\}', '', optimized)
    
    # Clean up excessive whitespace
    optimized = re.sub(r'\n\s*\n\s*\n', '\n\n', optimized)
    
    return optimized

def create_external_js_file(consolidated_js, html_files):
    """Create external JavaScript file and update HTML files"""
    
    # Write consolidated JavaScript
    js_filename = 'scripts.js'
    with open(js_filename, 'w', encoding='utf-8') as f:
        f.write(consolidated_js)
    
    print(f"Created consolidated JavaScript file: {js_filename}")
    
    # Create minified version
    minified_js = minify_js_advanced(consolidated_js)
    minified_filename = 'scripts.min.js'
    with open(minified_filename, 'w', encoding='utf-8') as f:
        f.write(minified_js)
    
    print(f"Created minified JavaScript file: {minified_filename}")
    
    # Calculate size savings
    original_size = len(consolidated_js)
    minified_size = len(minified_js)
    reduction = ((original_size - minified_size) / original_size) * 100
    
    print(f"Original size: {original_size} bytes")
    print(f"Minified size: {minified_size} bytes ({reduction:.1f}% reduction)")
    
    return js_filename, minified_filename

def minify_js_advanced(js_code):
    """Advanced JavaScript minification"""
    minified = js_code
    
    # Remove comments
    minified = re.sub(r'//[^\n]*', '', minified)
    minified = re.sub(r'/\*.*?\*/', '', minified, flags=re.DOTALL)
    
    # Remove unnecessary whitespace
    minified = re.sub(r'\s+', ' ', minified)
    minified = re.sub(r'\s*([{}();,:])\s*', r'\1', minified)
    minified = re.sub(r'\s*([=+\-*/!<>])\s*', r'\1', minified)
    
    # Remove trailing semicolons before }
    minified = re.sub(r';\s*}', '}', minified)
    
    return minified.strip()

def generate_html_update_script(js_filename, html_files):
    """Generate a script to update HTML files to use external JS"""
    
    script_content = f"""#!/usr/bin/env python3
\"\"\"
Script to update HTML files to use external JavaScript
Run this script to replace inline JavaScript with external file reference
\"\"\"

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
            script_tag = f'    <script src="{js_filename}"></script>\\n  </body>'
            content = content.replace('</body>', script_tag)
        
        # Create backup
        backup_file = html_file + '.backup'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(open(html_file, 'r').read())
        
        # Write updated file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {{html_file}} (backup: {{backup_file}})")
        
    except Exception as e:
        print(f"Error updating {{html_file}}: {{e}}")

def main():
    html_files = {html_files}
    
    response = input(f"Update {{len(html_files)}} HTML files to use external JavaScript? (y/n): ")
    if response.lower() == 'y':
        for html_file in html_files:
            update_html_file(html_file)
        print("HTML files updated successfully!")
    else:
        print("HTML update cancelled.")

if __name__ == "__main__":
    main()
"""
    
    with open('update_html_for_external_js.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Created HTML update script: update_html_for_external_js.py")

def main():
    """Main function for JavaScript deduplication"""
    
    # Find all HTML files
    html_files = []
    for pattern in ["*.html", "projects/*.html", "articles/*.html"]:
        import glob
        html_files.extend(glob.glob(pattern))
    
    print(f"Analyzing {len(html_files)} HTML files for JavaScript...")
    
    # Extract JavaScript blocks
    js_blocks = extract_js_blocks_from_html(html_files)
    print(f"Found {len(js_blocks)} JavaScript blocks")
    
    # Find duplicates
    duplicates, unique_blocks = find_duplicate_blocks(js_blocks)
    
    if duplicates:
        print(f"\\nFound {len(duplicates)} sets of duplicate JavaScript blocks:")
        total_duplicates = 0
        for block_hash, blocks in duplicates.items():
            print(f"  - Block appears in {len(blocks)} files:")
            for block in blocks:
                print(f"    * {block['source_file']}")
            total_duplicates += len(blocks) - 1
        
        print(f"\\nTotal duplicate blocks: {total_duplicates}")
        print(f"Unique blocks: {len(unique_blocks)}")
        
        # Consolidate JavaScript
        print("\\nConsolidating JavaScript...")
        consolidated_js = consolidate_javascript(unique_blocks)
        
        # Optimize
        print("Optimizing consolidated JavaScript...")
        optimized_js = optimize_consolidated_js(consolidated_js)
        
        # Create external files
        js_filename, minified_filename = create_external_js_file(optimized_js, html_files)
        
        # Generate HTML update script
        generate_html_update_script(js_filename, html_files)
        
        print(f"\\n=== Summary ===")
        print(f"Original blocks: {len(js_blocks)}")
        print(f"Duplicate blocks removed: {total_duplicates}")
        print(f"Final unique blocks: {len(unique_blocks)}")
        print(f"External JavaScript file: {js_filename}")
        print(f"Minified file: {minified_filename}")
        print(f"\\nNext steps:")
        print(f"1. Review the consolidated JavaScript in {js_filename}")
        print(f"2. Run 'python3 update_html_for_external_js.py' to update HTML files")
        print(f"3. Test your website to ensure everything works correctly")
        
    else:
        print("No duplicate JavaScript blocks found.")

if __name__ == "__main__":
    main()
