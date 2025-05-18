# Task: Custom Domain Setup with Namecheap and DigitalOcean

## Objective
Purchase a domain name from Namecheap and connect it to your DigitalOcean droplet to make your AI application accessible via a professional domain name instead of an IP address.

## Prerequisites
- Active DigitalOcean droplet with your AI application running
- Credit/debit card for domain purchase
- Basic understanding of DNS concepts

## Steps

### 1. Purchase a Domain from Namecheap

1. Visit [Namecheap](https://www.namecheap.com/)
2. Use the search bar to find an available domain name for your AI application
3. Select a domain name that is appropriate for your application
4. Add the domain to your cart and proceed to checkout
5. Pay for your domain

[What is namecheap and how does it work?](https://chatgpt.com/share/682978c2-5068-8010-a55c-a7f7057f7148)

### 2. Connect Domain to DigitalOcean

1. Go to [DigitalOcean](https://digitalocean.com) and log in to your account
2. Click "Add a domain" to your droplet
   ![](assets/media/DomainregisteringtoDigitalOceandroplet.nginxnamecheap/media/image3.png)
3. If needed, add another alias to the domain with the appropriate settings:
   ![](assets/media/DomainregisteringtoDigitalOceandroplet.nginxnamecheap/media/image2.png)

### 3. Configure Namecheap DNS Settings

1. Go to [Namecheap](https://namecheap.com) and log in to your account
2. Find your domain in your account dashboard
3. Set nameservers to "Custom DNS" with DigitalOcean's nameservers as described in [this DigitalOcean blogpost](https://docs.digitalocean.com/products/networking/dns/getting-started/dns-registrars/)
   ![](assets/media/DomainregisteringtoDigitalOceandroplet.nginxnamecheap/media/image1.png)
4. Wait for DNS propagation (can take 1-48 hours)
5. Test if propagation is complete by:
   - Pinging the domain from your browser
   - Using `nslookup yourdomain.com` command
   
   Example:
   ```
   root@ubuntu-s-1vcpu-2gb-nyc3-01:~# nslookup memsearch.ai
   Server: 127.0.0.53
   Address: 127.0.0.53#53
   
   Non-authoritative answer:
   Name: memsearch.ai
   Address: 64.225.56.62
   ```
   
   The address should match your droplet's IP
   
   For more detailed information:
   ```
   $ traceroute yourdomain.com
   ```

### 4. Configure Nginx on Your Droplet

1. SSH into your droplet:
   ```
   $ ssh -o ServerAliveInterval=60 root@your_droplet_ip
   ```

2. Navigate to the Nginx configuration directory:
   ```
   $ cd /etc/nginx/sites-enabled
   ```

3. Add a new server block to your Nginx configuration file:
   ```
   server {
       server_name www.yourdomain.com yourdomain.com;
       
       location / {
           proxy_pass http://localhost:5000;  # Change port as needed
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. Test the Nginx configuration for syntax errors:
   ```
   $ sudo nginx -t
   ```

5. Restart Nginx to apply changes:
   ```
   $ sudo systemctl restart nginx
   ```


### 5. Set Up SSL/HTTPS with Let's Encrypt

1. Install Certbot:
   ```
   $ sudo apt update
   $ sudo apt install certbot python3-certbot-nginx -y
   ```

2. Obtain and install SSL certificate:
   ```
   $ sudo certbot --nginx
   ```

3. Follow the prompts to complete the SSL setup
4. Certbot will automatically update your Nginx configuration

### 7. Add Subdomain (Optional)

1. Add a new A record from the DigitalOcean control panel:
   ![](assets/media/DomainregisteringtoDigitalOceandroplet.nginxnamecheap/media/image4.png)

2. Check if DNS has propagated using DigitalOcean's DNS tool:
   [https://www.digitalocean.com/community/tools/dns](https://www.digitalocean.com/community/tools/dns)

## Expected Outcome
Your application will be accessible via your custom domain name (https://yourdomain.com) instead of the DigitalOcean IP address.

## Troubleshooting
- **DNS not resolving**: Check your Namecheap DNS settings and ensure propagation time has passed
- **Nginx not serving your domain**: Verify server_name directive and Nginx configuration
- **SSL certificate issues**: Check Certbot logs and ensure your domain is correctly pointing to your server
- **Application errors**: Verify your application is running on the correct port

## Notes
- Domain registration typically costs $10-20 per year depending on the TLD
- DNS changes can take up to 48 hours to fully propagate worldwide
- Using HTTPS (SSL) improves security and user trust in your application
- PM2 ensures your application restarts automatically if the server reboots
