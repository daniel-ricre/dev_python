import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

api_key = os.getenv("API_KEY")


# for authentication
def verify_api_key(key):
    if key != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not autenticated"
        )


print(api_key)
