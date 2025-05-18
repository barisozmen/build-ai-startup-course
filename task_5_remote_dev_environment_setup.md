# Task 5: Remote Development Environment Setup

## Objective
Set up a remote development environment to efficiently work on your AI application hosted on the DigitalOcean Droplet directly from your local machine.

## Prerequisites
- Completed Task 2: SSH into DigitalOcean Droplet
- Basic understanding of SSH and remote development concepts
- Local development environment (VS Code, Cursor, or other IDE)


## Step 1: Set up your development tooling

#### Option 1: VS Code & Cursor Remote Development (Recommended)

1. Install Visual Studio Code on your local machine from [VS Code website](https://code.visualstudio.com/) or Cursor IDE from [Cursor website](https://www.cursor.com/)

2. Install the "Remote - SSH" extension:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
   - Search for "Remote - SSH"
   - Click "Install"

3. Configure SSH connection in VS Code:
   - Press F1 to open the command palette
   - Type "Remote-SSH: Connect to Host" and select it
   - Click "Add New SSH Host"
   - Enter: `ssh root@your_droplet_ip`
   - Select your SSH configuration file (usually `~/.ssh/config`)
   - Click "Connect" and enter your password or use SSH key authentication

4. Once connected, open your project folder:
   - Click "Open Folder" in VS Code
   - Navigate to your project directory (e.g., `/root/django_project`)
   - Start editing files directly on the remote server

#### Option 2: Cursor Remote Development

1. Install Cursor on your local machine from [Cursor website](https://www.cursor.com/)
2. Open Cursor and click on the "Remote" tab in the left sidebar
3. Click "Add New Remote" and enter your SSH connection details:
   - Host: `your_droplet_ip`
   - Username: `root`
   - Authentication: Choose SSH key or password
4. Connect to your remote server and open your project directory

### Option 3. Configure SSH for Convenience

1. Create an SSH config file on your local machine (if it doesn't exist):
   ```
   touch ~/.ssh/config
   chmod 600 ~/.ssh/config
   ```

2. Add your Droplet configuration to the SSH config file:
   ```
   nano ~/.ssh/config
   ```

3. Add the following configuration:
   ```
   Host ai-droplet
     HostName your_droplet_ip
     User root
     IdentityFile ~/.ssh/your_private_key
     ServerAliveInterval 60
   ```

4. Now you can connect using the shorthand name:
   ```
   ssh ai-droplet
   ```

### Option 4. Set Up File Synchronization

If you prefer to develop locally and sync files to the remote server:

1. Install rsync on your local machine (if not already installed):
   - **macOS/Linux**: Usually pre-installed, or use package manager
   - **Windows**: Install via WSL or use alternatives like WinSCP

2. Create a sync script in your local project directory:
   ```
   nano sync.sh
   ```

3. Add the following content:
   ```bash
   #!/bin/bash
   rsync -avz --exclude 'venv/' --exclude '*.pyc' --exclude '__pycache__/' \
   -e "ssh -i ~/.ssh/your_private_key" \
   ./ root@your_droplet_ip:~/django_project/
   ```

4. Make the script executable:
   ```
   chmod +x sync.sh
   ```

5. Run the script whenever you want to sync changes:
   ```
   ./sync.sh
   ```

### Option 5. Set Up Git-Based Workflow

1. Initialize a Git repository in your local project:
   ```
   git init
   ```

2. Create a `.gitignore` file:
   ```
   touch .gitignore
   ```

3. Add common Python/Django exclusions:
   ```
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   venv/
   ENV/
   
   # Django
   *.log
   local_settings.py
   db.sqlite3
   media/
   
   # IDE
   .idea/
   .vscode/
   ```

4. Set up a remote repository (GitHub, GitLab, etc.)

5. On your Droplet, clone the repository:
   ```
   cd ~
   git clone your_repository_url django_project
   ```

6. Configure your workflow:
   - Develop locally
   - Commit and push changes
   - SSH into your Droplet and pull changes
   - Restart services as needed

### Step 2: Configure Development Environment on the Droplet

1. Install development tools on the Droplet:
   ```
   sudo apt update
   sudo apt install -y python3-pip python3-dev python3-venv git
   ```

2. Set up a virtual environment (if not already done):
   ```
   cd ~/django_project
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Install additional development packages:
   ```
   pip install ipython django-debug-toolbar
   ```

### Step 3: Configure Django for Development

1. Update Django settings for development mode:
   ```
   nano ~/django_project/ai_app/settings.py
   ```

2. Add development-specific settings:
   ```python
   # Development settings
   DEBUG = True
   
   # Add debug toolbar
   if DEBUG:
       INSTALLED_APPS += ['debug_toolbar']
       MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
       INTERNAL_IPS = ['127.0.0.1']
   ```

## Expected Outcome
A fully configured remote development environment that allows you to efficiently develop your AI application directly on your DigitalOcean Droplet from your local machine.

## Troubleshooting

- **SSH Connection Issues**: Verify your SSH key permissions (should be 600) and ensure the Droplet's firewall allows SSH connections
- **File Synchronization Errors**: Check file permissions and ensure rsync is installed on both systems
- **IDE Connection Problems**: Verify that your remote development extension is properly configured
- **Git Workflow Issues**: Ensure you have proper Git credentials configured on both local and remote systems

## Notes

- Remote development eliminates the need to maintain separate development and production environments
- VS Code and Cursor provide the most seamless remote development experience
- For larger teams, a Git-based workflow may be more appropriate
- Consider setting up a staging environment for testing before deploying to production
- The rsync method is useful for quick file transfers but doesn't provide the full IDE integration experience
- Keep your SSH connection secure by using key-based authentication and considering tools like fail2ban for additional security
