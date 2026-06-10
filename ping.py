import subprocess
from datetime import datetime
import sys

def get_filename():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "ips.txt"

def read_ips(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def is_up(ip):
    result = subprocess.run(
        ["ping", "-c", "1", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def check_all(ips):
    results = {}
    for ip in ips:
        results[ip] = "UP" if is_up(ip) else "DOWN"
    return results

def write_report(results):
    up_count = list(results.values()).count("UP")
    down_count = len(results) - up_count

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"report_{timestamp}.txt"

    with open(report_name, "w") as report:
        report.write(f"Ping report - {timestamp}\n")
        report.write(f"{up_count} UP, {down_count} DOWN\n")
        report.write("-" * 30 + "\n")
        for ip, status in results.items():
            line = f"{ip:<16} {status}"
            print(line)
            report.write(line + "\n")

    return report_name

def main():
    filename = get_filename()
    try:
        ips = read_ips(filename)
    except FileNotFoundError:
        print(f"Could not find {filename} - create it with one target per line.")
        sys.exit(1)

    results = check_all(ips)
    report_name = write_report(results)
    print(f"\nReport written to {report_name}")

if __name__ == "__main__":
    main()
