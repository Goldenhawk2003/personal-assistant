from samsung import SamsungTV
import os
from dotenv import load_dotenv
load_dotenv()


def main():
    tv = SamsungTV(os.environ["JARVIS_SAMSUNG_TV_IP"], token=os.environ["JARVIS_SAMSUNG_TV_TOKEN"], mac_address=os.environ["JARVIS_SAMSUNG_TV_MAC"])
    tv.connect()
    #tv.volume_up(10)
    #tv.power_on()
    tv.power_off()

if __name__ == "__main__":
    main()