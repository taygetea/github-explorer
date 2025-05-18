#!/usr/bin/env python3

# gh-explorer.py - A TUI for GitHub search and exploration
# This is a skeleton file that we'll develop further

import sys
import os
import subprocess
import json
from datetime import datetime

def run_gh_command(args):
    """Run a GitHub CLI command and return the output"""
    try:
        cmd = ['gh'] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True) #TODO i have a bad feeling about this but i dont know why
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(e.stderr)
        return None

def main_menu(): #TODO as noted in main, modern cli software doesnt tend to have ui like this for reasons
    """Display the main menu"""
    print("\n📚 GitHub Explorer - Terminal UI\n")
    print("1. Search Repositories")
    print("2. Search Code")
    print("3. View Recent Repositories")
    print("4. Create a Gist")
    print("5. Search by Topic")
    print("6. Search by Language")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-6): ")
    return choice

def search_repos():
    """Search for repositories"""
    query = input("\nEnter search terms: ")
    if not query:
        return
    
    print("\nSearching for repositories...")
    try:
        # Get JSON output for more flexibility
        result = run_gh_command(['search', 'repos', query, '--limit', '20', '--json', 'fullName,description,stargazersCount,url']) #TODO hardcoding...
        if not result:
            return
        
        repos = json.loads(result)
        
        if not repos:
            print("No repositories found.")
            return
        
        # Display results
        print(f"\nFound {len(repos)} repositories:\n") #TODO paginate/scroll this. fzf?
        for i, repo in enumerate(repos):
            stars = repo.get('stargazersCount', 0)
            print(f"{i+1}. {repo['fullName']} ({stars} ⭐)")
            print(f"   {repo.get('description', 'No description')}")
            print()
        
        # Let user select a repo to view
        choice = input("Enter number to view (or press Enter to go back): ") # TODO actually display the numbers. the index is locked in that enumerate. maybe this should be fzf
        if choice.isdigit() and 1 <= int(choice) <= len(repos):
            idx = int(choice) - 1
            selected_repo = repos[idx]['fullName']
            view_repo(selected_repo)
    except Exception as e:
        print(f"Error: {e}")

def view_repo(repo_name):
    """View a specific repository"""
    print(f"\nViewing repository: {repo_name}\n")
    
    # Show repo info
    run_gh_command(['repo', 'view', repo_name])
    
    print("\nOptions:")
    print("1. Open in browser")
    print("2. Clone repository")
    print("3. Back to search results")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == '1':
        run_gh_command(['repo', 'view', repo_name, '--web']) #TODO we are viewing this in the terminal. currently the markdown on this sucks. bat, bat, glow?
    elif choice == '2':
        print(f"Cloning {repo_name}...")
        run_gh_command(['repo', 'clone', repo_name])

def search_code():
    """Search for code"""
    query = input("\nEnter code search terms: ") #TODO make it more clear what kind of search this is doing. if i type "term1 term2" here, is it term1 OR term2, term1 AND term2, the string "term1 term2"?
    if not query:
        return
    
    print("\nSearching for code (this may take a moment)...")
    result = run_gh_command(['search', 'code', query, '--limit', '15']) #TODO dont hardcode limit, fzf, etc etc
    print(result)
    
    # This is just a simple implementation - we would enhance this in the future

def search_by_topic(): #TODO topics on github suck. projects that want to be searchable by them have to include many overlapping tags. wants to be an embedding search. maybe a cached list
    """Search repositories by topic"""
    topic = input("\nEnter topic: ")
    if not topic:
        return
    
    print(f"\nSearching for repositories with topic: {topic}...")
    result = run_gh_command(['search', 'repos', '--topic', topic, '--sort', 'stars', '--limit', '20']) #TODO hardcode
    print(result)

def search_by_language():
    """Search repositories by language"""
    language = input("\nEnter programming language: ")#TODO this definitely should be fzf and a list somewhere
    if not language:
        return
    
    print(f"\nSearching for {language} repositories...")
    result = run_gh_command(['search', 'repos', '--language', language, '--sort', 'stars', '--limit', '20'])#TODO hardcode
    print(result)

def create_gist():#TODO shouldnt this be a gh extension instead? wait. it is. then why are we screwing with it so much?
    """Create a gist from file or text"""
    print("\nCreate a Gist:\n")#TODO all this choice logic is overdetermined and kinda ugly. 
    print("1. From file")
    print("2. From text input")
    print("3. Back to main menu")
    
    choice = input("\nEnter choice (1-3): ")
    
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
            temp_file = f"/tmp/gist_{int(datetime.now().timestamp())}.txt" #TODO md? maybe? do we need this temp file step?
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
        choice = main_menu() #TODO this is all very opaque. surely theres a better way.
        
        if choice == '0':
            print("\nExiting GitHub Explorer. Goodbye!\n")
            sys.exit(0)
        elif choice == '1':
            search_repos()
        elif choice == '2':
            search_code()
        elif choice == '3':
            print("\nFeature not implemented yet") #TODO which feature?
        elif choice == '4':
            create_gist()
        elif choice == '5':
            search_by_topic()
        elif choice == '6':
            search_by_language()
        else:
            print("\nInvalid choice. Please try again.") #TODO just exit
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        # Check if gh is installed
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
        main()
    except subprocess.CalledProcessError:
        print("Error: GitHub CLI (gh) is not installed or not in PATH.") #TODO not in path? interesting. how does the automatic path repair in pipx etc work?
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting GitHub Explorer. Goodbye!\n")
        sys.exit(0)
