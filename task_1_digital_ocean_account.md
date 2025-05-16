# Task 1: Create Digital Ocean Droplet

## Objective
Create and configure a DigitalOcean droplet that will host our AI application.

## Prerequisites
- Valid email address
- Credit/debit card for account verification
- Basic understanding of cloud hosting concepts

## Steps

### 1. Sign Up for DigitalOcean
1. Google "digital ocean 200 usd", and click the first sponsored link
2. Follow the Digital Ocean sign up process, and claim your $200 credit

### 2. Create a New DigitalOcean Droplet
1. Log in to your DigitalOcean account
2. Click "Create" > "Droplets" in the top navigation
3. Choose an image: Ubuntu 22.04 LTS (or latest LTS version)
4. Select a plan:
   - Basic shared CPU
   - Regular Intel (cheapest option is fine for this course)
   - $5/mo or $10/mo plan should be sufficient
5. Choose a datacenter region closest to your target users
6. Authentication:
   - Choose SSH keys or Password
   - If using SSH keys, follow the instructions to add your public key
7. Add a hostname (e.g., "ai-app-droplet")
8. Click "Create Droplet"

### 3. Configure your droplet
1. Note your Droplet's IP address from the DigitalOcean control panel
2. Wait a minute or two for the Droplet to fully initialize


## Expected Outcome
1. A functional DigitalOcean account
2. A running Droplet (running Ubuntu) with an assigned IP address.

## Notes
- The smallest Droplet size is usually sufficient for learning purposes
- You can resize your Droplet later if needed
- DigitalOcean charges hourly up to a monthly maximum, so you only pay for what you use 
- Consider enabling email notifications for billing alerts 
