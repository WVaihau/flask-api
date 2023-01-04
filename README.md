# SIRET API

@Authors (DE2) : 
- Raphaël JEHL
- Vincent LY
- Vaihau WILLIAMU
- Lucas MAIZ 

This is a FastAPI application that provides a RESTful API to retrieve and manipulate company information stored in a database based on their siret code.

## Requirements

Docker version : 20.10.16, build aa7e414

Python version : 3.8.8

## Installations

1. Downloads and setup

```cmd
docker pull mongo

docker run -d -p 27017:27017 --name m1 mongo

git clone https://github.com/WVaihau/api-siret.git

pip install -r requirements.txt
```

2. Download the csv file

Put the siret csv file StockEtablissement_utf8.csv located in Teams in the api-siret folder.

3. Load the data in mongo database

```cmd
python data_integration.py
```

_Note_ : This step might take a while as it will put all the records in the database.

4. Launch the app

```
uvicorn app:app --reload
```

## API Documentation

### Endpoints

- GET /get

Retrieve a company's information from the database based on its siret code.

__Input__

siret (int): The siret code of the company to retrieve.

__Output__

A list of dictionaries representing the company's information in JSON format.

__Errors__

If a company with the given siret code is not found, a 404 HTTP error is returned.

- POST /

Add a new company to the database.

__Input__

company (CompanyModel): The company to add to the database.

__Errors__

If a company with the same siret code already exists, a 409 HTTP error is returned.

If the siret code is not consistent with the siren and nic numbers, a 400 HTTP error is returned.

If the insertion into the database fails, a 400 HTTP error is returned.

- PUT /{siret}

Update a company's information in the database.

__Input__

siret (int): The siret code of the company to update.

company (UpdateCompanyModel): The updated company information.

__Errors__

If a company with the given siret code is not found, a 404 HTTP error is returned.

- DELETE /{siret}

Delete a company from the database.

__Input__

siret (int): The siret code of the company to delete.

__Errors__

If a company with the given siret code is not found, a 404 HTTP error is returned.

## Tests

After launching the app, you can try the API at this url : __127.0.0.1:8000/docs__

_Note_ : an example of an existing siret is __180725400014__