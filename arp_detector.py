from scapy.all import ARP, Ether, srp
from colorama import Fore, Style, init
from datetime import datetime
import time

init(autoreset=True)

TARGET_IP = "10.1.1.1"
last_mac = None

def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    answered = srp(packet, timeout=2, verbose=False)[0]

    if answered:
        return answered[0][1].hwsrc
    return None

def main():
    global last_mac

    print(Fore.YELLOW + "Starting ARP Spoofing Detector...")
    print(Fore.YELLOW + f"Monitoring gateway IP: {TARGET_IP}")
    print(Fore.YELLOW + "Press CTRL+C to stop.\n")

    while True:
        current_mac = get_mac(TARGET_IP)

        if current_mac is None:
            print(Fore.RED + f"[WARNING] No ARP response from {TARGET_IP}")
        elif last_mac is None:
            last_mac = current_mac
            print(Fore.CYAN + f"[BASELINE] {TARGET_IP} is mapped to {current_mac}")
        elif current_mac != last_mac:
            alert = f"""
[ALERT] Possible ARP Spoofing Detected!
Time: {datetime.now()}
IP Address: {TARGET_IP}
Original MAC: {last_mac}
New MAC: {current_mac}
"""
            print(Fore.RED + alert + Style.RESET_ALL)

            with open("sample_logs/arp_alert_log.txt", "a") as file:
                file.write(alert + "\n")
        else:
            print(Fore.GREEN + f"[SAFE] {TARGET_IP} is still mapped to {current_mac}")

        time.sleep(3)

if __name__ == "__main__":
    main()
