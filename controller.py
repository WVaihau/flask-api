import model as md
import pymongo  # package for working with MongoDB
from loguru import logger
from fastapi import FastAPI, HTTPException, Request, Response


def init_collection():
    """
    Initialize the connection to the mongoDB database and return it
    """
    client = pymongo.MongoClient(md.MONGO_URL)
    db = client[md.DB_NAME]
    collection = db[md.COLLECTION_NAME]

    return collection

def log(request, response, code_status=200):
    """
    Logs a request and response in a log file.

    The function logs the client hostname, the request method, the response status code,
    and the route URL in the log file. If the status code is 200, the log is recorded as 
    an info. Otherwise, the log is recorded as a warning.

    Parameters:
    request (Request): Request object containing information about the request.
    response (Response): Response object containing information about the response.
    code_status (int, optional): Response status code. Default is 200.

    Returns:
    None
    """

    response.status_code = code_status

    # Open the log file
    logger.add(md.logFile)
    # Log the request and response
    message = "{} {:<6} {}  | route : {}".format(
        request.client.host,
        request.method,
        response.status_code,
        request.url.path
    )
    if response.status_code == 200:
        logger.info(message)
    else:
        logger.warning(message)
    # Close the log file
    logger.remove()

def find_result(collection, siret):
    """
    Retrieve the company information from the specified collection in the database with the given siret.
    
    Args:
        collection (pymongo.collection.Collection): The collection to retrieve the company from.
        siret (str): The siret of the company to retrieve.
    
    Returns:
        list[dict]: A list of dictionaries containing the company's information. The _id field is excluded from the returned dictionaries.
    """
    cursor = collection.find({"siret":siret}, {"_id":False})

    return [{k:str(v) for k,v in company.items()} for company in cursor]

def consistency_siret(siret, siren, nic):
    """
    Check whether the siret is consistent with the provided siren and nic.
    
    Args:
        siret (str): The siret to check.
        siren (str): The siren to check.
        nic (str): The nic to check.
    
    Returns:
        bool: True if the siret is 14 characters long, the siren is 9 characters long, and the siren and nic concatenated together form the siret. Otherwise, False.
    """

    return (str(siret) == "{}{:0>5}".format(siren, nic)) and (len("{:>14}".format(siret))==14)

def create_new_company(company : md.CompanyModel):
    """
    Create a dictionary containing the company's information.
    
    Args:
        company (md.CompanyModel): The company object to extract the information from.
    
    Returns:
        dict: A dictionary containing the company's information.
    """
    return {
        "siret" : company.siret,
        "siren" : company.siren,
        "nic" : company.nic,
        "statutDiffusionEtablissement" : company.statutDiffusionEtablissement,
        "dateCreationEtablissement" : company.dateCreationEtablissement,
        "trancheEffectifsEtablissement" : company.trancheEffectifsEtablissement,
        "anneeEffectifsEtablissement" : company.anneeEffectifsEtablissement,
        "activitePrincipaleRegistreMetiersEtablissement" : company.activitePrincipaleRegistreMetiersEtablissement,
        "dateDernierTraitementEtablissement" : company.dateDernierTraitementEtablissement,
        "etablissementSiege" : company.etablissementSiege,
        "nombrePeriodesEtablissement" : company.nombrePeriodesEtablissement,
        "complementAdresseEtablissement" : company.complementAdresseEtablissement,
        "numeroVoieEtablissement" : company.numeroVoieEtablissement,
        "indiceRepetitionEtablissement" : company.indiceRepetitionEtablissement,
        "typeVoieEtablissement" : company.typeVoieEtablissement,
        "libelleVoieEtablissement" : company.libelleVoieEtablissement,
        "codePostalEtablissement" : company.codePostalEtablissement,
        "libelleCommuneEtablissement" : company.libelleCommuneEtablissement,
        "libelleCommuneEtrangerEtablissement" : company.libelleCommuneEtrangerEtablissement,
        "distributionSpecialeEtablissement" : company.distributionSpecialeEtablissement,
        "codeCommuneEtablissement" : company.codeCommuneEtablissement,
        "codeCedexEtablissement" : company.codeCedexEtablissement,
        "libelleCedexEtablissement" : company.libelleCedexEtablissement,
        "codePaysEtrangerEtablissement" : company.codePaysEtrangerEtablissement,
        "libellePaysEtrangerEtablissement" : company.libellePaysEtrangerEtablissement,
        "complementAdresse2Etablissement" : company.complementAdresse2Etablissement,
        "numeroVoie2Etablissement" : company.numeroVoie2Etablissement,
        "indiceRepetition2Etablissement" : company.indiceRepetition2Etablissement,
        "typeVoie2Etablissement" : company.typeVoie2Etablissement,
        "libelleVoie2Etablissement" : company.libelleVoie2Etablissement,
        "codePostal2Etablissement" : company.codePostal2Etablissement,
        "libelleCommune2Etablissement" : company.libelleCommune2Etablissement,
        "libelleCommuneEtranger2Etablissement" : company.libelleCommuneEtranger2Etablissement,
        "distributionSpeciale2Etablissement" : company.distributionSpeciale2Etablissement,
        "codeCommune2Etablissement" : company.codeCommune2Etablissement,
        "codeCedex2Etablissement" : company.codeCedex2Etablissement,
        "libelleCedex2Etablissement" : company.libelleCedex2Etablissement,
        "codePaysEtranger2Etablissement" : company.codePaysEtranger2Etablissement,
        "libellePaysEtranger2Etablissement" : company.libellePaysEtranger2Etablissement,
        "dateDebut" : company.dateDebut,
        "etatAdministratifEtablissement" : company.etatAdministratifEtablissement,
        "enseigne1Etablissement" : company.enseigne1Etablissement,
        "enseigne2Etablissement" : company.enseigne2Etablissement,
        "enseigne3Etablissement" : company.enseigne3Etablissement,
        "denominationUsuelleEtablissement" : company.denominationUsuelleEtablissement,
        "activitePrincipaleEtablissement" : company.activitePrincipaleEtablissement,
        "nomenclatureActivitePrincipaleEtablissement" : company.nomenclatureActivitePrincipaleEtablissement,
        "caractereEmployeurEtablissement" : company.caractereEmployeurEtablissement
    }

