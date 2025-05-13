# Milestone 5: Setting Up Nginx Web Server

## Objective
Install and configure Nginx as a proper web server for our AI application.

#### What is Nginx?
nginx ("engine x") is an HTTP web server, reverse proxy, content cache, load balancer, TCP/UDP proxy server, and mail proxy server (ref: https://nginx.org/).

#### What is a web server?
A web server is a software application that handles HTTP requests and responses. It is responsible for serving web pages to clients.

#### What is a reverse proxy?
A reverse proxy is a server that sits between the client and the web server. It receives requests from the client and forwards them to the web server. The web server then sends the response back to the client.

#### What is a load balancer?
A load balancer is a server that distributes incoming application traffic across a group of backend servers, either for the purpose of improving performance, or to allow for greater scalability that can support larger traffic.



## Prerequisites
- SSH access to your DigitalOcean Droplet
- Basic understanding of web servers

## Steps

### 1. Install Nginx
1. Connect to your Droplet via SSH
2. Update package lists:
   ```
   sudo apt update
   ```
3. Install Nginx:
   ```
   sudo apt install nginx -y
   ```

### 2. Configure Firewall
1. Allow Nginx HTTP traffic through the firewall:
   ```
   sudo ufw allow 'Nginx HTTP'
   ```
2. Verify firewall status:
   ```
   sudo ufw status
   ```

### 3. Check Nginx Status
1. Verify that Nginx is running:
   ```
   sudo systemctl status nginx
   ```
   (Press 'q' to exit)
2. If not running, start Nginx:
   ```
   sudo systemctl start nginx
   ```

### 4. Access Default Nginx Page
1. Open a web browser on your local computer
2. Navigate to your Droplet's IP address: `http://your_droplet_ip`
3. You should see the default Nginx welcome page (that says "Welcome to nginx!")

### 5. Basic Nginx Configuration
1. Create a directory for your web content:
   ```
   sudo mkdir -p /var/www/ai-app
   ```
2. Create a basic HTML file:
   ```
   echo "<html><body><h1>AI App with Nginx</h1><p>Nginx is successfully serving this page!</p></body></html>" > /var/www/ai-app/index.html
   ```

### 6. Configure Nginx Server Block
1. Create a new server block configuration:
   ```
   sudo nano /etc/nginx/sites-available/ai-app
   ```
2. Add the following configuration:
   ```
   server {
       listen 80;
       server_name your_droplet_ip;
       
       location / {
           root /var/www/ai-app;
           index index.html;
           try_files $uri $uri/ =404;
       }
   }
   ```
3. Create a symbolic link to enable the site:
   ```
   sudo ln -s /etc/nginx/sites-available/ai-app /etc/nginx/sites-enabled/
   ```
4. Verify configuration syntax:
   ```
   sudo nginx -t
   ```
5. Reload Nginx:
   ```
   sudo systemctl reload nginx
   ```

For more details, see Nginx official guide: https://nginx.org/en/docs/beginners_guide.html


### 7. Test Your Configuration
1. Open a browser and navigate to `http://<your_droplet_ip>`
2. You should now see your custom HTML page

## Expected Outcome
Nginx properly installed and serving a custom HTML page.


## Troubleshooting
- **404 Not Found error**: Check your server block configuration and file paths
- **Permission denied error**: Verify ownership and permissions on your web directory
- **"Welcome to nginx" still shows**: Make sure your server block is enabled and Nginx was reloaded

## Notes
- Nginx is a powerful web server that will handle client requests for our AI application
- This basic setup will be expanded in later milestones 