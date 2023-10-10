import universal_collector as uc

Filename = "CSIdata.txt"


class printer(uc.serial_target):
    def activity(self,data):
        with open(Filename,'a') as file:
            print(data)
            file.write(data)

test = printer("COM5","115200")

test.serial_init()
test.collect()

while True:
    command = input(">>>")
    if command == "-stop":
        test.system_close()
        break
