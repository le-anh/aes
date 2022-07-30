from Crypto.Cipher import AES

class AesConst:
    @staticmethod
    def BlockSize()->int:
        return AES.block_size

    @staticmethod
    def PadSize()->int:
        return AesConst.BlockSize()

    @staticmethod
    def KeySize()->int:
        return AesConst.BlockSize() * 2
    
    @staticmethod
    def IVSize()->int:
        return AesConst.BlockSize()