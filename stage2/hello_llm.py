from google.genai import errors

from src.llm.client import ask


def main():
    print("\n--- 1. Plain question ---")
    print(ask("What is data analytics?"))

    print("\n--- 2. System instruction ---")
    print(
        ask(
            "Explain data analytics.",
            system="Explain concepts like a friendly teacher to a beginner.",
        )
    )

    print("\n--- 3. Temperature ---")
    print("Temperature 0.0:")
    print(ask("Give me one short definition of AI.", temperature=0.0))

    print("\nTemperature 1.0:")
    print(ask("Give me one short definition of AI.", temperature=1.0))

    print("\n--- 4. Hallucination example ---")
    print(
        ask(
            "What was the exact solar capacity of India on "
            "January 1, 1900? If reliable information is unavailable, "
            "say that you do not know."
        )
    )


if __name__ == "__main__":
    try:
        main()
    except errors.APIError as error:
        print(f"Gemini API error: {error}")