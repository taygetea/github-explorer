#!/usr/bin/env python3
"""
GitHub API client using the GitHub CLI (gh) as a backend
"""

import json
import subprocess
import shlex
from typing import Dict, List, Optional, Any, Union

class GitHubClient:
    """Client for interacting with GitHub through the GitHub CLI."""
    
    def __init__(self):
        """Initialize the GitHub client and verify gh is installed."""
        self._check_gh_installed()
        
    def _check_gh_installed(self):
        """Check if GitHub CLI is installed and throw error if not."""
        try:
            self.run_command(["--version"])
        except Exception as e:
            raise RuntimeError(
                "GitHub CLI (gh) is not installed or not in PATH. "
                "Please install it from https://cli.github.com/"
            ) from e
    
    def run_command(self, args: List[str]) -> str:
        """Run a GitHub CLI command and return the output."""
        try:
            cmd = ["gh"] + args
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"GitHub CLI command failed: {error_msg}")
    
    def search_repositories(
        self, 
        query: str, 
        limit: int = 20,
        sort: Optional[str] = "stars",
        language: Optional[str] = None,
        topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for repositories matching query."""
        # Build command arguments
        args = ["search", "repos", query, "--json", 
                "fullName,description,stargazersCount,forksCount,updatedAt,url,language"]
        
        if limit:
            args.extend(["--limit", str(limit)])
        if sort:
            args.extend(["--sort", sort])
        if language:
            args.extend(["--language", language])
        if topic:
            args.extend(["--topic", topic])
            
        # Execute command
        output = self.run_command(args)
        return json.loads(output)
    
    def get_repository(self, repo_name: str) -> Dict[str, Any]:
        """Get detailed information about a repository."""
        # Get the basic repository info
        args = ["repo", "view", repo_name, "--json", 
                "nameWithOwner,description,stargazerCount,forkCount,updatedAt,url,primaryLanguage"]
        
        # Execute command
        output = self.run_command(args)
        repo_data = json.loads(output)
        
        # Get the README separately using gh api
        try:
            readme_content = self.run_command([
                "api", 
                f"repos/{repo_name}/readme", 
                "--jq", ".content"
            ])
            import base64
            if readme_content:
                # GitHub API returns base64 encoded content
                readme_text = base64.b64decode(readme_content).decode('utf-8')
                repo_data["readme"] = {"text": readme_text}
        except Exception:
            # README might not exist
            repo_data["readme"] = {"text": "No README available."}
            
        return repo_data
    
    def search_code(
        self, 
        query: str, 
        limit: int = 20, 
        language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for code matching query."""
        # Build command arguments
        args = ["search", "code", query, "--json", 
                "repository,path,textMatches"]
        
        if limit:
            args.extend(["--limit", str(limit)])
        if language:
            args.extend(["--language", language])
            
        # Execute command
        output = self.run_command(args)
        return json.loads(output)
    
    def create_gist(
        self, 
        file_path: str,
        description: Optional[str] = None,
        public: bool = False
    ) -> str:
        """Create a gist from a file."""
        args = ["gist", "create"]
        
        if description:
            args.extend(["--desc", description])
        
        if not public:
            args.append("--secret")
            
        args.append(file_path)
        
        # Execute command
        return self.run_command(args)
    
    def open_in_browser(self, repo_name: str) -> None:
        """Open a repository in the web browser."""
        self.run_command(["repo", "view", repo_name, "--web"])
        
    def clone_repository(self, repo_name: str, directory: Optional[str] = None) -> str:
        """Clone a repository."""
        args = ["repo", "clone", repo_name]
        
        if directory:
            args.append(directory)
            
        return self.run_command(args)