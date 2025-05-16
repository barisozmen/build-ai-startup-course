# Build Your AI Startup From Scratch 🚀 

<div align="center">
<img src="assets/lego-builder.png" width="400" alt="frontpic">
</div>




This repository contains a step-by-step guide to building an AI startup, from setting up cloud infrastructure to deploying a functional AI-powered web application.

Prior to starting tasks, you can read [these slides](https://docs.google.com/presentation/d/15o64i37sIBoT4gUDC6-S_pjh0oApq129NZFnmFcEZ68/edit?usp=sharing) that gives a background for choices of tech stack and the methods.


## Tasks

1. **Create Digital Ocean Droplet** - Set up a cloud server to host your AI application.
2. **SSH into DigitalOcean Droplet** - Securely connect to your cloud server via SSH.
3. **Display "Hello World" in a local browser** - Create a basic web server to verify your remote server is working.
4. **Nginx Web Server Setup** - Install and configure Nginx as a proper web server for your application.
5. **Django Setup** - Install and configure Django to create a web application framework.
6. **Ghibli Style Image Conversion App** - Build a web application that transforms user images into Studio Ghibli art style.
   - **Chat Application with OpenAI API** - Optionally, add a chat application that integrates with OpenAI's API to provide intelligent responses to user queries.
7. **User System and Authentication** - Set up user registration, login, and profile management.

Optionals:
- **Custom Domain Setup** - Purchase a domain name from Namecheap and connect it to your application.
- **Stripe Payment System** - Subscription payments for premium features.
- **Logging with Logfire** - Set up structured loggings
- **PM2 Process Manager** - Linux process manager setup, for keeping the app running robustly

## What you will learn?

How to:
- Set up and manage cloud infrastructure
- Configure web servers and security
- Build a Django web application
- Integrate with AI APIs for image style transfer
- Integrate with OpenAI API for chat application
- Implement user authentication and profiles
- Set up custom domain names
- Process subscription payments
- Deploy a production-ready application
- Keep the app running robustly

## Technologies Used

- **Cloud Infrastructure**: [DigitalOcean](https://www.digitalocean.com/) ([primer](https://chatgpt.com/share/6826cf79-d574-8010-9862-60782fd4f784))
- **Web Server**: [Nginx](https://nginx.org/) ([primer](https://chatgpt.com/share/6826d61a-3088-8010-8dcf-18eeb5887cea))
- **Backend Framework**: [Django](https://www.djangoproject.com/) ([primer](https://chatgpt.com/share/6826cf56-acec-8010-803c-f7c07cabd481))
- **Frontend**: Django Templates + HTML/CSS/JS
- **Image Style Transfer**: [DeepAI Style Transfer API](https://deepai.org/machine-learning-model/fast-style-transfer)
- **Chat Application**: [OpenAI API](https://openai.com/api/)
- **Deployment**: [Gunicorn](https://gunicorn.org/) WSGI server
- **Domain Registration**: [Namecheap](https://www.namecheap.com/)
- **Payment Processing**: [Stripe](https://stripe.com/) ([primer](https://chatgpt.com/share/6826d6e7-6708-8010-81f2-794542d2e225))
- **Logging**: [Logfire](https://logfire.dev/) ([primer](https://chatgpt.com/share/6826d6c0-d33c-8010-a241-75eadb041494))
- **Process Manager**: [PM2](https://pm2.keymetrics.io/) ([primer](https://chatgpt.com/share/6826d677-8774-8010-ad1c-3fe2cf81cde4))

## Prerequisites
- Basic understanding of command line and SSH
- Familiarity with Python programming
- A credit/debit card for DigitalOcean account verification, domain purchase, and Stripe setup

## Support

If you encounter any issues while following these tasks, refer to the troubleshooting sections in each task file or consult the official documentation for the relevant technologies.
