import pyads

class TwinCat3_ADSserver:
    def __init__(self, ip = "127.0.0.1.1.1", amsNetIdTarget = pyads.PORT_TC3PLC1):
        '''
        type ip: str
        type amsNetIdTarget: pyads.PORT_xxx
        '''
        self.ip = ip
        self.amsNetIdTarget = amsNetIdTarget
        self.plc = pyads.Connection(ip, pyads.PORT_TC3PLC1)
        self.plc.open()
    
    def read_by_name(self, name, type):
        '''
        type name: str
        type type: pyads.PLCTYPE_xxx; example:pyads.PLCTYPE_INT
        '''
        return self.plc.read_by_name(name, type)
    
    def write_by_name(self, name, value, type):
        '''
        type name: str
        type value: int, float, str, bool
        type type: pyads.PLCTYPE_xxx; example:pyads.PLCTYPE_INT
        '''
        self.plc.write_by_name(name, value, type)
    
    def close(self):
        self.plc.close()


