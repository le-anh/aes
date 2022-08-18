class FileReader:
    @staticmethod
    def Read(file_in: str)->bytes:
        with open(file_in, "rb") as fin:
            file_data = fin.read()
        return file_data