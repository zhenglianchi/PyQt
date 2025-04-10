import pyads
import threading
import time

class TwinCat3_ADSserver:
    def __init__(self, ip="127.0.0.1.1.1", amsNetIdTarget=pyads.PORT_TC3PLC1):
        '''
        type ip: str
        type amsNetIdTarget: pyads.PORT_xxx
        '''
        self.ip = ip
        self.amsNetIdTarget = amsNetIdTarget
        self.plc = pyads.Connection(ip, pyads.PORT_TC3PLC1)
        self.plc.open()
        # 新增线程相关属性
        self.update_thread = None
        self.running = False
        self.lock = threading.Lock()
        self.variables = {}  # 存储要监控的变量 {name: (type, callback)}

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

    def add_variable(self, name, var_type, callback=None):
        """添加要监控的变量"""
        with self.lock:
            self.variables[name] = (var_type, callback)

    def remove_variable(self, name):
        """移除监控变量"""
        with self.lock:
            if name in self.variables:
                del self.variables[name]

    def _update_loop(self):
        """线程主循环"""
        while self.running:
            try:
                # 复制当前变量列表避免遍历时修改
                with self.lock:
                    current_vars = self.variables.copy()
                
                # 遍历并读取所有变量
                for name, (var_type, callback) in current_vars.items():
                    value = self.read_by_name(name, var_type)
                    if callback:
                        callback(name, value)  # 触发回调
                
                # 更新间隔（可根据需要调整）
                time.sleep(0.1)
                
            except pyads.ADSError as e:
                print(f"ADS通信错误: {e}")
                time.sleep(1)  # 出错后等待重试
            except Exception as e:
                print(f"未知错误: {e}")
                break

    def start_thread(self):
        """启动更新线程"""
        if not self.running:
            self.running = True
            self.update_thread = threading.Thread(target=self._update_loop)
            self.update_thread.daemon = True  # 设置为守护线程
            self.update_thread.start()
            print("变量监控线程已启动")

    def stop_thread(self):
        """停止更新线程"""
        if self.running:
            self.running = False
            if self.update_thread.is_alive():
                self.update_thread.join()
            print("变量监控线程已停止")



# 初始化连接
tc3 = TwinCat3_ADSserver()

# 定义回调函数
def value_changed(name, value):
    print(f"变量更新: {name} = {value}")

# 添加要监控的变量
tc3.add_variable("MAIN.bCounter", pyads.PLCTYPE_INT, value_changed)
tc3.add_variable("MAIN.fTemperature", pyads.PLCTYPE_BOOL, value_changed)

# 启动线程
tc3.start_thread()

# 停止线程
tc3.stop_thread()