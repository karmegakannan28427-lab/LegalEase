"""
Text sanitization utilities.
"""

import html
import re


def sanitize_text(text: str) -> str:
    """
    Normalize generated text.
    """

    replacements = {

        "\u2018": "'",

        "\u2019": "'",

        "\u201c": '"',

        "\u201d": '"',

        "\u2013": "-",

        "\u2014": "-",

        "\u2026": "...",

        "\u00a0": " ",
    }


    result = text or ""


    for old, new in replacements.items():

        result = result.replace(
            old,
            new
        )


    # Remove extra spaces
    result = re.sub(
        r"[ \t]+",
        " ",
        result
    )


    # Remove excessive empty lines
    result = re.sub(
        r"\n{3,}",
        "\n\n",
        result
    )


    return result.strip()


def html_escape(text: str) -> str:
    """
    Escape text before displaying as HTML.
    """

    return html.escape(
        text or ""
    )