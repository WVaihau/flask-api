from pydantic import BaseModel
from typing import Union

# VARIABLES

## Database : MongoDB

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "companydb"
COLLECTION_NAME = "corporate"

## Logs
logFile = "siret_api_logs.log"

# OBJECTS
class UpdateCompanyModel(BaseModel):
    statutDiffusionEtablissement: Union[str, None] = ""
    dateCreationEtablissement: Union[str, None] = ""
    trancheEffectifsEtablissement: Union[str, None] = ""
    anneeEffectifsEtablissement: Union[str, None] = ""
    activitePrincipaleRegistreMetiersEtablissement: Union[str, None] = ""
    dateDernierTraitementEtablissement: Union[str, None] = ""
    etablissementSiege: Union[str, None] = ""
    nombrePeriodesEtablissement: Union[str, None] = ""
    complementAdresseEtablissement: Union[str, None] = ""
    numeroVoieEtablissement: Union[str, None] = ""
    indiceRepetitionEtablissement: Union[str, None] = ""
    typeVoieEtablissement: Union[str, None] = ""
    libelleVoieEtablissement: Union[str, None] = ""
    codePostalEtablissement: Union[str, None] = ""
    libelleCommuneEtablissement: Union[str, None] = ""
    libelleCommuneEtrangerEtablissement: Union[str, None] = ""
    distributionSpecialeEtablissement: Union[str, None] = ""
    codeCommuneEtablissement: Union[str, None] = ""
    codeCedexEtablissement: Union[str, None] = ""
    libelleCedexEtablissement: Union[str, None] = ""
    codePaysEtrangerEtablissement: Union[str, None] = ""
    libellePaysEtrangerEtablissement: Union[str, None] = ""
    complementAdresse2Etablissement: Union[str, None] = ""
    numeroVoie2Etablissement: Union[str, None] = ""
    indiceRepetition2Etablissement: Union[str, None] = ""
    typeVoie2Etablissement: Union[str, None] = ""
    libelleVoie2Etablissement: Union[str, None] = ""
    codePostal2Etablissement: Union[str, None] = ""
    libelleCommune2Etablissement: Union[str, None] = ""
    libelleCommuneEtranger2Etablissement: Union[str, None] = ""
    distributionSpeciale2Etablissement: Union[str, None] = ""
    codeCommune2Etablissement: Union[str, None] = ""
    codeCedex2Etablissement: Union[str, None] = ""
    libelleCedex2Etablissement: Union[str, None] = ""
    codePaysEtranger2Etablissement: Union[str, None] = ""
    libellePaysEtranger2Etablissement: Union[str, None] = ""
    dateDebut: Union[str, None] = ""
    etatAdministratifEtablissement: Union[str, None] = ""
    enseigne1Etablissement: Union[str, None] = ""
    enseigne2Etablissement: Union[str, None] = ""
    enseigne3Etablissement: Union[str, None] = ""
    denominationUsuelleEtablissement: Union[str, None] = ""
    activitePrincipaleEtablissement: Union[str, None] = ""
    nomenclatureActivitePrincipaleEtablissement: Union[str, None] = ""
    caractereEmployeurEtablissement: Union[str, None] = ""

class CompanyModel(UpdateCompanyModel):
    siret: int
    siren: int
    nic: int
