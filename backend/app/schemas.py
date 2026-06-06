from pydantic import BaseModel, EmailStr, Field, model_validator

class UserSignup(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    @model_validator(mode='after')
    def verify_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match!")
        return self

class UserLogin(BaseModel):
    username: str
    password: str

class ParcelCreateRequest(BaseModel):
    name: str
    boundary: dict

# ADD THIS TO FIX THE ERROR
class AuditRunRequest(BaseModel):
    parcel_id: str
    feature_scenario: str