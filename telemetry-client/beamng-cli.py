from rich.console import Console
from GamesTelemetry.BeamngTelemetryClient import OutgaugeServer
from dashboard import Dashboard
import os
from time import sleep
from serial.tools.list_ports import comports


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def list_ports():
    ports = comports()
    for port in ports:
        rc.print(f"[green underline]{port}[/green underline]")


if __name__ == "__main__":
    rc = Console()
    dashboard = Dashboard()
    beamng = OutgaugeServer(UDP_IP="127.0.0.1")
    beamng.start()

    while True:
        clearConsole()
        list_ports()
        command = rc.input("Enter arduino port: ")
        if dashboard.open(port=command):
            rc.print("[green]Serial port is open[/green]")
            break
        else:
            rc.print("[red]Cant open port[/red]")
            sleep(5)

    while True:
        try:
            if dashboard.RPM > 0:
                dashboard.ignition = True
                dashboard.parking_lights = True
            else:
                dashboard.ignition = False
                dashboard.parking_lights = False

            dashboard.speed = beamng.speed * 3.6
            dashboard.RPM = beamng.RPM
            dashboard.fuel = beamng.fuel * 1000
            dashboard.coolant_temp = beamng.engtemp
            dashboard.oil_temp = beamng.oiltemp

            dashboard.update()
        except:
            break
