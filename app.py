import controller as ctrl
import model as md
from fastapi import FastAPI, HTTPException, Request, Response

# Initialize the FastAPI app
app = FastAPI()

# Initialize the database connection
collection = ctrl.init_collection()

@app.get("/get", response_description="Get informations from a given siret code")
async def fetch_siret_info(request: Request, response: Response, siret:int):
    """
    Retrieve a company's information from the database based on its siret code.
    
    Args:
        request (Request): The request object provided by FastAPI.
        response (Response): The response object provided by FastAPI.
        siret (int): The siret code of the company to retrieve.
    
    Returns:
        list[dict]: A list of dictionaries representing the company's information.
    
    Raises:
        HTTPException: If a company with the given siret code is not found.
    """

    # Fetch from the DB based on the siret code
    cursor = collection.find({"siret":siret}, {"_id":False})
    # Parse the result
    results = [{k:str(v) for k,v in company.items()} for company in cursor]

    # Return the parsed result if found, otherwise raise an HTTPException
    if len(results) > 0 :
        ctrl.log(request, response)
        return results
    else:
        ctrl.log(request, response, 404)
        raise HTTPException(status_code=404, detail=f"Siret code : {siret} -> not found")

@app.post("/", response_description="Add a new company")
async def add_company(request: Request, response: Response, company: md.CompanyModel):
    """
    Add a new company to the database.
    
    Args:
        request (Request): The request object provided by FastAPI.
        response (Response): The response object provided by FastAPI.
        company (CompanyModel): The company to add to the database.
    
    Raises:
        HTTPException: If a company with the same siret code already exists, 
                      if the siret code is not consistent with the siren and nic numbers, 
                      or if the insertion into the database fails.
    """
    # Check if a company with the same siret code already exists
    already_exist = ctrl.find_result(collection, company.siret)
    if (len(already_exist)>0):
        raise HTTPException(status_code=409, detail=f"A company with {company.siret} siret code already exists")
    else:
        # Check if the siret code is consistent with the siren and nic numbers
        if(ctrl.consistency_siret(company.siret, company.siren, company.nic)):
            # Create a new company document
            new_company = ctrl.create_new_company(company)
            # Insert the new company into the database
            collection.insert_one(new_company)
            # Verify that the insertion was successful
            confirmed_insertion = ctrl.find_result(collection, company.siret)
            if len(confirmed_insertion)==1:
                ctrl.log(request, response)
                raise HTTPException(status_code=200, detail=f"The insertion proceed correctly")
            else:
                ctrl.log(request, response, 400)
                raise HTTPException(status_code=400, detail=f"The insertion doesn't work")
        else:
            ctrl.log(request, response, 400)
            raise HTTPException(status_code=400, detail=f"Inputs entered are not consistent. Siret must be composed of the siren number and the nic number.")


@app.put("/{siret}", response_description="Update a company")
def update_company(request: Request, response: Response, siret:int, company:md.UpdateCompanyModel):
    """
    Update a company in the database.
    
    Args:
        request (Request): The request object provided by FastAPI.
        response (Response): The response object provided by FastAPI.
        siret (int): The siret code of the company to update.
        company (UpdateCompanyModel): The updated company information.
    
    Raises:
        HTTPException: If a company with the given siret code does not exist, or if the update fails.
    """
    # Check if a company with the given siret code exists
    exist = ctrl.find_result(collection, siret)
    if len(exist)==0:
        ctrl.log(request, response, 404)
        raise HTTPException(status_code=404, detail=f"The corporate with {siret} siret code doesn't exist")
    else:
        # Update the company's information
        updated_company = ctrl.update_company(company)

        collection.update_one({"siret":siret}, {"$set": updated_company})
        ctrl.log(request, response, 200)
        raise HTTPException(status_code=200, detail=f"The update proceed correctly")

@app.delete("/delete/{company_siret}", response_description="Delete a company")
def delete_company(request: Request, response: Response, company_siret:int):
    """
    Delete a company from the database.
    
    Args:
        request (Request): The request object provided by FastAPI.
        response (Response): The response object provided by FastAPI.
        company_siret (int): The siret code of the company to delete.
    
    Raises:
        HTTPException: If a company with the given siret code does not exist, or if the deletion fails.
    """

    exist = ctrl.find_result(collection, company_siret)
    if len(exist)==0:
        ctrl.log(request, response, 404)
        raise HTTPException(status_code=404, detail=f"The corporate with {company_siret} siret code doesn't exist")
    else:
        # Delete the company from the database
        delete_result = collection.delete_one({"siret": company_siret})
        # Verify that the deletion was successful
        if delete_result.deleted_count == 1:
            ctrl.log(request, response, 200)
            raise HTTPException(status_code=200, detail=f"The deletion proceed correctly")
        else:
            ctrl.log(request, response, 400)
            raise HTTPException(status_code=400, detail=f"The deletion doesn't work")


