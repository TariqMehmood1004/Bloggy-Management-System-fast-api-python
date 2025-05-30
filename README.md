
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