Materials Database API - Quick Start Guide
Introduction
Welcome to the Materials Database API! This guide will help you get started with running the API on your local machine.

Prerequisites
Before you begin, make sure you have the following installed on your machine:

Python
MongoDB
Installation

Clone the project repository from GitHub:

$pip install -r requirements.txt
Set Up MongoDB
Start MongoDB:

For Windows: Open the MongoDB Compass application.

For macOS/Linux: Open a terminal and run:

$mongod
Run the API
Open a terminal in the project directory.

Run the following command to load data into the database:

$python app.py
This will load sample data into the MongoDB database.

Once the data is loaded, the API will be accessible at http://192.168.1.5:8080/.

Using the API
Store Data
To store new data, you can use the following command:

$curl -X POST -H "Content-Type: application/json" -d '{"nsites": 1, "formula_pretty": "H2O", "volume": 18.01528}' http://192.168.1.5:8080/store-data


Search
To search for materials, use: 

$curl -X GET "http://192.168.1.5:8080/search?query=H2O"


Numerical Filter
Apply numerical filters with:

$curl -X GET "http://192.168.1.5:8080/filter?field=volume&operator=>&value=10"



Boolean Field Filter
Filter using boolean fields:

$curl -X GET "http://192.168.1.5:8080/boolean-filter?field=is_stable&value=true"


Element-Based Filtering
Perform element-based filtering:

$curl -X GET "http://192.168.1.5:8080/element-filter?elements=Ti-N"


Multi-Column Sort
Sort the data based on columns:

$curl -X GET "http://192.168.1.5:8080/sort?columns=volume,density&order=asc"


Clone the repository:

$git clone https://github.com/panujkumar86/Material-DB.git

Navigate to the project directory:

$cd your-repo
Install the required Python packages:
