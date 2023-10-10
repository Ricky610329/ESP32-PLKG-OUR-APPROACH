"""
This is a fast and light weight serial data collect module.

-----------------------------------------
simple, affective, easy to use
-----------------------------------------

Ricky 2023/10/10
"""

import serial
import asyncio

class serial_target():
    def __init__(self,Port: str,Baud: int):
        self.__Port:str = Port
        self.__Baud:int = Baud
        self.__collect_interval:float = 0.1 #how long to check serial input
        self.__output_interval:float = 5 #how long to output serial data, use yield
        self.__ser: serial.Serial
        self.__buff: str = ""
        self.__terminate: bool = False
    

    #set collect interval
    def set_collect_interval(self, collect_interval: float) -> bool:
        try:
            self.__collect_interval = collect_interval
            print("COLLECT INTERVAL CHANGE SUCCESS")
            return True
        except:
            print("COLLECT INTERVAL CHANGE FAIL")
            return False
    
    #set output interval
    def set_output_interval(self, output_interval: float) -> bool:
        try:
            self.__output_interval = output_interval
            print("OUTPUT INTERVAL CHANGE SUCCESS")
            return True
        except:
            print("OUTPUT INTERVAL CHANGE FAIL")
            return False
    
    #initialize serial
    def serial_init(self):
        try:
            self.__ser = serial.Serial(self.__Port,self.__Baud)
            print("SERIAL INITIALIZATION SUCCESS")
            return True
        except:
            print("SERIAL INITIALIZATION FAIL")
            return False
    
    
    #output data core
    async def __pop_core(self):
        while not self.__terminate:
            await asyncio.sleep(self.__output_interval)
            yield self.__buff
            self.__buff = ""

    #collect serial data core
    async def __collect_core(self):
        while not self.__terminate:
            try:
                self.__buff = self.__buff + self.__ser.read(self.__ser.in_waiting).decode()
            except UnicodeDecodeError:
                return False
            await asyncio.sleep(self.__collect_interval)

    #main collection system
    async def __collection_main(self):
        self.__task_collection = asyncio.create_task(self.__collect_core())
        self.__pop_gen = self.__pop_core()
        async for data in self.__pop_gen:
            self.activity(data)

    def collect(self):
        asyncio.run(self.__collection_main())

    
    #close serial
    def system_close(self):
        try:
            self.__terminate = True
            self.__ser.close()
            print("SERIAL CLOSED")
            return True
        except:
            print("SERIAL CLOSED FAIL")
            return False
        
    
    #write you code in activity
    def activity(self,data):
        pass