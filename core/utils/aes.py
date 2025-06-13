import json
import base64
import os
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def __init__(self, token: Optional[str] = None) -> None:
        self.key = self.__generate_key()
        self.iv = self.__generate_iv()
        self.token = token


    def __generate_key(self) -> bytes:
        raw_key = os.getenv("JWT_SECRET_KEY")
        return raw_key.encode("utf-8")

    def __generate_iv(self) -> bytes:
        raw_iv = os.getenv("JWT_IV")
        return raw_iv.encode("utf-8")

    def generate_token(self, expires_in: int, data: Dict[str, Any]) -> "AESCipher":
        data["exp"] = (datetime.now() + timedelta(minutes=expires_in)).timestamp()
        json_string = json.dumps(data)
        data_bytes = json_string.encode("utf-8")
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(pad(data_bytes, AES.block_size))
        self.token = base64.b64encode(self.iv + encrypted).decode("utf-8")
        return self

    @property
    def json(self) -> Dict[str, Any]:
        if self.token is None:
            raise ValueError("Didn't generate a token yet. Generate a token first.")
        try:
            encrypted_data = base64.b64decode(self.token)
            iv = encrypted_data[: AES.block_size]
            encrypted_message = encrypted_data[AES.block_size :]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted_message), AES.block_size)
            json_string = decrypted.decode("utf-8")
        except:
            return None
        return json.loads(json_string)

    @property
    def is_valid(self) -> bool:
        try:
            self.json
        except:
            return False
        return True

    @property
    def is_expired(self) -> bool:
        self.json
        if self.json["exp"] < datetime.now().timestamp():
            return True
        return False
    

    def extend_exp(self, expires_in: int) -> "AESCipher":
        data = self.json
        data["exp"] = (datetime.now() + timedelta(minutes=expires_in)).timestamp()
        self.generate_token(expires_in, data)
        return self

    def __repr__(self) -> str:
        return f"AESCipher(token={self.token})"