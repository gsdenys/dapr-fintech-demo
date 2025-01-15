from fastapi import APIRouter
from bson.objectid import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

from app.database import collection
from app.model import Company

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_company(company: Company):
    """
    Create a new company in the database.

    Args:
        company (Company): The company data to be created.

    Returns:
        dict: A dictionary containing the ID of the newly created company.
    """
    new_company = company.model_dump()
    result = await collection.insert_one(new_company)

    return {"id": str(result.inserted_id)}


@router.get("/{{company_id}}", response_model=dict)
async def get_company(company_id: str):
    """
    Retrieve a company by its ID.

    Args:
        company_id (str): The ID of the company to retrieve.

    Returns:
        dict: The company data if found.

    Raises:
        CompanyNotFoundException: If the company is not found.
        InternalServerErrorException: If an unexpected error occurs during database interaction.
    """
    company = await collection.find_one({"_id": ObjectId(company_id)})

    if not company:
        raise HTTPException(status_code=404)

    company["id"] = str(company["_id"])
    del company["_id"]

    return company


@router.delete("/{{company_id}}", response_model=dict)
async def delete_company(company_id: str):
    """
    Delete a company by its ID.

    Args:
        company_id (str): The ID of the company to delete.

    Returns:
        dict: A dictionary containing a success message if the deletion is successful.

    Raises:
        CompanyNotFoundException: If the company is not found.
        InternalServerErrorException: If an unexpected error occurs during database interaction.
    """
    result = await collection.delete_one({"_id": ObjectId(company_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404)

    return {"message": "Company deleted successfully"}


@router.put("/{{company_id}}", response_model=dict)
async def update_company(company_id: str, company: Company):
    """
    Update a company's details by its ID.

    Args:
        company_id (str): The ID of the company to update.
        company (Company): The updated company data.

    Returns:
        dict: A dictionary containing a success message if the update is successful.

    Raises:
        CompanyNotFoundException: If the company is not found.
        InternalServerErrorException: If an unexpected error occurs during database interaction.
    """
    updated_company = {"$set": company.model_dump()}

    result = await collection.update_one({"_id": ObjectId(company_id)}, updated_company)

    if result.matched_count == 0:
        raise HTTPException(status_code=404)

    return {"message": "Company updated successfully"}


@router.get("/")
async def get_all_companies():
    """
    Retrieve all companies from the database.

    Returns:
        list: A list of dictionaries, each containing the data of a company.

    Raises:
        InternalServerErrorException: If an unexpected error occurs during database interaction.
    """

    companies = []

    async for company in collection.find():
        company["id"] = str(company["_id"])
        del company["_id"]

        companies.append(company)

    return companies
