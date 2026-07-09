from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List


def _parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


@dataclass
class TripRequest:
    destination: str
    start_date: str
    end_date: str
    budget: float
    interests: List[str]
    travelers: int = 1


class TravelPlannerAgent:
    """Simple planning agent that creates a practical day-by-day itinerary."""

    _activity_catalog: Dict[str, Dict[str, List[str]]] = {
        "culture": {
            "budget": ["Visit local museums on discounted-entry day", "Take a self-guided historical walking tour"],
            "standard": ["Join a guided city heritage tour", "Explore top museums and landmarks"],
            "premium": ["Book a private art and architecture tour", "Attend a cultural performance with premium seating"],
        },
        "food": {
            "budget": ["Try local street food", "Visit a neighborhood market"],
            "standard": ["Reserve a popular local restaurant", "Take a half-day food tasting tour"],
            "premium": ["Book a chef's tasting menu", "Take a private culinary workshop"],
        },
        "adventure": {
            "budget": ["Hike a nearby scenic trail", "Rent bikes for a self-guided route"],
            "standard": ["Join a group outdoor adventure excursion", "Take a guided kayak or bike tour"],
            "premium": ["Book a private adventure guide", "Take a premium full-day excursion"],
        },
        "relaxation": {
            "budget": ["Spend an afternoon in a public park", "Enjoy a beach or waterfront sunset"],
            "standard": ["Book a wellness pass at a local spa", "Take a scenic cruise"],
            "premium": ["Book a luxury spa day", "Reserve a premium wellness retreat session"],
        },
        "nightlife": {
            "budget": ["Explore live music venues with low cover fees", "Join a social pub walk"],
            "standard": ["Reserve a rooftop lounge experience", "Attend a curated nightlife district tour"],
            "premium": ["Book VIP club access", "Reserve a private evening entertainment package"],
        },
    }

    def generate_plan(self, request: TripRequest) -> Dict[str, object]:
        start = _parse_date(request.start_date)
        end = _parse_date(request.end_date)
        if end < start:
            raise ValueError("end_date must be on or after start_date")
        if request.travelers < 1:
            raise ValueError("travelers must be at least 1")

        day_count = (end - start).days + 1
        budget_tier = self._budget_tier(request.budget, request.travelers, day_count)
        interests = [interest.strip().lower() for interest in request.interests if interest.strip()]
        if not interests:
            interests = ["culture", "food", "relaxation"]

        itinerary = []
        for index in range(day_count):
            current_day = start + timedelta(days=index)
            focus = interests[index % len(interests)]
            activity = self._select_activity(focus, budget_tier, index)
            evening = self._select_activity("food", budget_tier, index + 1)
            itinerary.append(
                {
                    "day": index + 1,
                    "date": current_day.strftime("%Y-%m-%d"),
                    "theme": focus,
                    "morning": f"Explore {request.destination} highlights related to {focus}.",
                    "afternoon": activity,
                    "evening": evening,
                }
            )

        return {
            "destination": request.destination,
            "travelers": request.travelers,
            "dates": {"start": request.start_date, "end": request.end_date, "days": day_count},
            "budget": request.budget,
            "budget_tier": budget_tier,
            "interests": interests,
            "summary": (
                f"A {day_count}-day {budget_tier} itinerary for {request.destination} "
                f"designed around {', '.join(interests)} interests."
            ),
            "packing_tips": self._packing_tips(interests),
            "daily_itinerary": itinerary,
        }

    def _budget_tier(self, total_budget: float, travelers: int, day_count: int) -> str:
        per_person_daily = total_budget / max(travelers * day_count, 1)
        if per_person_daily < 100:
            return "budget"
        if per_person_daily < 250:
            return "standard"
        return "premium"

    def _select_activity(self, interest: str, budget_tier: str, seed: int) -> str:
        bucket = self._activity_catalog.get(interest, self._activity_catalog["culture"])
        activities = bucket[budget_tier]
        return activities[seed % len(activities)]

    @staticmethod
    def _packing_tips(interests: List[str]) -> List[str]:
        tips = ["Bring comfortable walking shoes", "Carry copies of important travel documents"]
        if "adventure" in interests:
            tips.append("Pack weather-appropriate activewear")
        if "relaxation" in interests:
            tips.append("Include light leisure wear for downtime")
        if "nightlife" in interests:
            tips.append("Pack one smart-casual evening outfit")
        return tips


def _render_markdown(plan: Dict[str, object]) -> str:
    lines = [
        f"# Travel Plan: {plan['destination']}",
        "",
        f"**Summary:** {plan['summary']}",
        f"**Dates:** {plan['dates']['start']} to {plan['dates']['end']} ({plan['dates']['days']} days)",
        f"**Budget Tier:** {plan['budget_tier']}",
        "",
        "## Daily Itinerary",
    ]

    for day in plan["daily_itinerary"]:
        lines.extend(
            [
                f"### Day {day['day']} - {day['date']} ({day['theme']})",
                f"- Morning: {day['morning']}",
                f"- Afternoon: {day['afternoon']}",
                f"- Evening: {day['evening']}",
                "",
            ]
        )

    lines.append("## Packing Tips")
    for tip in plan["packing_tips"]:
        lines.append(f"- {tip}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Travel Planner Agent")
    parser.add_argument("--destination", required=True)
    parser.add_argument("--start-date", required=True, help="Format: YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="Format: YYYY-MM-DD")
    parser.add_argument("--budget", required=True, type=float)
    parser.add_argument("--interests", default="culture,food,relaxation")
    parser.add_argument("--travelers", default=1, type=int)
    parser.add_argument("--json", action="store_true", dest="json_output")

    args = parser.parse_args()
    request = TripRequest(
        destination=args.destination,
        start_date=args.start_date,
        end_date=args.end_date,
        budget=args.budget,
        interests=args.interests.split(","),
        travelers=args.travelers,
    )

    plan = TravelPlannerAgent().generate_plan(request)
    if args.json_output:
        print(json.dumps(plan, indent=2))
    else:
        print(_render_markdown(plan))


if __name__ == "__main__":
    main()
