from pydantic import BaseModel

class Company(BaseModel):
    """
    Pydantic model to define the structure of a Company.

    Attributes:
        name (str): The name of the company.
        registration_number (str): The registration number of the company.
    """

    name: str
    registration_number: str