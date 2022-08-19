class FileReader:
    @staticmethod
    def Read(file_in: str, mod: str = "rb") -> bytes:
        with open(file_in, mod) as fin:
            file_data = fin.read()
        return file_data