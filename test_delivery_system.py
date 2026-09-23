import unittest
from pathlib import Path

from delivery_system import generate_report


BASE_DIR = Path(__file__).parent
TEST_CASE_DIR = BASE_DIR


class DeliverySystemTestCase(unittest.TestCase):

    def test_all_packages_are_assigned(self):
        for number in range(1, 11):
            report = generate_report(TEST_CASE_DIR / f"test_case_{number}.json")
            total_packages = sum(
                details["packages_delivered"]
                for agent_id, details in report.items()
                if agent_id != "best_agent"
            )
            with open(TEST_CASE_DIR / f"test_case_{number}.json", "r", encoding="utf-8") as file:
                import json
                input_data = json.load(file)
            self.assertEqual(total_packages, len(input_data["packages"]))

    def test_base_case(self):
        report = generate_report(BASE_DIR / "base_case.json")
        self.assertEqual(
            sum(
                details["packages_delivered"]
                for agent_id, details in report.items()
                if agent_id != "best_agent"
            ),
            5,
        )

    def test_best_agent_is_not_idle(self):
        for number in range(1, 11):
            report = generate_report(TEST_CASE_DIR / f"test_case_{number}.json")
            best_agent = report["best_agent"]
            self.assertGreater(report[best_agent]["packages_delivered"], 0)


if __name__ == "__main__":
    unittest.main()
