# Ez-Pizza

A web application for shopping for and placing orders for pizza.

## Project Description

This web application lets users place pizza orders online, receive email confimation for their placed orders, and track their orders' status. The backend is built using the Django framework, relying on its customizable features to design an admin and authentication system. For data storage, a postgresql database connection is integrated for management of menu items, shopping cart items and placed orders.  The dynamic frontend ui relies on the React library, bootstrap, and django templates. The menu items in the app follow that of [Pinocchio's Pizza and Subs](https://www.pinocchiospizza.net/menu.html).

### Technology used
| Technology  |       Version    |      Utility    |
|-------------|------------------|-----------------|
|    Django   |  v3.2.13         | Python based web-framework|
|   Postgres  | v14.0            | SQL based Relational Database Management System (RDMS)|
| Psycopg2    |     v2.9.1       | A PostgreSQL database adapter for Python web apps |
| React       |     v17.0.2      | Javascript-based library for frontend ui design|
| Cloudinary  |     v1.29.0      | A python library that facilitates access and storage of media files via connection to the Cloudinary Cloud Service. |


## Installation and Setup


1. Launch your terminal.
2. Create a new folder and navigate to it.
   ```
    mkdir ez_pizza
    cd ez_pizza
   ```
3. Clone this github repository here: https://github.com/ThatDudeJude/Ez-Pizza.git
   `
4. Ensure that [python](https://www.python.org) version v3.8+ and pip is installed in your computer.
5. Install a postgres server for your OS ([more info here](https://www.postgres.org/download)) if not installed. For windows users, you can add psql.exe to path.
6. Create a new virtual environment and activate it .For Linux and Mac OS run `python3 -m venv venv && ./venv/bin/activate` . For Windows cmd.exe run `c:\>c:\Python38\python -m venv venv && venv/SCRIPTS/activate.bat` .
7. Install a postgres server for your OS if not installed ([more info here](https://www.postgres.org/download)). 
8. Install all required libraries. 
   ```
   python3 -m pip install -r requirements.txt
   ```
9. To use the cloudinary service, create a cloudinary account [here](https://www.cloudinary.com/). Create a folder for storing assets with the folder structure ``ezpizza/users/avatars/`` (you can follow  [this](https://www.cloudinary.com/documentation/dam_folders_collections_sharing#create_folders) cloudinary guide). Upload a [default avatar](https://www.freepik.com/free-photos-vectors/user-avatar) jpg image to that folder and name it __default_avatar.jpg__.
10. User your cloudinary **cloudname**, **api key**, and **api secret** from your cloudinary account dashboard. Set the respective environment variables (preferably inside a .env file at the project's root level)
```
    CLOUD_NAME=[cloudname]
    API_KEY=[api_key]
    API_SECRET=[api_secret]
```
11.   Set up an smtp service, preferrably [gmail's smtp](https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab). Add the following variables to your environment
```
    DEFAULT_FROM_EMAIL=[youraccount@gmail.com]
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_HOST_USER=[youraccount@gmail.com]
    EMAIL_HOST_PASSWORD=[your smtp service account password]        
```
12.   Open a new terminal and create a postgres database for development and testing purposes. 

For Mac and Linux users, run :
```    
    sudo su postgres
    psql postgres
    \! hostname
```

For Windows users, run:
```
    psql -U postgres    
    \! hostname
```
You need to create a role and assign the necessary priviledges
```    
    CREATE USER ez_pizza with password 'ez_pizza_password';        
    CREATE DATABASE ez_pizza_db;
    GRANT ALL PRIVILEDGES ON DATABASE ez_pizza_db TO ez_pizza;
    \connect ez_pizza_db
    \conninfo    
    \q
```
   
Now set the environment variables using information from hostname, the ez_pizza password, and the database's `\conninfo` output.
   ```
   DATABASE_URL=postgres://USERNAME:PASSWORD@HOSTNAME:PORT/ezpizza_db   
   ``` 
13.  Add a secret key for the Django app. To generate a secret key, type in ``python3 -c "import secrets; print(secrets.hex_token());" `` and use the output as the secret key.
```
    SECRET_KEY=[secret_key]        
    
```
To launch the django server, run ``python3 manage.py runserver`` and navigate to http://127.0.0.1:8000/ to view the application

## Tests

To run the tests make sure to press Ctrl + C to stop the server first and set the environment variable
```
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
For both e2e and unit tests, run
```
    python manage.py test
```

## Screenshots and visuals
* Login 
![Login Demo](/static/assets/Login.gif)
* Menu
![Menu Demo](/static/assets/Menu.gif)
* Shop
![Shop Demo](/static/assets/Shop.gif)
* Order
![Order Demo](/static/assets/Order.gif)

## Contributing
Want to contribute? See contributing guidelines [here](/CONTRIBUTING.md).

## Codebeat

[![codebeat badge](https://codebeat.co/badges/f49762c5-7506-446a-b738-fe7f9fb8bc28)](https://codebeat.co/a/thatdudejude/projects/github-com-thatdudejude-bibliophiliac-profile_branch_final)

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE.txt)