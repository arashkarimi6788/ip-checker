import subprocess
from datetime import datetime
import sys

def read_inventory(filename):
    inv = {}
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    name, ip = line.split(",")
                except ValueError:
                    print(f"Skipping bad line: {line}")
                    continue
                inv[name] = ip
    except FileNotFoundError:
        print(f"Error: could not find {filename}")
        sys.exit(1)
    return inv

def is_up(ip):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def write_report(results):
    up_count = 0
    for data in results.values():
        if data["status"] == "UP":
            up_count += 1
    down_count = len(results) - up_count

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"report_{timestamp}.txt"
    with open(report_name, "w") as report:
        report.write(f"Ping report - {timestamp}\n")
        report.write(f"{up_count} UP, {down_count} DOWN\n")
        report.write("-" * 40 + "\n")
        for name, data in results.items():
            line = f"{name:<12} ({data['ip']:<15}) {data['status']}"
            report.write(line + "\n")
    return report_name

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "inventory.txt"
    inventory = read_inventory(filename)

    results = {}
    for name, ip in inventory.items():
        status = "UP" if is_up(ip) else "DOWN"
        results[name] = {"ip": ip, "status": status}
        print(f"{name:<12} ({ip:<15}) {status}")

    report_name = write_report(results)
    print(f"\nReport written to {report_name}")

if __name__ == "__main__":
    main()
