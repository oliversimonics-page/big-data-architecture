"""
IoT szenzoradat-generátor Big Data / HDFS gyakorlathoz.

Példák:

    python generate_sensors.py --size 100M

    python generate_sensors.py --size 1G \
        --output data/historical/sensors.json

    python generate_sensors.py --size 500M \
        --start-date 2025-01-01

    python generate_sensors.py --size 2GB \
        --start-date 2024-01-01T00:00:00
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime, timedelta, date


# ---------------------------------------------------------------------------
# Konfiguráció
# ---------------------------------------------------------------------------

SENSORS = [
    ("sensor-001", "Buda", "temperature", 20.0, 30.0),
    ("sensor-002", "Buda", "humidity", 30.0, 80.0),
    ("sensor-003", "Buda", "pressure", 980.0, 1040.0),
    ("sensor-004", "Pest", "temperature", 20.0, 30.0),
    ("sensor-005", "Pest", "humidity", 30.0, 80.0),
    ("sensor-006", "Pest", "pressure", 980.0, 1040.0),
    ("sensor-007", "Obuda", "temperature", 18.0, 29.0),
    ("sensor-008", "Obuda", "humidity", 35.0, 85.0),
    ("sensor-009", "Obuda", "pressure", 980.0, 1040.0),
    ("sensor-010", "Airport", "temperature", 15.0, 32.0),
]


# ---------------------------------------------------------------------------
# Méret feldolgozása
# ---------------------------------------------------------------------------

def parse_size(value: str) -> int:
    """
    Méret szöveg -> byte.

    Elfogadott példák:
        100
        100K
        100KB
        50M
        50MB
        2G
        2GB
        1T
        1TB
    """

    value = value.strip().upper()

    units = {
        "B": 1,
        "K": 1024,
        "KB": 1024,
        "M": 1024 ** 2,
        "MB": 1024 ** 2,
        "G": 1024 ** 3,
        "GB": 1024 ** 3,
        "T": 1024 ** 4,
        "TB": 1024 ** 4,
    }

    for unit in sorted(units.keys(), key=len, reverse=True):
        if value.endswith(unit):
            number = value[:-len(unit)]

            try:
                number = float(number)
            except ValueError:
                raise argparse.ArgumentTypeError(
                    f"Érvénytelen méret: {value}"
                )

            if number <= 0:
                raise argparse.ArgumentTypeError(
                    "A fájlméretnek pozitívnak kell lennie."
                )

            return int(number * units[unit])

    try:
        size = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Érvénytelen méret: {value}. "
            f"Példák: 100M, 1G, 500MB"
        )

    if size <= 0:
        raise argparse.ArgumentTypeError(
            "A fájlméretnek pozitívnak kell lennie."
        )

    return size


# ---------------------------------------------------------------------------
# Dátum feldolgozása
# ---------------------------------------------------------------------------

def parse_start_date(value: str) -> datetime:
    """
    Elfogadott formátumok:

        YYYY-MM-DD
        YYYY-MM-DDTHH:MM:SS
        YYYY-MM-DD HH:MM:SS
    """

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    raise argparse.ArgumentTypeError(
        f"Érvénytelen dátum: {value}. "
        f"Használj például: 2025-01-01 vagy 2025-01-01T12:00:00"
    )


# ---------------------------------------------------------------------------
# Szenzorrekord generálása
# ---------------------------------------------------------------------------

def generate_record(timestamp: datetime, sequence: int) -> dict:
    """
    Egyetlen IoT szenzorrekord létrehozása.
    """

    sensor_id, location, sensor_type, min_value, max_value = random.choice(
        SENSORS
    )

    value = random.uniform(min_value, max_value)

    # Néhány szenzortípusnál életszerűbb kerekítés
    if sensor_type == "temperature":
        value = round(value, 1)
    elif sensor_type == "humidity":
        value = round(value, 1)
    elif sensor_type == "pressure":
        value = round(value, 2)

    return {
        "timestamp": timestamp.isoformat(),
        "sensor_id": sensor_id,
        "location": location,
        "sensor_type": sensor_type,
        "value": value,
        "sequence": sequence,
    }


# ---------------------------------------------------------------------------
# Fő generáló függvény
# ---------------------------------------------------------------------------

def generate_file(
    output_path: str,
    target_size: int,
    start_datetime: datetime,
) -> None:

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    current_time = start_datetime

    # 1 másodpercenként generálunk egy eseményt.
    # Sok rekord keletkezik, ezért a fájl jól használható
    # Spark/Hadoop demonstrációhoz.
    time_step = timedelta(seconds=1)

    sequence = 0

    print()
    print("Szenzoradat-generálás")
    print("---------------------")
    print(f"Kimenet:       {output_path}")
    print(f"Célméret:      {target_size:,} byte")
    print(f"Kezdő dátum:   {start_datetime.isoformat()}")
    print()

    with open(output_path, "w", encoding="utf-8") as f:

        while True:

            record = generate_record(
                timestamp=current_time,
                sequence=sequence,
            )

            # JSON Lines formátum:
            # minden sor egy önálló JSON objektum.
            line = json.dumps(
                record,
                ensure_ascii=False,
                separators=(",", ":"),
            ) + "\n"

            f.write(line)

            sequence += 1
            current_time += time_step

            # Csak időnként ellenőrizzük a méretet.
            # Így nagy fájloknál nem kell minden egyes rekordnál
            # filesystem stat műveletet végrehajtani.
            if sequence % 1000 == 0:
                f.flush()

                current_size = f.tell()

                if current_size >= target_size:
                    break

        f.flush()

    final_size = os.path.getsize(output_path)

    print("Generálás kész.")
    print()
    print(f"Rekordok száma: {sequence:,}")
    print(f"Fájl mérete:    {final_size:,} byte")
    print(f"Célméret:       {target_size:,} byte")
    print(f"Időtartomány:   {start_datetime.isoformat()}")
    print(f"                -> {current_time.isoformat()}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "IoT szenzoradatokat generál a megadott fájlméret eléréséig."
        )
    )

    parser.add_argument(
        "--size",
        required=True,
        type=parse_size,
        help=(
            "A kívánt fájlméret. Például: "
            "100M, 500MB, 1G, 2GB"
        ),
    )

    parser.add_argument(
        "--output",
        default="sensors.json",
        help=(
            "A kimeneti JSON Lines fájl. "
            "Alapértelmezés: data/historical/sensors.json"
        ),
    )

    parser.add_argument(
        "--start-date",
        type=parse_start_date,
        default=None,
        help=(
            "A generálás kezdő dátuma. "
            "Például: 2025-01-01 vagy 2025-01-01T12:00:00. "
            "Ha nincs megadva, az aktuális nap 00:00:00 lesz."
        ),
    )

    args = parser.parse_args()

    if args.start_date is None:
        start_datetime = datetime.combine(
            date.today(),
            datetime.min.time(),
        )
    else:
        start_datetime = args.start_date

    generate_file(
        output_path=args.output,
        target_size=args.size,
        start_datetime=start_datetime,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGenerálás megszakítva.")
        sys.exit(1)
