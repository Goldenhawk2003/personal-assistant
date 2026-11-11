import subprocess


class FireStick:
    def __init__(self, ip: str, adb_path: str):
        self.ip = ip
        self.adb_path = adb_path

    FIRESTICK_APPS = {
        "netflix": "com.netflix.ninja",
        "prime": "com.amazon.firebat",
        "prime video": "com.amazon.firebat",
        "youtube": "com.amazon.firetv.youtube",
        "disney": "com.disney.disneyplus",
        "disney plus": "com.disney.disneyplus",
    }
    def connect(self):
        subprocess.run(
            [self.adb_path, "connect", f"{self.ip}:5555"],
            check=True,
        )

    def _run_shell(self, *args):
        subprocess.run(
            [
                self.adb_path,
                "-s",
                f"{self.ip}:5555",
                "shell",
                *args,
            ],
            check=True,
        )

    def home(self):
        self._run_shell("input", "keyevent", "KEYCODE_HOME")

    def back(self):
        self._run_shell("input", "keyevent", "KEYCODE_BACK")
    
    def start_app(self, package_name: str):
        self._run_shell("monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1")

    def start_app_by_name(self, app_name: str):
        app_name = app_name.lower().strip()

        package_name = self.FIRESTICK_APPS.get(app_name)

        if package_name is None:
            raise ValueError(f"Unknown app: {app_name}")

        self.start_app(package_name)

    def play_pause(self):
        self._run_shell(
            "input",
            "keyevent",
            "KEYCODE_MEDIA_PLAY_PAUSE",
        )