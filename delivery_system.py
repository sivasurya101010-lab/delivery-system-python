import json
import math
from pathlib import Path


def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_entities(entities):
    if isinstance(entities, dict):
        return entities

    return {entity["id"]: entity["location"] for entity in entities}


def normalize_data(data):
    return {
        "warehouses": normalize_entities(data["warehouses"]),
        "agents": normalize_entities(data["agents"]),
        "packages": [
            {
                **package,
                "warehouse": package.get("warehouse", package.get("warehouse_id")),
            }
            for package in data["packages"]
        ],
    }


def calculate_distance(point_a, point_b):
    return math.sqrt(
        (point_a[0] - point_b[0]) ** 2
        + (point_a[1] - point_b[1]) ** 2
    )


def assign_packages(data):
    assignments = {agent_id: [] for agent_id in data["agents"]}

    for package in data["packages"]:
        warehouse_location = data["warehouses"][package["warehouse"]]

        nearest_agent = min(
            data["agents"],
            key=lambda agent_id: (
                calculate_distance(data["agents"][agent_id], warehouse_location),
                agent_id,
            ),
        )

        assignments[nearest_agent].append(package)

    return assignments


def simulate_deliveries(data, assignments):
    report = {}

    for agent_id, packages in assignments.items():
        current_location = data["agents"][agent_id]
        total_distance = 0.0

        for package in packages:
            warehouse_location = data["warehouses"][package["warehouse"]]
            destination = package["destination"]

            total_distance += calculate_distance(
                current_location,
                warehouse_location,
            )
            total_distance += calculate_distance(
                warehouse_location,
                destination,
            )

            current_location = destination

        packages_delivered = len(packages)

        report[agent_id] = {
            "packages_delivered": packages_delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": round(total_distance / packages_delivered, 2)
            if packages_delivered
            else None,
        }

    active_agents = [
        agent_id
        for agent_id, details in report.items()
        if details["packages_delivered"] > 0
    ]

    best_agent = min(
        active_agents,
        key=lambda agent_id: (report[agent_id]["efficiency"], agent_id),
    ) if active_agents else None

    report["best_agent"] = best_agent
    return report


def generate_report(file_path):
    """Load input, assign packages, simulate deliveries, and build the report."""
    data = normalize_data(load_data(file_path))
    assignments = assign_packages(data)
    return simulate_deliveries(data, assignments)


def save_report(report, file_path="report.json"):
    """Save the final report as formatted JSON."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


if __name__ == "__main__":
    input_file = Path("base_case.json")
    output_file = Path("report.json")

    report = generate_report(input_file)
    save_report(report, output_file)
    print(f"Report saved to {output_file}")
