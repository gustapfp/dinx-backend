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
        """Create a short-lived access token.

        Args:
            data (dict): The data to encode (must include "sub").
            expires_delta (timedelta | None): Custom expiration; defaults to 15 minutes.

        Returns:
            str: Encoded JWT access token.
        """
        encoded_data = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        encoded_data.update({"exp": expire, "type": "access"})
        return jwt.encode(encoded_data, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict) -> tuple[str, datetime]:
        """Create a long-lived refresh token.

        Args:
            data (dict): The data to encode (must include "sub").

        Returns:
            tuple[str, datetime]: Encoded JWT refresh token and its expiration datetime.
        """
        encoded_data = data.copy()
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        encoded_data.update({"exp": expires_at, "type": "refresh"})
        token = jwt.encode(encoded_data, self.secret_key, algorithm=self.algorithm)
        return token, expires_at

    def decode_token(self, token: str) -> dict:
        """Decode and validate a JWT token (access or refresh).

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded token payload.

        Raises:
            jwt.InvalidTokenError: If the token is invalid or expired.
        """
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
