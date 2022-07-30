# File writer class
class FileWriter:
    # Write file
    @staticmethod
    def Write(file_out: str,
              data: bytes) -> None:
        with open(file_out, "wb") as fout:
            fout.write(data)
