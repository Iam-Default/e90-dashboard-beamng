from rich.console import Console
from GamesTelemetry.BeamngTelemetryClient import OutgaugeServer
from dashboard import Dashboard
import os
from time import sleep
from serial.tools.list_ports import comports


def check_ip(ip):
    numbers = ip.split(".")

    if len(numbers) > 4 or len(numbers) < 4:
        return False

    for number in numbers:
        if int(number) < 0 or int(number) > 255:
            return False
    return True


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

    clearConsole()

    while True:
        command = rc.input("Enter ip: ")
        clearConsole()
        if command.lower() == "exit":
            break

        if check_ip(command):
            beamng = OutgaugeServer(UDP_IP=command)
            beamng.start()
            break
        else:
            rc.print("[red]Incorrect ip address[/red]")

    sleep(5)

    while True:
        clearConsole()
        list_ports()
        command = rc.input("Enter arduino port: ")
        if dashboard.open(port=command):
            dashboard.ignition = True
            rc.print("[green]Serial port is open[/green]")
            break
        else:
            rc.print("[red]Cant open port[/red]")
            sleep(5)

    while True:
        try:
            dashboard.speed = beamng.speed
            dashboard.RPM = beamng.RPM
            dashboard.fuel = beamng.fuel
            dashboard.update()
        except:
            break
