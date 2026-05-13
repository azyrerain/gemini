import google.genai as genai
import random, time

class GeminiClient:
    FREE_MODELS = [
        "models/gemini-3.1-flash-lite",
        "models/gemini-2.5-flash-lite",
        "models/gemini-2.0-flash-lite",
        "models/gemini-flash-lite-latest",
    ]

    def __init__(self, api_key: str, model: str = None):
        self.client = genai.Client(api_key=api_key)
        self.model = model or self.FREE_MODELS[0]

    def get_response(self, prompt: str) -> str:
        for model in self.FREE_MODELS:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                if "UNAVAILABLE" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    time.sleep(1 + random.random())
                    continue
                return f"Request failed on {model}: {e}"
        return "All free models are currently overloaded. Please try again later."


class SortingHatClient:
    HOUSES = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    def __init__(self, api_key: str):
        self.gemini = GeminiClient(api_key)

    def next_timeless_question(self, child_name: str, previous_answers: list[str]) -> str:
        prompt = f"""
        You are the Hogwarts Sorting Hat. Speak in its voice.
        The child is named {child_name}.
        Previous answers: {previous_answers}
        Ask ONE new thoughtful question that probes deeper into their personality,
        building on what they have already said.
        """
        return self.gemini.get_response(prompt).strip()

    def next_recency_question(self, child_name: str, previous_answers: list[str]) -> str:
        prompt = f"""
        You are the Hogwarts Sorting Hat. Speak in its voice.
        The child is named {child_name}.
        Previous answers so far: {previous_answers}
        Ask ONE probing but supportive question with RECENCY bias —
        meaning it should focus on something happening today or this week.
        It could be about feelings, experiences, relationships, schoolwork,
        or anything recent that reveals their current state of mind.
        """
        return self.gemini.get_response(prompt).strip()

    def run_interview(self, child_name: str) -> tuple[list[str], list[str]]:
        timeless_answers = []
        timeless_questions = []
        # Ask 3 timeless questions in sequence
        for _ in range(3):
            q = self.next_timeless_question(child_name, timeless_answers)
            timeless_questions.append(q)
            # In practice, you'd collect the child's answer interactively here
            ans = input(f"{q}\n> ")
            timeless_answers.append(ans)

        recency_answers = []
        recency_questions = []
        # Ask 2 recency-biased questions
        for _ in range(2):
            q = self.next_recency_question(child_name, timeless_answers + recency_answers)
            recency_questions.append(q)
            ans = input(f"{q}\n> ")
            recency_answers.append(ans)

        return timeless_answers + recency_answers, timeless_questions + recency_questions

    def sort_student(self, child_name: str, all_answers: list[str]) -> str:
        traits_summary = " ".join(all_answers)
        prompt = f"""
        You are the Hogwarts Sorting Hat. Speak in its voice.
        Based on these answers from {child_name}:
        {traits_summary}
        Choose one of Gryffindor, Hufflepuff, Ravenclaw, or Slytherin.
        Announce the decision dramatically, and explain how their strengths,
        weaknesses, opportunities, and threats influenced your choice.
        """
        response = self.gemini.get_response(prompt)
        if "overloaded" in response or "failed" in response:
            house = random.choice(self.HOUSES)
            return f"Hmm… tricky, tricky… but I see it now. Better be… {house}!"
        return response
