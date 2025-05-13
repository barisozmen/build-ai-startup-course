# Build an AI Startup

<div align="center">
<img src="https://cdn.worldvectorlogo.com/logos/elastic-stack.svg" width="200" alt="logo">
</div>


This repository contains a step-by-step guide to building an AI startup, from setting up cloud infrastructure to deploying a functional AI-powered web application.

Prior to starting tasks, you can read [these slides](https://docs.google.com/presentation/d/15o64i37sIBoT4gUDC6-S_pjh0oApq129NZFnmFcEZ68/edit?usp=sharing) that gives a background for choices of tech stack and methods chosen.


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

## Project Overview

This project guides you through building a complete AI-powered web application from scratch. You'll learn how to:

- Set up and manage cloud infrastructure
- Configure web servers and security
- Build a Django web application
- Integrate with AI APIs for image style transfer
- Integrate with OpenAI API for chat application
- Implement user authentication and profiles
- Set up custom domain names
- Process subscription payments
- Deploy a production-ready application

## Getting Started

Follow each task in sequence. Each task file contains detailed instructions, prerequisites, and troubleshooting tips to help you succeed.

## Technologies Used

- **Cloud Infrastructure**: DigitalOcean
- **Web Server**: Nginx
- **Backend Framework**: Django
- **Image Style Transfer**: DeepAI Style Transfer API
- **Chat Application**: OpenAI API
- **Deployment**: Gunicorn WSGI server
- **Domain Registration**: Namecheap
- **Payment Processing**: Stripe
- **Logging**: Logfire
- **Process Manager**: PM2

## Requirements
- Basic understanding of command line and SSH
- Familiarity with Python programming
- A credit/debit card for DigitalOcean account verification, domain purchase, and Stripe setup

## Support

If you encounter any issues while following these tasks, refer to the troubleshooting sections in each task file or consult the official documentation for the relevant technologies.
