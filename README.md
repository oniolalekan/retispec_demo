# retispec_demo

A patient can have zero or multiple acquisitions.
![uml_diagram](https://github.com/oniolalekan/retispec_demo/blob/main/uml_diagram.jpeg)

FastApi:
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.


SQLAlchemy is used as the Object Relational Mapper (ORM)

What is SQLAlchemy?
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. SQLAlchemy is a tool in the Object Relational Mapper (ORM) category of a tech stack. One major drawback of this ORM is that it doesn't capture updates to model's (table) properties. The table will have to be deleted before the column to be addded.


Pydantic is used for validation. It is, for example, used to validate that all of the right environment variables have been set.

# How to run the service?

# Step I: Install python dependencies
First install the dependencies which is in the requirements.txt file. It's better to wrap this in a Virtual Environment. 

# Step II: Download PgAdmin
pgAdmin is the most popular and feature rich Open Source administration and development platform for PostgreSQL, the most advanced Open Source database in the world.

# Step III: Create a database (named postgres) in the Postgres PgAdmin
Right-click on the item Servers, select Create -> Server and provide the connection to your PostgreSQL instance set up during the installation. In the default PostgreSQL setup, the administrator user is postgres with an empty password. In the connection tab be sure to have the host set to localhost. Click Save afterwards.

Right-click on the item Databases, select Create -> Database. Use "postgres" as the Database name. Set owner to the default user (postgres) in the step above and click Save afterwards.

# Step IV: Setup the Environment Variables
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD={the database password in step III}
DATABASE_NAME=postgres
DATABASE_USERNAME=postgres

# Step V: Run the local server with:
uvicorn app.main:app --reload
This will first create the database schema using the SQLAlchemy ORM and then start the service.

Copy the URL the service is running on and paste it in your browser: http://127.0.0.1:8000





