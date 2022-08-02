class FileWriter:
    # Writer file
    @staticmethod
    def Write(file_out: str, data: bytes)->None:
        with open(file_out, 'w') as fout:
            fout.write(data)