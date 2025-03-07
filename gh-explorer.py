#\!/data/data/com.termux/files/usr/bin/python3

# gh-explorer.py - A TUI for GitHub search and exploration
# This is a skeleton file that we'll develop further

import sys
import os
import subprocess
import json
from datetime import datetime

def run_gh_command(args):
    Run a GitHub CLI command and return the output
    try:
        cmd = ['gh'] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(e.stderr)
        return None

def main_menu():
    """Display the main menu"""
    print("
📚 GitHub Explorer - Terminal UI
")
    print("1. Search Repositories")
    print("2. Search Code")
    print("3. View Recent Repositories")
    print("4. Create a Gist")
    print("5. Search by Topic")
    print("6. Search by Language")
    print("0. Exit")
    
    choice = input("
Enter your choice (0-6): ")
    return choice

def search_repos():
    """Search for repositories"""
    query = input("
Enter search terms: ")
    if not query:
        return
    
    print("
Searching for repositories...")
    try:
        # Get JSON output for more flexibility
        result = run_gh_command(['search', 'repos', query, '--limit', '20', '--json', 'nameWithOwner,description,stargazersCount,url'])
        if not result:
            return
        
        repos = json.loads(result)
        
        if not repos:
            print("No repositories found.")
            return
        
        # Display results
        print(f"
Found {len(repos)} repositories:
")
        for i, repo in enumerate(repos):
            stars = repo.get('stargazersCount', 0)
            print(f"{i+1}. {repo['nameWithOwner']} ({stars} ⭐)")
            print(f"   {repo.get('description', 'No description')}")
            print()
        
        # Let user select a repo to view
        choice = input("Enter number to view (or press Enter to go back): ")
        if choice.isdigit() and 1 <= int(choice) <= len(repos):
            idx = int(choice) - 1
            selected_repo = repos[idx]['nameWithOwner']
            view_repo(selected_repo)
    except Exception as e:
        print(f"Error: {e}")

def view_repo(repo_name):
    """View a specific repository"""
    print(f"
Viewing repository: {repo_name}
")
    
    # Show repo info
    run_gh_command(['repo', 'view', repo_name])
    
    print("
Options:")
    print("1. Open in browser")
    print("2. Clone repository")
    print("3. Back to search results")
    
    choice = input("
Enter choice (1-3): ")
    
    if choice == '1':
        run_gh_command(['repo', 'view', repo_name, '--web'])
    elif choice == '2':
        print(f"Cloning {repo_name}...")
        run_gh_command(['repo', 'clone', repo_name])

def search_code():
    """Search for code"""
    query = input("
Enter code search terms: ")
    if not query:
        return
    
    print("
Searching for code (this may take a moment)...")
    result = run_gh_command(['search', 'code', query, '--limit', '15'])
    print(result)
    
    # This is just a simple implementation - we would enhance this in the future

def search_by_topic():
    """Search repositories by topic"""
    topic = input("
Enter topic: ")
    if not topic:
        return
    
    print(f"
Searching for repositories with topic: {topic}...")
    result = run_gh_command(['search', 'repos', '--topic', topic, '--sort', 'stars', '--limit', '20'])
    print(result)

def search_by_language():
    """Search repositories by language"""
    language = input("
Enter programming language: ")
    if not language:
        return
    
    print(f"
Searching for {language} repositories...")
    result = run_gh_command(['search', 'repos', '--language', language, '--sort', 'stars', '--limit', '20'])
    print(result)

def create_gist():
    """Create a gist from file or text"""
    print("
Create a Gist:
")
    print("1. From file")
    print("2. From text input")
    print("3. Back to main menu")
    
    choice = input("
Enter choice (1-3): ")
    
    if choice == '1':
        filepath = input("Enter file path: ")
        if os.path.isfile(filepath):
            desc = input("Description (optional): ")
            cmd = ['gist', 'create', filepath]
            if desc:
                cmd.extend(['-d', desc])
            result = run_gh_command(cmd)
            print(f"Gist created: {result}")
        else:
            print("File not found.")
    
    elif choice == '2':
        content = input("Enter content: ")
        if content:
            # Write to temp file
            temp_file = f"/tmp/gist_{int(datetime.now().timestamp())}.txt"
            with open(temp_file, 'w') as f:
                f.write(content)
            
            desc = input("Description (optional): ")
            cmd = ['gist', 'create', temp_file]
            if desc:
                cmd.extend(['-d', desc])
            
            result = run_gh_command(cmd)
            print(f"Gist created: {result}")
            
            # Clean up
            os.remove(temp_file)

def main():
    """Main program loop"""
    while True:
        choice = main_menu()
        
        if choice == '0':
            print("
Exiting GitHub Explorer. Goodbye\!
")
            sys.exit(0)
        elif choice == '1':
            search_repos()
        elif choice == '2':
            search_code()
        elif choice == '3':
            print("
Feature not implemented yet")
        elif choice == '4':
            create_gist()
        elif choice == '5':
            search_by_topic()
        elif choice == '6':
            search_by_language()
        else:
            print("
Invalid choice. Please try again.")
        
        input("
Press Enter to continue...")

if __name__ == "__main__":
    try:
        # Check if gh is installed
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
        main()
    except subprocess.CalledProcessError:
        print("Error: GitHub CLI (gh) is not installed or not in PATH.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("
Exiting GitHub Explorer. Goodbye\!
")
        sys.exit(0)

