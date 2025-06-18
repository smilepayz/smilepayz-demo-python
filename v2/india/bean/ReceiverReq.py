class ReceiverReq:
    def __init__(self, name):
        if name is not None:
            self.name = name


    def print_info(self):
        print(f"{self.name}  ")

