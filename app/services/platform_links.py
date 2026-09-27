from urllib.parse import quote_plus


def search_links(
    query: str
) -> list[dict]:

    q = quote_plus(
        query.strip()
    )

    return [

        {
            "name": "Google Search",
            "url":
                f"https://www.google.com/search?q={q}"
        },

        {
            "name": "Amazon Search",
            "url":
                f"https://www.amazon.in/s?k={q}"
        },

        {
            "name": "Flipkart Search",
            "url":
                f"https://www.flipkart.com/search?q={q}"
        },
    ]