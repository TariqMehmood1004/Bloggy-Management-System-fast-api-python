
## Bloggy Management System | FastAPIs | Python | Docker | AWS
Bloggy is a blog management system that allows users to create, update, and delete blogs. It is a simple and easy-to-use platform that allows users to create and manage their own blogs. The system is built using FastAPI, Python, Docker, and AWS. Authroization is done using JWT tokens. The system is deployed on AWS using Docker Compose. The system is deployed on AWS using Docker Compose. 

---

## Requirements 
### 1. FastAPI Application: 
* Create a FastAPI application that supports CRUD (Create, Read, Update, Delete) operations for blog posts. 
* Use Pydantic models for data validation. 

### 2. PostgreSQL Integration: 
* Connect the FastAPI application to a PostgreSQL database. 
* Define database models for blog posts and users. 

### 3. Authentication: 
* Implement user registration and login functionality using OAuth2 with JWT. 
* Protect CRUD operations so that only authenticated users can perform these actions. 

### 4. Caching: 
* Implement caching for read operations using a caching service like Redis. 

### 5. Docker Deployment: 
* Containerize the application using Docker. 
* Use Docker Compose to manage multiple containers (e.g., FastAPI app, PostgreSQL, 
Redis). 

### 6. Nginx Configuration: 
* Configure Nginx as a reverse proxy to serve the FastAPI application. 

### 7. Unit Testing: 
* Write unit tests for the application using Pytest. 
* Ensure tests cover authentication, CRUD operations, and caching functionality. 

---

### Step 1: 
Run the following command to start the FastAPI server
```
docker compose up --build
```

```
http://127.0.0.1:8000/docs
```

### Step 2: 
Authorize the user on swagger top-right **> Authorize**

### Step 3: 
Add the username and password to the fields under **> Authorize**

### Step 4: 
User will be logged in successfully

### Step 5: 
Click on **> POST /login** to get the access tokens

### Step 6: 
Once tokens are received, user will be able to access protected routes

### Step 7: 
Click on **> GET /users/me** to get the current user details

---

## Swagger Routes:
### 1. User Routes:
    * `POST` /register
    * `POST` /login
    * `GET` /users/me
    * `PUT` /users/me/update
    * `DELETE` /users/me/delete
    * `DELETE` /users/delete/all
    * `DELETE` /users/delete/{user_id}
    * `GET` /users

### 2. Blog Routes:
    * `GET` /blogs - Get All Blogs
    * `POST` /blogs - Create Blog
    * `DELETE` /blogs/delete/all - Delete All Blogs By Authorized
    * `DELETE` /blogs/{blog_id} - Delete Blog By Authorized
    * `GET` /blogs/{blog_id} - Get Blog by ID
    * `PUT` /blogs/update/{blog_id} - Update Blog
    * `GET` /users/me/blogs - Get All Blogs By Current User

---
## Docker
### IMAGES
Docker images are a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.

### Build an Image from a Dockerfile
#### Build an Image from a Dockerfile without the cache
```
docker build -t <image_name> . –no-cache
```

#### List local images
```
docker images
```

#### Delete an Image
```
docker rmi <image_name>
```

#### Remove all unused images
```
docker image prune
```
---
## DOCKER HUB
Docker Hub is a service provided by Docker for finding and sharing container images with your team. Learn more and find images at https://hub.docker.com

### Login into Docker
```
docker login -u <username>
```

### Publish an image to Docker Hub
```
docker push <username>/<image_name>
```

### Search Hub for an image
```
docker search <image_name>
```

### Pull an image from a Docker Hub
```
docker pull <image_name>
```

---
## DOCKER COMPOSE
### Step 1:
docker compose up --build

### Step 2:
uvicorn blog_fast_api_python.main:app --host 0.0.0.0 --port 8000

### Step 3: No need to build this again
docker compose up

---

## Redis Server
When you run *`docker-compose up --build`* it will start the redis server automatically. Because we have defined it in the docker-compose.yml file.

### Stop Redis Server
```
docker-compose down
```

---

