from rich.console import Console
from GamesTelemetry.BeamngTelemetryClient import OutgaugeServer
from dashboard import Dashboard
from time import sleep, time
from serial.tools.list_ports import comports
import os


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


class BeamngCli():
    def __init__(self):
        self.previous_time = time()
        self.console_update_interval = 0.5
        self.exit_message = "Exit succesfull"
        self.rc = Console()
        self.dashboard = Dashboard()
        self.beamng = OutgaugeServer()
        self.console_output_enable()
        self.select_com_port()
        self.beamng.start()

    def select_com_port(self):
        while True:
            clearConsole()
            self.list_ports()
            command = self.rc.input("Enter arduino port: ")
            if self.dashboard.open(port=command):
                self.rc.print(f"Serial port [green]{command}[/green] is open")
                break
            else:
                self.rc.print(
                    f"Can't open serial port [red]{command}[/red] !!")
                sleep(5)

    def update_dashboard(self):
        try:
            while True:
                self.check_ignition_on()
                self.dashboard.speed = self.beamng.speed * 3.6
                self.dashboard.RPM = self.beamng.RPM
                self.dashboard.fuel = self.beamng.fuel * 1000
                self.dashboard.coolant_temp = self. beamng.engtemp
                self.dashboard.oil_temp = self.beamng.oiltemp
                self.console_output()
                self.refresh_rate()
        except KeyboardInterrupt:
            self.rc.print(self.exit_message)

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

    def console_output_enable(self):
        command = self.rc.input("Enable console output: ").lower()
        if command == "y":
            self.console_output_enabled = True
            return
        self.console_output_enabled = False

    def console_update_required(self):
        self.current_time = time()
        if (self.current_time - self.previous_time) > self.console_update_interval:
            self.previous_time = self.current_time
            return True
        return False

    def console_output(self):
        if self.console_output_enabled and self.console_update_required():
            clearConsole()
            self.rc.print(
                f"{self.dashboard.speed} Km/h, {self.dashboard.RPM} RPM/min")


if __name__ == "__main__":

    beamng = BeamngCli()
    beamng.update_dashboard()
