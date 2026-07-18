import requests
import ipaddress

def check():
    r = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
    data = r.json()
    
    target_ip = ipaddress.IPv6Address("2406:da1a:314:7101:651f:32b0:638b:d3c2")
    for item in data.get("ipv6_prefixes", []):
        prefix = ipaddress.IPv6Network(item.get("ipv6_prefix", ""))
        if target_ip in prefix:
            print(f"Match: {prefix} -> Region: {item.get('region')}, Service: {item.get('service')}")

if __name__ == "__main__":
    check()
