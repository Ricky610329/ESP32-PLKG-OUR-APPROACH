import universal_collector as uc

Filename = "CSIdata.txt"


class printer(uc.serial_target):
    def __init__(self, Port: str, Baud: int):
        super().__init__(Port, Baud)
    def activity(self,data):
        print(data)
        with open(Filename,'a') as file:
            file.write(data)

test = printer("COM6","115200")

test.serial_init()
test.collect()

while True:
    command = input(">>>")
    if command == "-stop":
        test.system_close()
        break
