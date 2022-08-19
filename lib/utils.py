import binascii
from typing import Union

class Utils:

    @staticmethod
    def Decode(data: Union[str, bytes], encoding: str = "utf-8") -> str:
        if isinstance(data, str):
            dec = data
        elif isinstance(data, bytes):
            dec = data.decode(encoding)
        else:
            raise TypeError("Invalid data type")
        return dec

    @staticmethod
    def Encode(data: Union[str, bytes], encoding: str = "utf-8") -> bytes:
        if isinstance(data, str):
            enc = data.encode(encoding)
        elif isinstance(data, bytes):
            enc = data
        else:
            raise TypeError("Invalid data type")
        return enc

    @staticmethod
    def DataToString(data: Union[str, bytes]) -> str:
        if isinstance(data, str):
            st = data
        elif isinstance(data, bytes):
            st = Utils.BytesToHexStr(data)
        else:
            raise TypeError("Invalid data type")
        return st

    @staticmethod
    def BytesToHexStr(data: bytes) -> str:
        return Utils.Decode(binascii.hexlify(data))