import unittest
import random
from fastapi.testclient import TestClient
from controller import init_collection, consistency_siret, create_new_company, find_result
from model import CompanyModel, UpdateCompanyModel
from app import app

client = TestClient(app)

def filter_res(p_response, p_fields=["siret", "siren", "nic"]):
    return [{k:v for k,v in p_response.json()[0].items() if k in p_fields}]

class TestAPI(unittest.TestCase):
    def setUp(self):
        # Initialize the database connection
        self.collection = init_collection()

    def test_1_add_company(self):
        # Test adding a new company
        new_company = CompanyModel(siret=12345600789, siren=123456, nic=789)
        response = client.post("/", json=new_company.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "The insertion proceed correctly"})

        # Test adding a company with an already existing siret code
        response = client.post("/", json=new_company.dict())
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"detail": "A company with 12345600789 siret code already exists"})

        # Test adding a company with an inconsistent siret code

        ## siret != siren + nic
        new_company.siret = 123456780
        response = client.post("/", json=new_company.dict())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Inputs entered are not consistent. Siret must be composed of the siren number and the nic number."})

        ## len(siret) > 14
        new_company.siret = 141234567800789
        new_company.siren = 1412345678
        new_company.nic = 789
        response = client.post("/", json=new_company.dict())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Inputs entered are not consistent. Siret must be composed of the siren number and the nic number."})

    def test_2_fetch_siret_info(self):
        # Test fetching a company that exists in the database
        response = client.get("/get", params={"siret": 12345600789})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(filter_res(response), 
        [{"siret": "12345600789", "siren": "123456", "nic": "789"}])

        # Test fetching a company that does not exist in the database
        response = client.get("/get", params={"siret": 987654321})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Siret code : 987654321 -> not found"})


    def test_3_update_company(self):
        # Test updating a company that exists in the database
        update_data = UpdateCompanyModel(etablissementSiege="Paris")
        response = client.put("/12345600789", json=update_data.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "The update proceed correctly"})

        # Test updating a company that does not exist in the database
        response = client.put("/987654321", json=update_data.dict())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "The corporate with 987654321 siret code doesn't exist"})

    def test_4_delete_company(self):
        # Test deleting a company that exists in the database
        response = client.delete("/delete/12345600789")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "The deletion proceed correctly"})

        # Test deleting a company that does not exist in the database
        response = client.delete("/delete/987654321")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "The corporate with 987654321 siret code doesn't exist"})

if __name__ == 'main':
    unittest.main()