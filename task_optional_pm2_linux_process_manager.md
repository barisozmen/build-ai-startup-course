# Task: PM2 Process Manager Setup for Linux

## Objective
Install and configure PM2 (Process Manager 2) to ensure your AI application runs continuously, automatically restarts after crashes, and starts on system boot.

## Prerequisites
- SSH access to your DigitalOcean Droplet
- Node.js and npm installed
- Django application set up and running

## Steps

### 1. Install Node.js and npm (if not already installed)

1. Connect to your Droplet via SSH:
   ```
   ssh root@your_droplet_ip
   ```

2. Update package lists:
   ```
   sudo apt update
   ```

3. Install Node.js and npm:
   ```
   sudo apt install nodejs npm -y
   ```

4. Verify installation:
   ```
   nodejs --version
   npm --version
   ```

### 2. Install PM2 Globally

1. Install PM2 using npm:
   ```
   sudo npm install pm2 -g
   ```

2. Verify PM2 installation:
   ```
   pm2 --version
   ```

### 3. Configure PM2 for Your Django Application

1. Navigate to your Django project directory:
   ```
   cd ~/django_project
   ```

2. Create a PM2 ecosystem configuration file:
   ```
   nano ecosystem.config.js
   ```

3. Add the following configuration:
   ```javascript
   module.exports = {
     apps: [{
       name: "django_app",
       script: "venv/bin/gunicorn",
       args: "ai_app.wsgi:application --bind 0.0.0.0:8000",
       interpreter: "none",
       watch: false,
       instances: "1",
       autorestart: true,
       max_memory_restart: "500M",
       env: {
         DJANGO_SETTINGS_MODULE: "ai_app.settings"
       }
     }]
   };
   ```

### 4. Start Your Application with PM2

1. Start your application using the ecosystem file:
   ```
   pm2 start ecosystem.config.js
   ```

2. Check the status of your application:
   ```
   pm2 status
   ```

3. View application logs:
   ```
   pm2 logs django_app
   ```

### 5. Configure PM2 to Start on System Boot

1. Generate startup script:
   ```
   pm2 startup
   ```

2. This will output a command that you need to run. Copy and execute that command.

3. Save the current PM2 process list:
   ```
   pm2 save
   ```

### 6. Basic PM2 Commands

1. Restart your application:
   ```
   pm2 restart django_app
   ```

2. Stop your application:
   ```
   pm2 stop django_app
   ```

3. Delete your application from PM2:
   ```
   pm2 delete django_app
   ```

4. Monitor CPU and memory usage:
   ```
   pm2 monit
   ```

### 7. Update Nginx Configuration

1. Update your Nginx configuration to proxy to the PM2-managed Gunicorn:
   ```
   sudo nano /etc/nginx/sites-available/ai-app
   ```

2. Modify the location block:
   ```
   location / {
       proxy_pass http://127.0.0.1:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   ```

3. Test and reload Nginx:
   ```
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### 8. Create a Deployment Script

1. Create a deployment script for easy updates:
   ```
   nano deploy.sh
   ```

2. Add the following content:
   ```bash
   #!/bin/bash
   
   echo "Pulling latest changes..."
   git pull
   
   echo "Installing dependencies..."
   source venv/bin/activate
   pip install -r requirements.txt
   
   echo "Running migrations..."
   python manage.py migrate
   
   echo "Collecting static files..."
   python manage.py collectstatic --noinput
   
   echo "Restarting application..."
   pm2 restart django_app
   
   echo "Deployment complete!"
   ```

3. Make the script executable:
   ```
   chmod +x deploy.sh
   ```

## Expected Outcome
Your Django application will run continuously under PM2 supervision, automatically restart after crashes, and start automatically when the server boots.

## Troubleshooting

- **Application not starting**: Check PM2 logs with `pm2 logs django_app`
- **PM2 not starting on boot**: Verify startup script with `pm2 startup` and `pm2 save`
- **Memory issues**: Adjust `max_memory_restart` in ecosystem.config.js
- **Permission problems**: Ensure proper file permissions for your application
- **Nginx proxy errors**: Check Nginx error logs with `sudo tail -f /var/log/nginx/error.log`

## Notes

- PM2 is a powerful process manager with many features beyond what's covered here
- For production environments, consider adjusting the number of instances based on your server's CPU cores
- PM2 can be configured to send email alerts when your application crashes
- The ecosystem.config.js file can be expanded to include multiple applications
- Consider using PM2's built-in load balancer for better performance by setting `instances: "max"`
- PM2 provides a web-based dashboard called PM2 Plus for monitoring (paid service)
