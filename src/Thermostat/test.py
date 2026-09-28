from thermostat import UniluxThermostat

def main():
    thermostat = UniluxThermostat("192.168.18.13")
    thermostat.set_temperature(22.5)
    print(thermostat.get_info())


if __name__ == "__main__":
    main()