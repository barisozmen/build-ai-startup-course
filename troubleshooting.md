# Troubleshooting Guide for AI Startup Project

This document provides solutions for common issues you might encounter. Use this as a reference when you get stuck on specific tasks.

## Table of Contents
- [Digital Ocean Droplet Setup](#digital-ocean-droplet-setup)
- [SSH Access](#ssh-access)
- [Web Server Setup](#web-server-setup)
- [Nginx Configuration](#nginx-configuration)
- [Remote Development Environment](#remote-development-environment)
- [Django Setup](#django-setup)
- [AI Image Generation App](#ai-image-generation-app)
- [User Authentication System](#user-authentication-system)
- [Optional Components](#optional-components)

## Digital Ocean Droplet Setup

### Cannot create a Droplet
- **Issue**: Creation process fails or times out
- **Solution**: 
  - Try a different browser or clear cache/cookies
  - Verify payment method is valid and has sufficient funds
  - Choose a different datacenter region if one is at capacity

### Account verification issues
- **Issue**: Cannot verify account with credit card
- **Solution**:
  - Ensure card details are entered correctly
  - Try a different card if available
  - Contact DigitalOcean support if problems persist

### Droplet not accessible after creation
- **Issue**: Cannot reach new Droplet via IP
- **Solutions**:
  - Wait 2-3 minutes for Droplet initialization to complete
  - Verify the Droplet is powered on in control panel
  - Check for any error messages in the console

## SSH Access

### Connection refused errors
- **Issue**: `ssh: connect to host <IP> port 22: Connection refused`
- **Solutions**:
  - Wait a few minutes for Droplet initialization
  - Verify your IP address is correct
  - Ensure you're not behind a firewall blocking port 22

### Permission denied errors
- **Issue**: `Permission denied (publickey)` or password rejection
- **Solutions**:
  - For SSH key: 
    ```
    chmod 600 ~/.ssh/your_private_key
    ```
  - Verify correct username (usually `root` for new Droplets)
  - Confirm password is correct (if using password authentication)
  - Check if the public key was properly added to the Droplet

### SSH key issues
- **Issue**: Cannot authenticate with SSH key
- **Solutions**:
  - Ensure you're specifying the correct private key:
    ```
    ssh -i ~/.ssh/your_private_key root@your_droplet_ip
    ```
  - Verify the key has correct permissions (should be 600)
  - Check if the key is in the expected format
  - Try regenerating and re-adding SSH keys

### Connection timeouts
- **Issue**: SSH sessions disconnect after inactivity
- **Solution**: Use ServerAliveInterval option:
  ```
  ssh -o ServerAliveInterval=60 root@your_droplet_ip
  ```
  Or add it to your SSH config file:
  ```
  Host *
    ServerAliveInterval 60
  ```

## Web Server Setup

### Python web server issues
- **Issue**: Python HTTP server won't start
- **Solutions**:
  - Verify Python is installed: `python3 --version`
  - Check if port 8000 is already in use: `netstat -tuln | grep 8000`
  - Try a different port if needed

### Cannot access web server in browser
- **Issue**: Browser can't connect to `http://<your_droplet_ip>:8000`
- **Solutions**:
  - Verify the Python server is running
  - Check firewall settings: `sudo ufw status`
  - Allow the port through the firewall: `sudo ufw allow 8000`
  - Ensure you're binding to 0.0.0.0, not just localhost: 
    ```
    python3 -m http.server 8000 --bind 0.0.0.0
    ```

### Server crashes or stops unexpectedly
- **Issue**: Web server terminates when SSH session closes
- **Solutions**:
  - best solution will be using PM2 to keep the server running after session closes (see [task for PM2](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_optional_pm2_linux_process_manager.md)).
  - Use `nohup` to keep the server running after session closes:
    ```
    nohup python3 -m http.server 8000 > server.log 2>&1 &
    ```
  - Consider using `screen` or `tmux` for persistent sessions
  - For Django development server:
    ```
    nohup python manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &
    ```

## Nginx Configuration

### Nginx won't start
- **Issue**: Nginx fails to start after installation
- **Solutions**:
  - Check for syntax errors in configuration:
    ```
    sudo nginx -t
    ```
  - Verify ports aren't in conflict: `netstat -tuln | grep 80`
  - Check error logs: `sudo tail -f /var/log/nginx/error.log`

### 404 Not Found errors
- **Issue**: Browser shows 404 when accessing site
- **Solutions**:
  - Verify file paths in server block configuration
  - Check if index.html exists in the specified root directory
  - Ensure symbolic links are created correctly:
    ```
    sudo ln -s /etc/nginx/sites-available/ai-app /etc/nginx/sites-enabled/
    ```

### Permission denied errors
- **Issue**: Nginx reports permission errors in logs
- **Solutions**:
  - Check ownership and permissions of web directories:
    ```
    sudo chown -R www-data:www-data /var/www/ai-app
    sudo chmod -R 755 /var/www/ai-app
    ```
  - Check SELinux status if applicable: `sestatus`

### Still seeing "Welcome to nginx" default page
- **Issue**: Default page shows instead of your custom page
- **Solutions**:
  - Ensure your server block is enabled
  - Remove or rename the default config:
    ```
    sudo rm /etc/nginx/sites-enabled/default
    ```
  - Reload Nginx: `sudo systemctl reload nginx`

## Remote Development Environment

### VS Code Remote SSH connection issues
- **Issue**: Cannot connect via VS Code Remote extension
- **Solutions**:
  - Verify SSH works from terminal first
  - Check Remote-SSH extension is installed
  - Check VS Code logs: View > Output > Remote-SSH
  - Try adding the host to ~/.ssh/config:
    ```
    Host ai-droplet
      HostName your_droplet_ip
      User root
      IdentityFile ~/.ssh/your_private_key
      ServerAliveInterval 60
    ```

### Cursor Remote Development connection issues
- **Issue**: Cannot connect via Cursor
- **Solutions**:
  - Ensure Cursor is up to date
  - Verify SSH access works from terminal
  - Try restarting Cursor
  - Check that the remote path exists and is correct

### File synchronization problems
- **Issue**: Files not syncing with rsync
- **Solutions**:
  - Verify rsync is installed on both systems
  - Check file permissions
  - Try with verbose option to see details:
    ```
    rsync -avz --exclude 'venv/' -e "ssh -i ~/.ssh/your_private_key" ./ root@your_droplet_ip:~/project/
    ```

### Git-based workflow issues
- **Issue**: Cannot push/pull from repository
- **Solutions**:
  - Check Git credentials are configured on both systems
  - Verify repository URL is correct
  - Ensure you have proper permissions for the repository
  - Check for SSH key or authentication issues

## Django Setup

### Django installation failures
- **Issue**: Cannot install Django in virtual environment
- **Solutions**:
  - Update pip: `pip install --upgrade pip`
  - Check Python version compatibility
  - Verify internet connectivity
  - Try with verbose output: `pip install django -v`

### Django migrations issues
- **Issue**: Migrations fail to apply
- **Solutions**:
  - Check database configuration in settings.py
  - Verify database user has proper permissions
  - For serious issues, you may need to reset migrations:
    ```
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" -delete
    python manage.py makemigrations
    python manage.py migrate
    ```

### Static files not loading
- **Issue**: CSS/JS files not appearing in browser
- **Solutions**:
  - Check STATIC_URL and STATIC_ROOT in settings.py
  - Run `python manage.py collectstatic`
  - Verify Nginx configuration for serving static files
  - Check file permissions for static directories

### Server starts but shows 500 errors
- **Issue**: Internal Server Error when accessing Django
- **Solutions**:
  - Check Django error logs
  - Verify DEBUG=True in settings.py during development
  - Check if database is properly configured
  - Make sure required environment variables are set

## AI Image Generation App

### API key issues
- **Issue**: Cannot connect to image generation API
- **Solutions**:
  - Verify API key is correct
  - Check if billing is set up for the service
  - Ensure the key is properly configured in settings
  - Try API request outside Django to isolate the issue

### Image upload/generation failures
- **Issue**: Images fail to upload or generate
- **Solutions**:
  - Check file permissions for media directory
  - Verify MEDIA_URL and MEDIA_ROOT settings
  - Increase Nginx upload size limit:
    ```
    client_max_body_size 10M;
    ```
  - Look for API-specific error messages

### Image display problems
- **Issue**: Generated images don't appear in gallery
- **Solutions**:
  - Check media file paths
  - Verify Nginx is configured to serve media files
  - Ensure database entries are created correctly
  - Check for file permission issues

### Prompt content policy violations
- **Issue**: API rejects prompts as inappropriate
- **Solutions**:
  - Review API provider's content policy
  - Implement content filtering on user prompts
  - Add error handling for rejected prompts

## User Authentication System

### Registration failures
- **Issue**: Users cannot register new accounts
- **Solutions**:
  - Check form validation errors
  - Verify password complexity requirements
  - Ensure username/email isn't already in use
  - Check Django logs for detailed error messages

### Login problems
- **Issue**: Users cannot log in after registration
- **Solutions**:
  - Verify login view and URL configuration
  - Check if user accounts are being properly activated
  - Reset user passwords manually if needed:
    ```
    python manage.py changepassword username
    ```
  - Check LOGIN_URL and LOGIN_REDIRECT_URL in settings

### Profile picture upload issues
- **Issue**: Profile pictures don't upload or display
- **Solutions**:
  - Check media file configuration
  - Verify form enctype is set to `multipart/form-data`
  - Check file size limits and permissions
  - Ensure ImageField is properly configured in model

### Permission and authorization issues
- **Issue**: Users accessing unauthorized content
- **Solutions**:
  - Verify view permissions and decorators
  - Check user authentication in templates
  - Ensure login_required decorator is applied where needed
  - Review queryset filters for user-specific content

## Optional Components

### Stripe Payment Integration
- **Issue**: Payments not processing
- **Solutions**:
  - Verify Stripe API keys (test vs. production)
  - Check webhook configuration
  - Ensure proper error handling in payment views
  - Look for detailed errors in Stripe dashboard

### Custom Domain Setup
- **Issue**: Domain not pointing to Droplet
- **Solutions**:
  - Verify DNS settings in Namecheap
  - Check DigitalOcean DNS configuration
  - Allow time for DNS propagation (24-48 hours)
  - Use `nslookup` or `dig` to troubleshoot DNS issues

### Email Notification Problems
- **Issue**: Emails not being sent
- **Solutions**:
  - Check email settings in settings.py
  - Verify SMTP credentials
  - For Gmail, ensure you're using an App Password
  - Try console email backend for testing

### PM2 Process Manager Issues
- **Issue**: Application not starting with PM2
- **Solutions**:
  - Check PM2 logs: `pm2 logs`
  - Verify ecosystem.config.js configuration
  - Ensure proper paths to virtual environment
  - Check if the application runs outside PM2

### Logfire Integration Problems
- **Issue**: Logs not appearing in Logfire dashboard
- **Solutions**:
  - Verify Logfire token is correct
  - Check internet connectivity from server
  - Ensure logfire library is properly initialized
  - Look for any rate limiting or quota issues

## General Troubleshooting Tips

1. **Check logs**: Always review relevant logs first:
   - Nginx: `/var/log/nginx/error.log`
   - Django: Console output or configured log files
   - System: `journalctl -xe`

2. **Test connectivity**:
   - `ping` to verify network access
   - `curl` or `wget` to test HTTP endpoints
   - `telnet <host> <port>` to check if ports are open

3. **Verify permissions**:
   - File permissions: `ls -la`
   - Directory ownership: `ls -ld /path/to/dir`
   - Fix common permission issues: `chmod +x script.sh`

4. **Resource constraints**:
   - Check disk space: `df -h`
   - Monitor memory usage: `free -m`
   - View CPU load: `top` or `htop`

5. **Isolate the problem**:
   - Test components individually
   - Create minimal reproduction cases
   - Temporarily disable features to narrow down issues


## Getting Help
If blocked, ask ChatGPT with a detailed description of the issue. If not solved, open a new issue on the repository for getting help from others. If still not solved, ask me directly.
