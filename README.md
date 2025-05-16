# Build Your AI Startup From Scratch 🚀 

<div align="center">
<img src="assets/lego-builder.png" width="400" alt="frontpic">
</div>




This repository contains a step-by-step guide to building an AI startup, from setting up cloud infrastructure to deploying a functional AI-powered web application.

Prior to starting tasks, you can read [these slides](https://docs.google.com/presentation/d/15o64i37sIBoT4gUDC6-S_pjh0oApq129NZFnmFcEZ68/edit?usp=sharing) that gives a background for choices of tech stack and the methods.


## Tasks

1. [Task 1: Create Digital Ocean Droplet](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_1_digital_ocean_account.md) - Set up a cloud server to host your AI application.
2. [Task 2: SSH into DigitalOcean Droplet](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_2_ssh_into_digital_ocean_droplet.md) - Securely connect to your cloud server via SSH.
3. [Task 3: Display "Hello World" in a local browser](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_3_hello_world_in_local_browser.md) - Create a basic web server to verify your remote server is working.
4. [Task 4: Nginx Web Server Setup](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_4_nginx_setup.md) - Install and configure Nginx as a proper web server for your application.
5. [Task 5: Django Setup](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_5_django_setup.md) - Install and configure Django to create a web application framework.
6. [Task 6: Ghibli Style Image Conversion App](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_6_ghibli_style_image_conversion_app.md) - Build a web application that transforms user images into Studio Ghibli art style.
   - [Task 6b: Chat Application with OpenAI API](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_6b_chat_application_with_openai_api.md) - Optionally, add a chat application that integrates with OpenAI's API to provide intelligent responses to user queries.
7. [Task 7: User System and Authentication](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_7_user_system_and_authentication.md) - Set up user registration, login, and profile management.

Optionals:
- [Custom Domain Setup](https://github.com/barisozmen/build-ai-startup-course/blob/main/optional_task_custom_domain_setup.md) - Purchase a domain name from Namecheap and connect it to your application.
- [Stripe Payment System](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_optional_stripe_payment_system.md) - Subscription payments for premium features.
- [Logging with Logfire](https://github.com/barisozmen/build-ai-startup-course/blob/main/task_optional_logging_with_logfire.md) - Set up structured loggings
- [PM2 Process Manager](https://github.com/barisozmen/build-ai-startup-course/blob/main/optional_task_pm2_process_manager.md) - Linux process manager setup, for keeping the app running robustly

Other:
- [Terminal Commands](https://github.com/barisozmen/build-ai-startup-course/blob/main/terminal_commands.md)


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
