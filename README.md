# Mystery Delivery System

## Approach

The program reads a JSON input file, assigns each package to the nearest delivery agent, simulates the deliveries, and writes a `report.json` file.

## Assumptions

1. Packages are assigned using the agents' **initial locations** and the warehouse location. Agent movement during simulation does not change package assignment.
2. All assignments are completed before delivery simulation begins.
3. Packages assigned to an agent are delivered in the same order they appear in the input JSON.
4. For each package, an agent travels from its current location to the package warehouse and then from the warehouse to the destination.
5. After delivering a package, the agent's current location becomes that package's destination.
6. An agent does not return to a warehouse after a delivery unless the next assigned package requires a warehouse visit.
7. If two agents are equally close to a warehouse, the agent with the lexicographically smaller ID is selected. This provides deterministic tie-breaking.
8. Efficiency is `total_distance / packages_delivered`.
9. An agent with zero deliveries has no meaningful efficiency, so its efficiency is represented as `null` and it is not considered for `best_agent`.
10. `best_agent` is the active agent with the lowest efficiency. Equal efficiencies are resolved using the same deterministic agent-ID tie-breaker.
11. Distances are calculated using Euclidean distance. Intermediate calculations keep full precision; only final report values are rounded to two decimal places.
12. No route optimization or workload balancing is performed because the specification does not define either behavior.
13. The supplied `base_case.json` and test cases use different container formats for warehouses/agents. The implementation normalizes both formats into the same internal representation.
14. The implementation uses Python's standard `json` module for JSON parsing; no third-party dependency is required.

## Running

```bash
python delivery_system.py
```

This reads `base_case.json` and creates `report.json`.

## Running tests

```bash
python -m unittest -v
```

The supplied test cases can also be passed directly to `generate_report()`.
