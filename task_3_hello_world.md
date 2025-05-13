# Task 4: Display "Hello World" in a Browser

## Objective
Set up a basic web server to display a "Hello World" message accessible via web browser from your local computer (e.g. your personal laptop).

## Prerequisites
- SSH access to your DigitalOcean Droplet
- Basic knowledge of terminal commands

## Steps

### 1. Update System Packages
1. Connect to your Droplet via SSH
2. Update package lists and upgrade installed packages:
   ```
   sudo apt update
   sudo apt upgrade -y
   ```

### 2. Install Python and Create a Simple Web Server
1. Install Python if not already available:
   ```
   sudo apt install python3 -y
   ```
2. Create a simple HTML file:
   ```
   mkdir -p ~/hello-world
   echo "<html><body><h1>Hello, World!</h1><p>My first AI app server is working!</p></body></html>" > ~/hello-world/index.html
   ```
3. Start a basic Python web server:
   ```
   cd ~/hello-world
   python3 -m http.server 8000
   ```

### 3. Configure Firewall to Allow Web Traffic
1. Allow HTTP traffic through the firewall:
   ```
   sudo ufw allow 8000
   sudo ufw enable
   ```
   (Enter 'y' when prompted)

### 4. Access Your Hello World Page
1. Find out your droplet's public IP address
   a. run following command in your droplet (when SSH'ed into it)
   ```
   curl ifconfig.me
   ```
   b. Find out your droplet's public IP address from DigitalOcean control panel
2. Open a web browser on your local computer
3. Navigate to: `http://<your_droplet_ip>:8000`
4. You should see the "Hello World" message. 

Congrats! You've just created a basic web server that can be viewed by anyone in the world!


## Expected Outcome
A basic web page displaying "Hello World" accessible via browser.

## Troubleshooting
- **Cannot access the page**: Ensure your firewall allows port 8000 traffic
- **Connection timed out**: Check if Python server is running and the IP address is correct
- **Python command not found**: Verify Python installation with `python3 --version`

## Notes
- This is a temporary web server for testing
- To stop the server, press Ctrl+C in the terminal
- In the next milestone, we'll set up a proper web server with Nginx 