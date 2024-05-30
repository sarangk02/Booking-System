
# API Odyssey: Navigating Backend and Deployment Frontiers

This project is a Django Rest API for a Slot Booking System aimed at enhancing operational efficiency. It utilizes JWT Token authentication to ensure secure access to the system. PostgreSQL is employed as the robust backend database.

## Features

- **JWT Token authentication** for secure access
- **PostgreSQL** backend for efficient data management, particularly for image data
- Containerized application with **Docker** for seamless deployment
- Custom DjangoREST, PostgreSQL, and Nginx images integrated for deployment
- **NGINX** and **Gunicorn** used for effective request balancing
- **Caching** and **Reverse Proxy** concept employed for automated deployment process

## Project Setup

1. Clone the repository:

   ```shell
   git clone https://github.com/sarangk02/Booking-System.git
   ```

2. Start your docker daemon and run the command:
    ```shell
    docker compose up -d
    ```

3. Make django database migrations and create superuser named admin and enter your choice of password
    ```shell
    docker compose exec web ./setup.sh
    ```

4. Visit the localhost and you can see your website ready to access on [localhost](http://localhost:80) port 80 i.e. default port

5. You can view the documentation for [API Endpoints](https://www.postman.com/navigation-specialist-1976778/workspace/slotbookingsystem/documentation/28095221-30cc4e51-80f6-4dd0-83e5-5ce13c844ce6) created with Postman

## Support
For support, email sarang.kulkarni@somaiya.edu

***
[License](https://choosealicense.com/licenses/mit/)

[Don't Click Me🧐](https://www.youtube.com/watch?v=dQw4w9WgXcQ)