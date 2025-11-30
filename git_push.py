import subprocess
import sys

def run_git_command(cmd, description):
    """Run a git command and print the result"""
    print(f"\n{'='*50}")
    print(f"{description}...")
    print(f"Running: {' '.join(cmd)}")
    print('='*50)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            env={**subprocess.os.environ, 'GIT_PAGER': '', 'PAGER': ''}
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode != 0:
            print(f"Warning: Command returned exit code {result.returncode}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("\n🚀 Starting Git Push Process...")
    
    # Step 1: Resolve merge conflicts
    run_git_command(
        ['git', 'rm', '-f', 'hrmsproject/approval/__pycache__/urls.cpython-310.pyc'],
        "Step 1: Removing conflicted __pycache__ file (urls)"
    )
    
    run_git_command(
        ['git', 'rm', '-f', 'hrmsproject/approval/__pycache__/views.cpython-310.pyc'],
        "Step 2: Removing conflicted __pycache__ file (views)"
    )
    
    # Step 3: Stage all changes
    run_git_command(
        ['git', 'add', '-A'],
        "Step 3: Staging all changes"
    )
    
    # Step 4: Show status
    run_git_command(
        ['git', 'status', '--short'],
        "Step 4: Current status"
    )
    
    # Step 5: Commit
    success = run_git_command(
        ['git', 'commit', '-m', 'Restructure templates to app-level and update views'],
        "Step 5: Committing changes"
    )
    
    if not success:
        print("\n⚠️  Commit failed or nothing to commit. Check the status above.")
        response = input("\nContinue with push anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Step 6: Push
    success = run_git_command(
        ['git', 'push', 'origin', 'main'],
        "Step 6: Pushing to GitHub"
    )
    
    if success:
        print("\n✅ Success! Changes pushed to GitHub.")
    else:
        print("\n❌ Push failed. Please check the error messages above.")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()

