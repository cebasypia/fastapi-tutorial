from typing import TypedDict


class TEmail(TypedDict):
    email: list[str]


class TFirebase(TypedDict):
    identities: TEmail


class AuthUser(TypedDict):
    iss: str
    aud: str
    auth_time: int
    user_id: str
    sub: str
    iat: int
    exp: int
    email: str
    email_verified: bool
    firebase: TFirebase
    uid: str