def update_company(company : md.UpdateCompanyModel):
    """
    Create a dictionary containing the company's information based on the update company model
    
    Args:
        company (md.UpdateCompanyModel): The company object to get the information from.
    
    Returns:
        dict: A dictionary containing the company's information.
    """
    return {
            "statutDiffusionEtablissement" : company.statutDiffusionEtablissement,
            "dateCreationEtablissement" : company.dateCreationEtablissement,
            "trancheEffectifsEtablissement" : company.trancheEffectifsEtablissement,
            "anneeEffectifsEtablissement" : company.anneeEffectifsEtablissement,
            "activitePrincipaleRegistreMetiersEtablissement" : company.activitePrincipaleRegistreMetiersEtablissement,
            "dateDernierTraitementEtablissement" : company.dateDernierTraitementEtablissement,
            "etablissementSiege" : company.etablissementSiege,
            "nombrePeriodesEtablissement" : company.nombrePeriodesEtablissement,
            "complementAdresseEtablissement" : company.complementAdresseEtablissement,
            "numeroVoieEtablissement" : company.numeroVoieEtablissement,
            "indiceRepetitionEtablissement" : company.indiceRepetitionEtablissement,
            "typeVoieEtablissement" : company.typeVoieEtablissement,
            "libelleVoieEtablissement" : company.libelleVoieEtablissement,
            "codePostalEtablissement" : company.codePostalEtablissement,
            "libelleCommuneEtablissement" : company.libelleCommuneEtablissement,
            "libelleCommuneEtrangerEtablissement" : company.libelleCommuneEtrangerEtablissement,
            "distributionSpecialeEtablissement" : company.distributionSpecialeEtablissement,
            "codeCommuneEtablissement" : company.codeCommuneEtablissement,
            "codeCedexEtablissement" : company.codeCedexEtablissement,
            "libelleCedexEtablissement" : company.libelleCedexEtablissement,
            "codePaysEtrangerEtablissement" : company.codePaysEtrangerEtablissement,
            "libellePaysEtrangerEtablissement" : company.libellePaysEtrangerEtablissement,
            "complementAdresse2Etablissement" : company.complementAdresse2Etablissement,
            "numeroVoie2Etablissement" : company.numeroVoie2Etablissement,
            "indiceRepetition2Etablissement" : company.indiceRepetition2Etablissement,
            "typeVoie2Etablissement" : company.typeVoie2Etablissement,
            "libelleVoie2Etablissement" : company.libelleVoie2Etablissement,
            "codePostal2Etablissement" : company.codePostal2Etablissement,
            "libelleCommune2Etablissement" : company.libelleCommune2Etablissement,
            "libelleCommuneEtranger2Etablissement" : company.libelleCommuneEtranger2Etablissement,
            "distributionSpeciale2Etablissement" : company.distributionSpeciale2Etablissement,
            "codeCommune2Etablissement" : company.codeCommune2Etablissement,
            "codeCedex2Etablissement" : company.codeCedex2Etablissement,
            "libelleCedex2Etablissement" : company.libelleCedex2Etablissement,
            "codePaysEtranger2Etablissement" : company.codePaysEtranger2Etablissement,
            "libellePaysEtranger2Etablissement" : company.libellePaysEtranger2Etablissement,
            "dateDebut" : company.dateDebut,
            "etatAdministratifEtablissement" : company.etatAdministratifEtablissement,
            "enseigne1Etablissement" : company.enseigne1Etablissement,
            "enseigne2Etablissement" : company.enseigne2Etablissement,
            "enseigne3Etablissement" : company.enseigne3Etablissement,
            "denominationUsuelleEtablissement" : company.denominationUsuelleEtablissement,
            "activitePrincipaleEtablissement" : company.activitePrincipaleEtablissement,
            "nomenclatureActivitePrincipaleEtablissement" : company.nomenclatureActivitePrincipaleEtablissement,
            "caractereEmployeurEtablissement" : company.caractereEmployeurEtablissement
        }