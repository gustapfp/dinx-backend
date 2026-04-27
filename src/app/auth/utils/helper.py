from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.config.settings import settings


class PasswordHelper:
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a bcrypt hash.

        Args:
            password (str): The plain-text password to verify.
            hashed_password (str): The stored bcrypt hash to verify against.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


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

    def decode_access_token(self, token: str) -> dict:
        """Decode and validate a JWT access token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded token payload.

        Raises:
            jwt.InvalidTokenError: If the token is invalid or expired.
        """
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
