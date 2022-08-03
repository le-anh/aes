class FileWriter:
    # Writer file
    @staticmethod
    def Write(file_out: str, data: bytes, mod="w")->None:
        with open(file_out, mod) as fout:
            fout.write(data)