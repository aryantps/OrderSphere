# Basic E-Commerce App with MongoDB and FastAPI
This is a demo e-commerce application built with FastAPI and MongoDB. It provides basic functionality for managing orders, including creating orders, listing orders with pagination, searching orders by various criteria, and fetching order details by order ID.

## Installation
To run this application locally, we need Python(poetry) + mongoDB installed on system. Clone the repository, navigate to the project directory, and install the dependencies using poetry:

```zsh
git clone <repository_url>
cd <project_directory>
poetry install
```



## Running the App
After installing dependencies, run the mongoDB server and provide.env values. Then, run the FastAPI server using the following command.

```zsh
poetry run uvicorn main:app --reload
```


## API Documentation
The Swagger documentation, available at /docs, allows users to explore and test API endpoints.


