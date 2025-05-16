# Terminal Commands by Category

## System Management

### Package Management
```bash
sudo apt update                      # Update package lists
sudo apt upgrade -y                  # Upgrade installed packages
sudo apt install [package] -y        # Install packages (python3, nginx, etc.)
```

### Service Management
```bash
sudo systemctl status nginx          # Check service status
sudo systemctl start nginx           # Start a service
sudo systemctl restart nginx         # Restart a service
sudo systemctl reload nginx          # Reload service configuration
sudo systemctl enable gunicorn       # Enable service to start at boot
sudo journalctl -u gunicorn          # View service logs
```

### Firewall Management
```bash
sudo ufw allow 8000                  # Allow traffic on port 8000
sudo ufw allow 'Nginx HTTP'          # Allow Nginx HTTP traffic
sudo ufw enable                      # Enable firewall
sudo ufw status                      # Check firewall status
```

## SSH & Remote Access

```bash
ssh root@your_droplet_ip                      # Connect to server via SSH
ssh -i ~/.ssh/your_private_key root@your_droplet_ip  # SSH with key file
ssh -o ServerAliveInterval=60 root@your_droplet_ip   # SSH with keep-alive
chmod 600 ~/.ssh/your_private_key             # Set correct permissions for SSH key
scp -r ~/path/to/your/project root@your_droplet_ip:/var/www/.  # Copy files to server
```

## File & Directory Operations

```bash
mkdir -p ~/hello-world                # Create directory (with parents)
echo "content" > ~/hello-world/index.html  # Create file with content
nano [filename]                       # Edit file with nano editor
cat [filename]                        # Display file contents
chmod +x deploy.sh                    # Make script executable
```

## Web Server & Networking

```bash
python3 -m http.server 8000           # Start simple Python web server
curl ifconfig.me                      # Get public IP address
nslookup yourdomain.com               # DNS lookup
traceroute yourdomain.com             # Trace route to domain
nginx -t                              # Test Nginx configuration
```

## Python & Django

```bash
python3 -m venv venv                  # Create virtual environment
source venv/bin/activate              # Activate virtual environment
pip install django gunicorn           # Install Python packages
python -m django --version            # Check Django version
django-admin startproject my_project . # Create Django project
python manage.py startapp app_name    # Create Django app
python manage.py migrate              # Run database migrations
python manage.py makemigrations       # Create migration files
python manage.py runserver 0.0.0.0:8000  # Run Django development server
gunicorn --bind 0.0.0.0:8000 my_project.wsgi  # Run Gunicorn WSGI server
```

## Node.js & PM2

```bash
sudo npm install pm2 -g               # Install PM2 globally
pm2 --version                         # Check PM2 version
pm2 start ecosystem.config.js         # Start app with PM2
pm2 status                            # Check PM2 process status
pm2 logs django_app                   # View PM2 application logs
pm2 restart django_app                # Restart PM2 process
pm2 stop django_app                   # Stop PM2 process
pm2 delete django_app                 # Delete PM2 process
pm2 monit                             # Monitor CPU/memory usage
pm2 startup                           # Generate PM2 startup script
pm2 save                              # Save current PM2 process list
```

## SSL/HTTPS

```bash
sudo apt install certbot python3-certbot-nginx -y  # Install Certbot
sudo certbot --nginx                  # Obtain and install SSL certificate
```

## Disk & System Information

```bash
df -h                                 # View disk space
free -m                               # Check memory usage
top                                   # List running processes
uname -a                              # Check system information
```
