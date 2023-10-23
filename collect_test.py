import universal_collector as uc
import asyncio
import glob

Data_Path = r"./collect_data"

Defult = r"csi_data"
filetype = r".txt"

#|Defult|AutoIndex|custom|filetype|
def FileNameGenerator(AutoIndex:bool = True, Custom: bool = False):
    global Data_Path
    if AutoIndex:
        path = Data_Path + r"/" + Defult + r"*"+ filetype
        filelist = glob.glob(path)
        if len(filelist) == 0:
            index = 1
        else:
            index = int(filelist[-1][len(Data_Path)+len(Defult)+1:-len(filetype)]) + 1
        filename =  Data_Path + r"/" + Defult + str(index) + filetype
    if not AutoIndex and Custom:
        filename = input("Custom>>")
        filename =  Data_Path + r"/" + filename + filetype

    return filename





class printer(uc.serial_target):
    def __init__(self, Port: str, Baud: int):
        super().__init__(Port, Baud)
        self.filename = "Empty"
    def newFilename(self):
        self.filename = FileNameGenerator()
    async def activity(self,data):
        print(data)
        with open(self.filename,'a') as file:
            file.write(data)

collect_monitor = printer("COM5","115200")

##initial collection
##serial close

while True:
    command = input("\n>>")
    if command == "r":
        collect_monitor.newFilename()
        collect_monitor.serial_init()
        collect_monitor.collect()

