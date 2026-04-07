from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.config.settings import settings
import jwt


class PasswordHelper:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password using bcrypt.

        Args:
            password (str): The password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the password is verified, False otherwise.
        """
        return self.pwd_context.verify(password, hashed_password)


class TokenHelper:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """Create an access token.

        Args:
            data (dict): The data to encode.
            expires_delta (timedelta | None): The expiration time.

        Returns:
            str: The encoded access token.
        """
        encoded_data = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        encoded_data.update({"exp": expire})
        encoded_jwt = jwt.encode(encoded_data, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
