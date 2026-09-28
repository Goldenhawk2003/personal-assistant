from firestick import FireStick

firestick = FireStick(
    ip="192.168.18.11",
    adb_path=r"C:\Users\ammar\Downloads\platform-tools-latest-windows\platform-tools\adb.exe",
)


def main():
    # firestick.connect()
    firestick.home()
    # firestick.start_app("com.netflix.ninja")
    # firestick.play_pause()


if __name__ == "__main__":
    main()