class FileWriter:
    @staticmethod
    def Write(file_out: str, data: bytes, mod : str = "w") -> None:
        with open(file_out, mod) as fout:
            fout.write(data)