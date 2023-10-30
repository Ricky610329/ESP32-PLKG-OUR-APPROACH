import predata.universal_collector as uc
import asyncio
import glob
import threading

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
            index = 1
            for s in filelist:
                temp = int(s[len(Data_Path)+len(Defult)+1:-len(filetype)]) + 1
                index = max(temp,index)
        filename =  Data_Path + r"/" + Defult + str(index) + filetype
    if not AutoIndex and Custom:
        filename = input("Custom>>")
        filename =  Data_Path + r"/" + filename + filetype
    print(filename)
    return filename







class printer(uc.serial_target):
    def __init__(self, Port: str, Baud: int):
        super().__init__(Port, Baud)
        self.filename = "Empty"
    def newFilename(self):
        self.filename = FileNameGenerator()
    async def activity(self,data):
        #print(data)
        with open(self.filename,'a') as file:
            file.write(data)



def main():
    collect_monitor = printer("COM5","115200")

    ##initial collection
    ##serial close

    while True:
        command = input("\n>>")
        if command == "r":
            collect_monitor.newFilename()
            collect_monitor.serial_init()
            task = threading.Thread(target = collect_monitor.collect)
            task.start()
        if command == 'q':
        
            collect_monitor.system_close()
            task.join()

if __name__ == "__main__":
    main()