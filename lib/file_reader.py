class FileReader:
    # Read file
    @staticmethod
    def Read(file_in: str)->bytes:
        with open(file_in, "r") as fin:
            file_data = fin.read()
        return file_data