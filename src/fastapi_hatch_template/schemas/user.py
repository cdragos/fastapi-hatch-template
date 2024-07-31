from pydantic import UUID4, BaseModel, EmailStr


class UserSchema(BaseModel):
    id: UUID4
    first_name: str | None
    last_name: str | None
    email: EmailStr

    class Config:
        from_attributes = True


class UsersResponseSchema(BaseModel):
    count: int
    users: list[UserSchema]
