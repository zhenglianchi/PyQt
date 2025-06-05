import time

from PyQt5.QtCore import QThread, pyqtSignal
# import NET_FT
from .rpi_ati_net_ft import NET_FT
import pyads

class ForceThread(QThread):
    _ft_data = pyqtSignal(list)

    def __init__(self, ftSensorIp, tc3):
        super().__init__()
        self.ip = ftSensorIp
        self._is_running = False
        self.sensor = NET_FT(self.ip)
        self.sensor.set_tare_from_ft()
        self.setObjectName("ForceThread")
        self.tc3 = tc3

    def run(self):
        self._is_running = True
        try:
            self.sensor.start_streaming()

            while self._is_running:
                try:
                    success, ft, status = self.sensor.try_read_ft_streaming(0.01)
                    if success:
                        self._ft_data.emit(ft.tolist())
                        self.writeFT(ft.tolist())
                    else:
                        time.sleep(0.05)

                    # data_record = self.sensor.measurement()
                    # if data_record:
                    #     ft = [data_record.Fx, data_record.Fy, data_record.Fz,
                    #           data_record.Tx, data_record.Ty, data_record.Tz]
                    #     self._ft_data.emit(ft)
                    # else:
                    #     time.sleep(0.05)
                except Exception as e:
                    print("ftSensor 解包错误：", e)
        except Exception as e:
            print("ftSensor 连接错误：", e)
        finally:
            if self.sensor:
                self.sensor.stop_streaming()
                self._is_running = False
                print("ftSensor 流式传输断开")

    def stop(self):
        self.sensor.stop_streaming()
        self._is_running = False

    def writeFT(self, ft):
        if len(ft) == 6:
            self.tc3.write_by_name(f"SiJueSiFu.FX", round(ft[0],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.FY", round(ft[1],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.FZ", round(ft[2],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.TX", round(ft[3],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.TY", round(ft[4],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.TZ", round(ft[5],3), pyads.PLCTYPE_LREAL)
