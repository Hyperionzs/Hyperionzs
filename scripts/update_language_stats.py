#!/usr/bin/env python3
"""
Script to update the README.md with the most used programming language
from all repositories in the user's GitHub account.
"""

import os
import re
from collections import defaultdict
from github import Github

def get_language_stats():
    """
    Fetch all repositories and calculate language statistics.
    
    Returns:
        dict: Language statistics sorted by count
        str: Primary (most used) language
    """
    # Get GitHub token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set")
        exit(1)
    
    # Initialize GitHub API
    g = Github(token)
    user = g.get_user()
    
    # Count languages across all repositories
    language_count = defaultdict(int)
    
    print(f"Scanning repositories for {user.login}...")
    
    for repo in user.get_repos():
        # Skip forked repositories
        if repo.fork:
            continue
        
        if repo.language:
            language_count[repo.language] += 1
            print(f"  - {repo.name}: {repo.language}")
    
    if not language_count:
        print("No languages found!")
        return {}, None
    
    # Sort by count
    sorted_languages = sorted(language_count.items(), key=lambda x: x[1], reverse=True)
    primary_language = sorted_languages[0][0]
    
    print(f"\n✅ Primary Language: {primary_language}")
    print(f"Language Statistics:")
    for lang, count in sorted_languages:
        print(f"  {lang}: {count} repo(s)")
    
    return dict(sorted_languages), primary_language

def update_readme(language_stats, primary_language):
    """
    Update the README.md file with language statistics.
    
    Args:
        language_stats (dict): Language statistics
        primary_language (str): The most used language
    """
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found")
        return
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create badge for primary language
    language_colors = {
        'Dart': '0175C2',
        'JavaScript': '323330',
        'PHP': '777BB4',
        'Python': '14354C',
        'C++': '00599C',
        'Java': 'ED8B00',
        'TypeScript': '3178c6',
        'Go': '00ADD8',
        'Rust': 'CE422B',
        'Ruby': 'CC342D'
    }
    
    color = language_colors.get(primary_language, '000000')
    primary_badge = f'![{primary_language}](https://img.shields.io/badge/{primary_language}-%23{color}.svg?style=for-the-badge&logo={primary_language.lower()}&logoColor=white)'
    
    # Create language description
    top_3_langs = list(language_stats.keys())[:3]
    langs_str = ', '.join(top_3_langs)
    
    language_description = f'''💡 **Primary Language: {primary_language}**

Most of my projects are written in **{primary_language}**, with significant experience in {langs_str} as well. I focus on building efficient and scalable applications across different domains.'''
    
    # Pattern to find the Most Used Language section
    pattern = r'### 📊 Most Used Language\s*<div align=center>\s*\n([\s\S]*?)\n\s*</div>\s*###'
    
    replacement = f'''### 📊 Most Used Language

<div align=center>

{primary_badge}

[![](https://github-readme-stats.vercel.app/api/top-langs?username=Hyperionzs&show_icons=true&locale=en&layout=compact&theme=radical)]()

{language_description}

</div>

###'''
    
    updated_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # If pattern didn't match, try alternative
    if updated_content == content:
        print("Warning: Could not find exact pattern. Trying alternative...")
        alt_pattern = r'(### 📊 Most Used Language\s*<div align=center>\s*\n)([\s\S]*?)(\n\s*</div>)'
        def replace_func(match):
            return f"{match.group(1)}\n{primary_badge}\n\n[![](https://github-readme-stats.vercel.app/api/top-langs?username=Hyperionzs&show_icons=true&locale=en&layout=compact&theme=radical)]()\n\n{language_description}\n{match.group(3)}"
        updated_content = re.sub(alt_pattern, replace_func, content, flags=re.MULTILINE)
    
    if updated_content == content:
        print("Warning: Could not update README. Pattern may have changed.")
        return
    
    # Write updated content
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ README.md updated successfully!")

def main():
    """
    Main function to orchestrate the update process.
    """
    print("🚀 Starting README language statistics update...\n")
    
    try:
        # Get language statistics
        language_stats, primary_language = get_language_stats()
        
        if not primary_language:
            print("❌ No language data found. Exiting.")
            return
        
        # Update README
        update_readme(language_stats, primary_language)
        print("\n✨ Update completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
