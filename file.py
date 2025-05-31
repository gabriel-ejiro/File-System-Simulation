class File(FileSystemComponent):
    def __init__(self, name, size):
        super().__init__(name)
        self._size = size  # size in KB

    def get_size(self):
        return self._size

    def display(self, indent=0):
        print(" " * indent + f"📄 {self.name} ({self._size} KB)")
