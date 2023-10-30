"""
This is a fast and lightweight serial data collection module.

-----------------------------------------
Simple, effective, and easy to use
-----------------------------------------

You should put everything that needs to be done in real-time processing in the 'activity' method.

If you need to use async in activity, please override the activity with:

async def activity_async(self, data):

and change:

async def _collection_main(self):
    self.__task_collection = asyncio.create_task(self._collect_core())
    self.__pop_gen = self._pop_core()
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
        self._Port:str = Port
        self._Baud:int = Baud
        self._collect_interval:float = 0.1 #how long to check serial input
        self._output_interval:float = 5 #how long to output serial data, use yield
        self._ser: serial.Serial
        self._buff: str = ""
        self._terminate: bool = False
        self._S_INIT: bool = False
        self._lock = asyncio.Lock()
        atexit.register(self.system_close)

        
    

    #set collect interval
    def set_collect_interval(self, collect_interval: float) -> bool:
        try:
            self._collect_interval = collect_interval
            print("COLLECT INTERVAL CHANGE SUCCESS")
            return True
        except:
            print("COLLECT INTERVAL CHANGE FAIL")
            return False
    
    #set output interval
    def set_output_interval(self, output_interval: float) -> bool:
        try:
            self._output_interval = output_interval
            print("OUTPUT INTERVAL CHANGE SUCCESS")
            return True
        except:
            print("OUTPUT INTERVAL CHANGE FAIL")
            return False
    
    #initialize serial
    def serial_init(self)->bool:
        self._terminate = False
        self._S_INIT = False
        try:
            self._ser = serial.Serial(self._Port,self._Baud)
            print("SERIAL INITIALIZATION SUCCESS")
            self._S_INIT = True
            return self._S_INIT
        except:
            print("SERIAL INITIALIZATION FAIL")
            self._S_INIT = False
            return self._S_INIT
    
    
    #output data core
    async def _pop_core(self):
        while not self._terminate:
            async with self._lock:
                yield self._buff
                self._buff = ""
            await asyncio.sleep(self._output_interval)
    #collect serial data core
    async def _collect_core(self):
        while not self._terminate:
            async with self._lock:
                try:
                    self._buff = self._buff + self._ser.read(self._ser.in_waiting).decode()
                except UnicodeDecodeError:
                    return False
            await asyncio.sleep(self._collect_interval)

    #main collection system
    async def _collection_main(self):
        if self._S_INIT:
            print("COLLECTION MAIN START")
            self.__task_collection = asyncio.create_task(self._collect_core())
            self.__pop_gen = self._pop_core()
            async for data in self.__pop_gen:
                await self.activity(data)
        elif self._S_INIT:
            print("TERMINATE COLLECTION MAIN")

    #run data collection
    def collect(self):
        asyncio.run(self._collection_main())

    
    #close serial
    def system_close(self):
        try:
            self._terminate = True
            self._ser.close()
            print("SERIAL CLOSED")
            return True
        except:
            print("SERIAL CLOSED FAIL")
            return False
        
    
    #write you code in activity
    async def activity_async(self, data):
        pass