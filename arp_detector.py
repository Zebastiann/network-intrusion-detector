from scapy.all import sniff, ARP
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

arp_table = {}

def log_alert(message):
    with open("arp_alert_log.txt", "a") as file:
        file.write(message + "\n")

def process_packet(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 2:
        ip = packet[ARP].psrc
        mac = packet[ARP].hwsrc

        if ip in arp_table:
            if arp_table[ip] != mac:
                alert = f"""
[ALERT] Possible ARP Spoofing Detected!
Time: {datetime.now()}
IP Address: {ip}
Original MAC: {arp_table[ip]}
New MAC: {mac}
"""
                print(Fore.RED + alert + Style.RESET_ALL)
                log_alert(alert)
            else:
                print(Fore.GREEN + f"[SAFE] {ip} is still mapped to {mac}")
        else:
            arp_table[ip] = mac
            print(Fore.CYAN + f"[NEW DEVICE] {ip} is mapped to {mac}")

def main():
    print(Fore.YELLOW + "Starting ARP Spoofing Detector...")
    print(Fore.YELLOW + "Monitoring ARP traffic. Press CTRL+C to stop.\n")

    sniff(store=False, prn=process_packet)

if __name__ == "__main__":
    main()
