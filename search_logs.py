#!/usr/bin/env python3
"""
Search for "may-britt moser" (case-insensitive) in log files.
Usage: python search_logs.py [directory] [--extension .txt]
"""

import os
import sys
import argparse
from pathlib import Path

def search_in_file(filepath, search_term):
    """Search for term in a single file, return matches with context."""
    matches = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if search_term.lower() in line.lower():
                    # Get context: 1 line before and after
                    start = max(0, i - 1)
                    end = min(len(lines), i + 2)
                    context = ''.join(lines[start:end]).strip()
                    matches.append({
                        'line_num': i + 1,
                        'line': line.strip(),
                        'context': context
                    })
    except Exception as e:
        print(f"  Error reading {filepath}: {e}", file=sys.stderr)
    return matches

def search_directory(directory, search_term, extensions=None):
    """Recursively search all files in directory."""
    results = {}
    search_path = Path(directory)
    
    if not search_path.exists():
        print(f"Directory not found: {directory}")
        return results
    
    # Default extensions for log files
    if extensions is None:
        extensions = ['.txt', '.log', '.md', '.json', '.csv', '.xml', '.html']
    
    file_count = 0
    for filepath in search_path.rglob('*'):
        if filepath.is_file():
            # Check extension if specified
            if extensions and filepath.suffix.lower() not in extensions:
                continue
            
            file_count += 1
            matches = search_in_file(filepath, search_term)
            if matches:
                results[str(filepath)] = matches
    
    print(f"\nSearched {file_count} files in {directory}")
    return results

def main():
    parser = argparse.ArgumentParser(description='Search for "may-britt moser" in log files')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to search (default: current)')
    parser.add_argument('--ext', '-e', nargs='*', help='File extensions to search (e.g., .txt .log)')
    parser.add_argument('--term', '-t', default='may-britt moser', help='Search term (default: may-britt moser)')
    parser.add_argument('--all', '-a', action='store_true', help='Search all file types')
    
    args = parser.parse_args()
    
    extensions = None
    if args.ext:
        extensions = [e if e.startswith('.') else f'.{e}' for e in args.ext]
    elif args.all:
        extensions = None  # Search all files
    
    search_term = args.term
    print(f'Searching for "{search_term}" in {args.directory}...')
    
    results = search_directory(args.directory, search_term, extensions)
    
    if results:
        print(f"\n{'='*60}")
        print(f"FOUND IN {len(results)} FILE(S):")
        print(f"{'='*60}\n")
        
        for filepath, matches in results.items():
            print(f"\n📄 {filepath}")
            print(f"   {len(matches)} match(es)")
            print("-" * 50)
            for m in matches:
                print(f"   Line {m['line_num']}: {m['line'][:100]}{'...' if len(m['line']) > 100 else ''}")
            print()
    else:
        print(f'\nNo matches found for "{search_term}"')

if __name__ == '__main__':
    main()
