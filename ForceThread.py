import time

from PyQt5.QtCore import QThread, pyqtSignal
import NetFT


class ForceThread(QThread):
    _ft_data = pyqtSignal(list)

    def __init__(self, ftSensorIp):
        super().__init__()
        self.ip = ftSensorIp
        self._is_running = False
        self.sensor = None
        self.setObjectName("ForceThread")

    def run(self):
        self._is_running = True
        try:
            self.sensor = NetFT.Sensor(self.ip)
            self.sensor.tare()
            self.sensor.startStreaming()

            while self._is_running:
                try:
                    data_record = self.sensor.measurement()
                    if data_record:
                        ft = [data_record.Fx, data_record.Fy, data_record.Fz,
                              data_record.Tx, data_record.Ty, data_record.Tz]
                        self._ft_data.emit(ft)
                    else:
                        time.sleep(0.05)
                except Exception as e:
                    print("ftSensor 解包错误：", e)
        except Exception as e:
            print("ftSensor 连接错误：", e)
        finally:
            if self.sensor:
                self._is_running = False
                self.sensor.stopStreaming()
                print("ftSensor 流式传输断开")
