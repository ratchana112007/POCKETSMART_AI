import json

import httpx

from app.config import settings


def _prompt(
    planner_type: str,
    data: dict
) -> str:

    return f"""
You are PocketSmart AI, a practical
budget and recommendation assistant.

Planner type:
{planner_type}

User input:

{json.dumps(data, indent=2)}

Return a useful recommendation in plain text with:

1. Summary
2. Budget allocation
3. Recommended categories/items
4. Practical tips
5. Shopping/search categories

Do not invent live product availability,
prices, ratings, or stock.

Use the user's currency-neutral budget
unless a currency is explicitly supplied.

Keep the answer concise and actionable.
""".strip()


def generate_recommendation(
    planner_type: str,
    data: dict
) -> str | None:

    if not settings.gemini_api_key:
        return None

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        f"{settings.gemini_model}:generateContent"
    )

    payload = {

        "contents": [
            {
                "parts": [
                    {
                        "text": _prompt(
                            planner_type,
                            data
                        )
                    }
                ]
            }
        ],

        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 1200
        }
    }

    try:

        with httpx.Client(
            timeout=25
        ) as client:

            response = client.post(
                url,
                params={
                    "key": settings.gemini_api_key
                },
                json=payload
            )

            response.raise_for_status()

            body = response.json()

            candidates = body.get(
                "candidates",
                []
            )

            if not candidates:
                return None

            parts = (
                candidates[0]
                .get("content", {})
                .get("parts", [])
            )

            text = "\n".join(
                part.get("text", "")
                for part in parts
            ).strip()

            return text or None

    except (
        httpx.HTTPError,
        ValueError,
        KeyError,
        TypeError
    ):
        return None