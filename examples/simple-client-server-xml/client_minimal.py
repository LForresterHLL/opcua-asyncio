import asyncio
import logging

import asyncua
from asyncua import Client
from asyncua import ua
import numpy as np
from datetime import datetime

class HelloClient:
    def __init__(self, endpoint):
        
        self.client = Client(endpoint)
        
    

    async def __aenter__(self):
        securityString = "Basic256Sha256,SignAndEncrypt,'C:\Users\User\Documents\GitHub\opcua-asyncio\examples\certificates\peer-certificate-example-1.der','C:\Users\User\Documents\GitHub\opcua-asyncio\examples\certificates\peer-certificate-example-1.der'"
        await self.client.set_security_string(securityString)
        await self.client.connect()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()

namespace = "http://phoenixcontact.com/OpcUA/DataSource/IEC61131-3/NewDataSource/"
async def main():
    async with HelloClient("opc.tcp://localhost:4840/UADiscovery/") as client:


        
        root = client.nodes.root
        print("Root node is: ", root)
        objects = client.nodes.objects
        print("Objects node is: ", objects)


        nsidx = await client.get_namespace_index(namespace)
        print(f"\n\nNamespace Index for '{namespace}': {nsidx}\n\n")
        
        rootchildren = await root.get_children()
        print(f"\n\nChildren of root: {rootchildren}\n\n")

        objchildren = await objects.get_children()
        print(f"\n\nChildren of objects: {objchildren}\n\n")


        # PRINT EVERYTHING THE DATA SOURCE HAS
        datanode = client.get_node("ns=8;s=/")
        name = (await datanode.read_browse_name()).Name

        datachildren = await datanode.get_children()
        print(f"Children of {name}: {datachildren}\n\n")

        # PRINT ALL GLOBAL VARIABLES
        globalvarsnode = client.get_node("ns=8;s=/.GlobalVars")
        name = (await globalvarsnode.read_browse_name()).Name
        globalvarschildren = await globalvarsnode.get_children()
        print(f"Children of {name}: {globalvarschildren}\n\n")

        # And down a last level to the TCI_00 level
        

        # ANALOGUE READ TEST
        TCL_00_node = client.get_node("ns=8;s=/g.TCI_00")
        name = (await TCL_00_node.read_browse_name()).Name
        val = await TCL_00_node.read_value()
        # type = await TCL_00_node.read_data_value()
        # print(type)
        
        print("_______________________________\n")
        print(f"{name} = {val}")
        print("_______________________________")

        # DIGITAL READ TEST
        DI_01_node = client.get_node("ns=8;s=/g.DI_01")
        name = (await DI_01_node.read_browse_name()).Name
        

        


        # ANALOGUE WRITE TEST
        # read first
        AO_00_NODE = client.get_node("ns=8;s=/g.AO_00")
        name = (await AO_00_NODE.read_browse_name()).Name
        val = await AO_00_NODE.read_value()
        print(f"\n\n{name} = {val}\n\n")
        print(await AO_00_NODE.read_data_value())
        # Try to write
       
        print("\n")     
        print(await AO_00_NODE.get_access_level())
        print("\n")

        await A
        
        # await AO_00_NODE.set_writable()
        # await AO_00_NODE.write_value(60)

        val = await AO_00_NODE.read_value()
        print(f"\n\n{name} = {val}\n\n")

        while True:
            await asyncio.sleep(1)
        
        # DIGITAL WRITE TEST
        # read first
        # DO_00_NODE = client.get_node("ns=8;s=/g.DO_00")
        # name = (await DO_00_NODE.read_browse_name()).Name
        # val = await DO_00_NODE.read_value()
        # print(f"\n{name} = {val}\n")
        
        # await DO_00_NODE.write_value(True)
        # print(f"\n\n{name} = {val}\n\n")







if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
