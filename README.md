
# FastAPI - Blog System

### Step 1: 
Run the following command to start the FastAPI server
```
fastapi dev main.py
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

### Step 1:
docker build -t blog_fastapi_app .

### Step 2:
docker run -d -p 8000:8000 --name blog_fastapi_container blog_fastapi_app