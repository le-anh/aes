from Crypto.Cipher import AES

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class EccConst:
    # https://www.ietf.org/rfc/rfc5639.txt ==> 3.4.  Domain Parameters for 256-Bit Curves
    P = 0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377
    A = 0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9
    B = 0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6
    G = Point(0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262, 0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997)
    N = 0xA9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7


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