import unittest

from travel_planner_agent import TripRequest, TravelPlannerAgent


class TravelPlannerAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = TravelPlannerAgent()

    def test_generates_expected_number_of_days(self):
        plan = self.agent.generate_plan(
            TripRequest(
                destination="Lisbon",
                start_date="2026-08-10",
                end_date="2026-08-12",
                budget=1500,
                interests=["culture", "food"],
                travelers=2,
            )
        )
        self.assertEqual(3, plan["dates"]["days"])
        self.assertEqual(3, len(plan["daily_itinerary"]))

    def test_invalid_date_range_raises(self):
        with self.assertRaises(ValueError):
            self.agent.generate_plan(
                TripRequest(
                    destination="Rome",
                    start_date="2026-08-12",
                    end_date="2026-08-10",
                    budget=900,
                    interests=["food"],
                    travelers=1,
                )
            )


if __name__ == "__main__":
    unittest.main()
