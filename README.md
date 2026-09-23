Mystery Delivery System

Approach

The program reads a json input file, assigns packages to the closest agent, simulates the deliveres, and writes the report.json file.

Assumptions
The following is a list of my assumptions when implementing this program:

1. Assignment is made according to the initial location of the agents. I thought it would make most sense that the assignment is made according to the initial positions of the agents. If the asignment followed the delivery sequence, it would have been too hard to optimize.
2. The assignment is performed before any delivery takes place.
3. An agent delivers the packages in the same order as they appear in the input JSON file. So the agent does not optimize the delivery route.
4. For each package delivered, a agent moves from their current position to the warehouse position, then to the destination.
5. An agent updates their current position to be the destination of a delivered package.
6. An agent only moves to a warehouse if they have to (because the next package has to be picked up there).
7. In case of a tie during the agent assignment process, we choose the agent with the lower index (i.e., agent_1 has higher priority over agent_2, and so on).
8. The efficiency is calculated as the total_distance / number_of_packages_delivered.
9. For agents that do not deliver any packages, their efficiency is null , and they are excluded from the best_agent calculation.
10. The best_agent is the one with the minimal efficiency (according to the efficiency definition in the description). Similar to the agent selection in case of a tie, the best_agent is selected by choosing the one with the lowest index in case of a tie.
11. The distance between two positions is calculated using the Euclidean distance. I computed everything with a floating point value and rounded the final value when writing the report to avoid errors due to repeated rounding.
12. Agents are not optimized in terms of delivery routes or package assignment. The problem description does not mention such optimization, and it was not implemented.
13. The base_case.json file does not have the same structure as the test cases. Therefore, there is an additional normalization step that converts the test cases to the same format as base_case.json .
14. Only the standard Python libraries were used (in this case, the json library).
Usage
The program can be run with the following command:

bash
python delivery_system.py

The program would read the base_case.json file and output the report.json file.

Tests

The test suite can be launched with the following command:
bash
python -m unittest -v
However, the test cases provided can also be directly inputted to generate_report() .

Bonus: ASCII Routes

The program also prints the delivery route of each agent in the terminal after generating the report.

Example:
A1: A1 -> W1 -> [10, 20] -> W2 -> [15, 25]