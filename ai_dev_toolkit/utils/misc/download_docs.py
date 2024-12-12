import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

def is_valid_git_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def download_docs(
    repo_url: str, 
    directory: str, 
    include_files: Optional[List[str]] = None,
    exclude_files: Optional[List[str]] = None,
    cleanup: bool = True
) -> bool:
    if not is_valid_git_url(repo_url):
        raise ValueError(f"Invalid git URL: {repo_url}")
        
    if not directory:
        raise ValueError("Directory cannot be empty")
        
    if include_files and exclude_files:
        raise ValueError("Cannot specify both include_files and exclude_files")
    
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = Path(repo_name)
    
    try:
        if include_files is None and exclude_files is None:
            include_files = ["*.md"]
            
        find_command = ""
        if include_files:
            find_command = " -o ".join(f"-name '{ext}'" for ext in include_files)
            find_command = f"find . -type f \( {find_command} \)"
        elif exclude_files:
            find_command = " -o ".join(f"-name '{ext}'" for ext in exclude_files)
            find_command = f"find . -type f ! \( {find_command} \)"
        else:
            find_command = "find . -type f"
            
        commands = [
            f"git clone --depth 1 --filter=blob:none --sparse {repo_url}",
            f"cd {repo_name} && git sparse-checkout set {directory}",
            f"cd {repo_name}/{directory} && {find_command} > keep_files.txt",
            f"cd {repo_name}/{directory} && find . -type f ! -exec grep -Fxf keep_files.txt {{}} \; -delete",
            f"cd {repo_name}/{directory} && rm keep_files.txt"
        ]
        
        for cmd in commands:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            if result.stderr:
                print(f"Warning: {result.stderr}")
                
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}")
        print(f"Error output: {e.stderr}")
        if cleanup:
            cleanup_repo(repo_path)
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        if cleanup:
            cleanup_repo(repo_path)
        return False

def cleanup_repo(repo_path: Path) -> None:
    try:
        if repo_path.exists():
            shutil.rmtree(repo_path)
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    repo_url = "https://github.com/run-llama/llama_index.git"
    directory = "docs"
    success = download_docs(repo_url, directory, include_files=["*.md", "*.rst"])
    print(f"Download {'successful' if success else 'failed'}")