from rich.console import Console
from GamesTelemetry.BeamngTelemetryClient import OutgaugeServer
from dashboard import Dashboard
from time import sleep
from serial.tools.list_ports import comports
import os


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


class BeamngCli():
    def __init__(self):
        self.rc = Console()
        self.dashboard = Dashboard()
        self.beamng = OutgaugeServer()
        self.select_com_port()
        self.beamng.start()

    def select_com_port(self):
        while True:
            clearConsole()
            self.__annotations__list_ports()
            command = self.rc.input("Enter arduino port: ")
            if self.dashboard.open(port=command):
                self.rc.print(f"Serial port [green]{command}[/green] is open")
                break
            else:
                self.rc.print(
                    f"Can't open serial port [red]{command}[/red] !!")
                sleep(5)

    def update_dashboard(self):
        while True:
            self.check_ignition_on()
            self.dashboard.speed = self.beamng.speed * 3.6
            self.dashboard.RPM = self.beamng.RPM
            self.dashboard.fuel = self.beamng.fuel * 1000
            self.dashboard.coolant_temp = self. beamng.engtemp
            self.dashboard.oil_temp = self.beamng.oiltemp
            self.refresh_rate()

    def check_ignition_on(self):
        if self.dashboard.RPM > 0:
            self.dashboard.ignition = True
            self.dashboard.parking_lights = True
        else:
            self.dashboard.ignition = False
            self.dashboard.parking_lights = False

    def refresh_rate(self, hz=60):
        second = 1
        sleep(second / hz)

    def list_ports(self):
        ports = comports()
        for port in ports:
            self.rc.print(f"[green underline]{port.device}[/green underline]")


if __name__ == "__main__":

    beamng = BeamngCli()
    beamng.update_dashboard()
