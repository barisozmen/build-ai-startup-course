# Task 2: SSH into DigitalOcean Droplet

## Objective
Securely connect to your DigitalOcean Droplet using SSH.

## Prerequisites
- Active DigitalOcean Droplet
- Terminal application:
  - Terminal or iTerm2 (macOS/Linux)
  - PowerShell or Windows Terminal (Windows)
  - PuTTY (alternative for Windows)
- SSH key (if you selected SSH authentication)

[What is SSH?](https://chatgpt.com/share/6826ede6-f3ec-8010-8059-5b3e83ee12da)


## Steps

### 1. Connect your droplet via SSH

#### First option: Use SSH key authentication
If you chose SSH key authentication during Droplet creation:
1. Open your terminal application
2. Make sure your private key has the correct permissions:
   ```
   chmod 600 ~/.ssh/your_private_key
   ```
3. Connect using the key:
   ```
   ssh -i ~/.ssh/your_private_key root@your_droplet_ip
   ```

#### Second option: Use password authentication
If you chose password authentication during Droplet creation:

1. Open your terminal application
2. Use the SSH command with your Droplet's IP address:
   ```
   ssh root@your_droplet_ip
   ```
3. Enter the password you created when setting up the Droplet


### 3. Basic Server Exploration
Once connected, explore the server with these commands:
1. Check system information: `uname -a`
2. View disk space: `df -h`
3. Check memory usage: `free -m`
4. List running processes: `top` (press 'q' to exit)
More exploration commands at https://bozmen.io/discovering-a-new-linux-machine

## Expected Outcome
Successful secure SSH connection to your DigitalOcean Droplet.

## Troubleshooting
- **Connection refused error**: Wait a few minutes for the Droplet to initialize or check if the IP address is correct
- **Permission denied error**: Ensure your SSH key or password is correct
- **SSH key issues**: Verify key permissions (private key should be `chmod 600`)

## Notes
- Using SSH keys is more secure than password authentication 