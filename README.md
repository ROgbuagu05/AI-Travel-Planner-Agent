# AI-Travel-Planner-Agent

A minimal AI Travel Planner Agent that generates a day-by-day itinerary from trip preferences.

## Features
- Creates a multi-day travel plan from destination, dates, budget, and interests
- Adapts recommendations to budget tier (budget/standard/premium)
- Outputs either Markdown (default) or JSON

## Usage

```bash
python3 /home/runner/work/AI-Travel-Planner-Agent/AI-Travel-Planner-Agent/travel_planner_agent.py \
  --destination "Paris" \
  --start-date "2026-09-01" \
  --end-date "2026-09-04" \
  --budget 2200 \
  --interests "culture,food,nightlife" \
  --travelers 2
```

For JSON output, add `--json`.

## Tests

```bash
python3 -m unittest -q /home/runner/work/AI-Travel-Planner-Agent/AI-Travel-Planner-Agent/test_travel_planner_agent.py
```
