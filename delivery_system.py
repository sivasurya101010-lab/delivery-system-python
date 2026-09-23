import json
import math
from pathlib import Path


def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_entities(entities):
    if isinstance(entities, dict):
        return entities

    result = {}

    # Convert list format into dictionary format
    for entity in entities:
        result[entity["id"]]= entity["location"]

    return result


def normalize_data(data):
    packages = []

    for package in data["packages"]:
        package_data = package.copy()
        package_data["warehouse"] = package.get("warehouse",package.get("warehouse_id"))
        packages.append(package_data)

    return {
        "warehouses": normalize_entities(data["warehouses"]),
        "agents": normalize_entities(data["agents"]),
        "packages":packages,
    }


def calculate_distance(point_a, point_b):
    # Calculate the Euclidean distance between two points
    return math.sqrt(( point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2 )


def assign_packages(data):
    assignments = {}

    for agent_id in data["agents"]:
        assignments[agent_id]=[]

    # Assign each package to the nearest agent
    for package in data["packages"]:
        warehouse_location= data["warehouses"][package["warehouse"]]

        nearest_agent = None
        shortest_distance = float("inf")

        for agent_id in data["agents"]:
            agent_location = data["agents"][agent_id]

            distance = calculate_distance(agent_location,warehouse_location)

            if distance < shortest_distance:
                shortest_distance = distance
                nearest_agent = agent_id

        assignments[nearest_agent].append(package)

    return assignments


def simulate_deliveries(data, assignments):
    report = {}

    for agent_id in assignments:
        packages = assignments[agent_id]
        current_location = data["agents"][agent_id]
        total_distance = 0.0

        for package in packages:
            warehouse_location = data["warehouses"][package["warehouse"]]
            destination = package["destination"]

            # Agent travels from current location to warehouse
            total_distance += calculate_distance(current_location,warehouse_location)

            # Agent travels from warehouse to destination
            total_distance += calculate_distance(warehouse_location,destination)

            current_location = destination

        packages_delivered = len(packages)

        if packages_delivered:
            efficiency = total_distance / packages_delivered

        else:
            efficiency = None

        report[agent_id] = {
            "packages_delivered": packages_delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": round(efficiency, 2) if efficiency is not None else None
        }


    # Find the agent with the lowest average distance per package
    active_agents = []

    for agent_id in report:
        if report[agent_id]["packages_delivered"] > 0:
            active_agents.append(agent_id)

    if active_agents:
        best_agent =active_agents[0]

        for agent_id in active_agents:
            if report[agent_id]["efficiency"] < report[best_agent]["efficiency"]:
                best_agent= agent_id
    else:
        best_agent=None

    report["best_agent"]= best_agent

    return report


def generate_report(file_path):
    data = load_data(file_path)
    data = normalize_data(data)

    assignments = assign_packages(data)

    return simulate_deliveries(data, assignments)


def save_report(report, file_path="report.json"):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


if __name__ == "__main__":
    input_file = Path("base_case.json")
    output_file = Path("report.json")

    report = generate_report(input_file)
    save_report(report, output_file)

    print(f"Report saved to {output_file}")