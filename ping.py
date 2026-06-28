import subprocess
import sys
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import shutil
import argparse

logger = logging.getLogger(__name__)


def read_inventory(filename):
    inventory = {}
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    name, ip = line.split(",")
                except ValueError:
                    logger.warning("Skipping malformed line: %s", line)
                    continue
                inventory[name.strip()] = ip.strip()
    except FileNotFoundError:
        logger.error("Inventory file not found: %s", filename)
        print(f"{filename} not found")
        sys.exit(1)
    return inventory


def is_up(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-w", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
    except subprocess.TimeoutExpired:
        return False
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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        filename="ping.log",
    )

    parser = argparse.ArgumentParser(description="Ping a named inventory of hosts")
    parser.add_argument(
        "inventory",
        nargs="?",
        default="inventory.txt",
        help="CSV inventory file (name,ip per line). Defaults to inventory.txt",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=50,
        help="Number of parallel ping workers (default: 50)",
    )
    args = parser.parse_args()

    inventory = read_inventory(args.inventory)

    if shutil.which("ping") is None:
        logger.error("ping binary not found on PATH")
        sys.exit(1)

    names = list(inventory.keys())
    ips = list(inventory.values())

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        statuses = executor.map(is_up, ips)	#parallel, order preserved

        results = {}
        for name, ip, up in zip(names, ips, statuses):
            status = "UP" if up else "DOWN"
            results[name] = {"ip": ip, "status": status}
            print(f"{name:<12} ({ip:<15}) {status}")
            if status == "UP":
                logger.info("%s is UP", name)
            else:
                logger.warning("%s is DOWN (no ICMP reply)", name)

    report_name = write_report(results)
    print(f"\nReport written to {report_name}")


if __name__ == "__main__":
    main()
