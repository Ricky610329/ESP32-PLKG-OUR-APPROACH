"""
This is a fast and lightweight serial data collection module.

-----------------------------------------
Simple, effective, and easy to use
-----------------------------------------

You should put everything that needs to be done in real-time processing in the 'activity' method.

If you need to use async in activity, please override the activity with:

async def activity_async(self, data):

and change:

async def __collection_main(self):
    self.__task_collection = asyncio.create_task(self.__collect_core())
    self.__pop_gen = self.__pop_core()
    async for data in self.__pop_gen:
        await self.activity_async(data)  # here

Furthermore, you can add:

def __init__(self, Port: str, Baud: int):
    self.lock = asyncio.Lock()

to help you with accessing the same parameter.

Author: Ricky
Date: 2023/10/10
"""

import serial
import asyncio
import atexit

class serial_target():
    def __init__(self,Port: str,Baud: int):
        self.__Port:str = Port
        self.__Baud:int = Baud
        self.__collect_interval:float = 0.1 #how long to check serial input
        self.__output_interval:float = 5 #how long to output serial data, use yield
        self.__ser: serial.Serial
        self.__buff: str = ""
        self.__terminate: bool = False
        self.__S_INIT: bool = False
        atexit.register(self.system_close)

        
    

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
    def serial_init(self)->bool:
        try:
            self.__ser = serial.Serial(self.__Port,self.__Baud)
            print("SERIAL INITIALIZATION SUCCESS")
            self.__S_INIT = True
            return self.__S_INIT
        except:
            print("SERIAL INITIALIZATION FAIL")
            self.__S_INIT = False
            return self.__S_INIT
    
    
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
        if self.__S_INIT:
            print("COLLECTION MAIN START")
            self.__task_collection = asyncio.create_task(self.__collect_core())
            self.__pop_gen = self.__pop_core()
            async for data in self.__pop_gen:
                self.activity(data)
        elif self.__S_INIT:
            print("TERMINATE COLLECTION MAIN")

    #run data collection
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



