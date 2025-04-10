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
                time.sleep(0.01)
                
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

    def connect(self):
        """连接到TwinCAT3 PLC"""
        self.plc.open()
        print("已连接到TwinCAT3 PLC")