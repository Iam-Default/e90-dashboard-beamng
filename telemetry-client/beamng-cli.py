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
        clearConsole()
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
            if command.lower() == "none":
                break
            try:
                self.dashboard.open(port=command)
                self.rc.print(f"Serial port [green]{command}[/green] is open")
                break
            except:
                self.rc.print(
                    f"Can't open serial port [red]{command}[/red] !!")
                sleep(2)

    def update_dashboard(self):
        try:
            while True:
                self.check_ignition_on()
                self.dashboard.speed = self.beamng.speed * 3.6
                self.dashboard.RPM = self.beamng.RPM
                self.dashboard.fuel = self.beamng.fuel * 1000
                self.dashboard.coolant_temp = self. beamng.engtemp
                self.dashboard.oil_temp = self.beamng.oiltemp
                self.dashboard.oil_pressure = self.beamng.oilpress
                self.dashboard.boost_pressure = self.beamng.turbo
                self.dashboard.gear = self.beamng.gear
                self.dash_lights()
                self.console_output()
                self.refresh_rate()
        except KeyboardInterrupt:
            self.rc.print(self.exit_message)

    def check_ignition_on(self):
        self.dashboard.ignition = self.dashboard.parking_lights = not self.dashboard.battery_warning

    def dash_lights(self):
        shift_light = 1
        high_beam = 2
        handbrake = 4
        pit_speed_limit = 8
        tc_active = 16
        left_turn_signal = 32
        right_turn_signal = 64
        hazard_light = 128
        oil_pressure_warning = 256
        battery_warning = 512
        abs_active = 1024

        dl = self.beamng.dashlights

        self.dashboard.shift_light = bool(dl & shift_light)
        self.dashboard.handbrake = bool(dl & handbrake)
        self.dashboard.tc_enabled = bool(dl & tc_active)
        self.dashboard.oil_pressure_warning = bool(dl & oil_pressure_warning)
        self.dashboard.battery_warning = bool(dl & battery_warning)
        self.dashboard.abs_enabled = bool(dl & abs_active)

        if dl & hazard_light:
            self.dashboard.blinkers = self.dashboard.BLINKERS_HAZZARD
        elif dl & left_turn_signal:
            self.dashboard.blinkers = self.dashboard.BLINKERS_LEFT
        elif dl & right_turn_signal:
            self.dashboard.blinkers = self.dashboard.BLINKERS_RIGHT
        else:
            self.dashboard.blinkers = self.dashboard.BLINKERS_OFF

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
                f"{self.dashboard.speed} Km/h, {self.dashboard.RPM} RPM/min, Boost {self.dashboard.boost_pressure} Bar, Oil press {self.dashboard.oil_pressure} Bar, Oil temp {self.dashboard.oil_temp} C, Coolant temp {self.dashboard.coolant_temp} C")
            self.rc.print(
                f"Ignition {self.dashboard.ignition}, Shift light {self.dashboard.shift_light}, Handbrake {self.dashboard.handbrake},  Blinkers {self.dashboard.blinkers}")


if __name__ == "__main__":

    beamng = BeamngCli()
    beamng.update_dashboard()
