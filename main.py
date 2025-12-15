"""
AI Writing Assistant
--------------------
Features:
- Verifies Gemini connection before continuing
- Generates outline, introduction, body, and conclusion for essays
- Clean CLI interface with colorized output
"""
import sys
import google.generativeai as g
from colorama import init, Fore
import config  # :white_check_mark: non-negotiable import
# Initialize color output
init(autoreset=True)
# --- Step 1: Load API key safely ---
API_KEY = getattr(config, "GEMINI_API_KEY", "").strip()
if not API_KEY or not API_KEY.startswith("AIza"):
    print(Fore.RED + ":x: Error: Please set a valid GEMINI_API_KEY in config.py before running.")
    sys.exit(1)
# Configure Gemini
g.configure(api_key=API_KEY)
# --- Step 2: Utility function to test API key ---
def gemini_ready_check() -> bool:
    """Verify that the Gemini API key and model are reachable."""
    try:
        model = g.GenerativeModel("gemini-2.0-flash")
        resp = model.generate_content("ping")
        if getattr(resp, "text", "").strip():
            print(Fore.GREEN + ":white_check_mark: Gemini API key verified successfully.\n")
            return True
        print(Fore.YELLOW + ":warning: Connected, but empty response. Continuing anyway.\n")
        return True
    except Exception as e:
        print(Fore.RED + ":x: Gemini API key verification failed.\n")
        print(Fore.YELLOW + f"Reason: {e}\n")
        print(Fore.CYAN + ":compass: Fix checklist:")
        print(Fore.WHITE + "- Ensure you copied the full key from Google AI Studio.")
        print(Fore.WHITE + "- Enable 'Generative Language API' for your project.")
        print(Fore.WHITE + "- Remove API restrictions while testing.\n")
        return False
# --- Step 3: Function to generate responses ---
def generate_response(prompt, temperature=0.3):
    """Generate text using Gemini 2.0 API."""
    try:
        model = g.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            prompt,
            generation_config=g.types.GenerationConfig(temperature=temperature)
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"
# --- Step 4: Collect user inputs ---
def get_essay_details():
    print(Fore.CYAN + "\n=== AI Writing Assistant ===\n")
    topic = input(Fore.YELLOW + "What is the topic of your essay? ")
    essay_type = input(Fore.YELLOW + "Essay type (e.g., Argumentative, Expository, Descriptive, Persuasive): ")
    print(Fore.GREEN + "\nSelect essay word count:")
    print(Fore.GREEN + "1. 300 words")
    print(Fore.GREEN + "2. 900 words")
    print(Fore.GREEN + "3. 1200 words")
    print(Fore.GREEN + "4. 2000 words")
    word_count_choice = input(Fore.YELLOW + "Choice (1-4): ")
    length = {"1": "300", "2": "900", "3": "1200", "4": "2000"}.get(word_count_choice, "300")
    target_audience = input(Fore.YELLOW + "Target audience (e.g., High school students, College professors): ")
    specific_points = input(Fore.YELLOW + "Any specific points to include? ")
    stance = input(Fore.YELLOW + "Your stance (For, Against, Neutral): ")
    references = input(Fore.YELLOW + "Any quotes or references to include? ")
    writing_style = input(Fore.YELLOW + "Preferred writing style (Formal, Conversational, Academic, Creative): ")
    outline_needed = input(Fore.YELLOW + "Would you like the AI to suggest an outline first? (Yes/No): ").lower()
    return {
        "topic": topic,
        "essay_type": essay_type,
        "length": length,
        "target_audience": target_audience,
        "specific_points": specific_points,
        "stance": stance,
        "references": references,
        "writing_style": writing_style,
        "outline_needed": outline_needed
    }
# --- Step 5: Generate essay content ---
def generate_essay_content(details):
    try:
        temperature = float(input(Fore.YELLOW + "Enter temperature (0.2=structured, 0.7=creative): "))
    except ValueError:
        temperature = 0.3
    # Optional outline
    if details["outline_needed"] == "yes":
        outline_prompt = (
            f"Create a clear outline for a {details['essay_type']} essay about '{details['topic']}', "
            f"written in a {details['writing_style']} tone for {details['target_audience']}."
        )
        outline = generate_response(outline_prompt, temperature)
        print(Fore.CYAN + "\n=== Generated Outline ===")
        print(Fore.GREEN + outline)
    # Introduction
    intro_prompt = (
        f"Write an introduction for a {details['essay_type']} essay on '{details['topic']}' "
        f"that supports a {details['stance']} stance. Use a {details['writing_style']} tone "
        f"for {details['target_audience']}."
    )
    introduction = generate_response(intro_prompt, temperature)
    print(Fore.CYAN + "\n=== Generated Introduction ===")
    print(Fore.GREEN + introduction)
    # Body
    body_style = input(Fore.YELLOW + "Generate body step-by-step or full draft? (Step/Full): ").lower()
    if body_style.startswith("f"):
        body_prompt = (
            f"Write the full body (about {details['length']} words) of a {details['essay_type']} essay "
            f"on '{details['topic']}', taking a {details['stance']} stance. "
            f"Maintain a {details['writing_style']} tone for {details['target_audience']}."
        )
        body = generate_response(body_prompt, temperature)
        print(Fore.CYAN + "\n=== Generated Full Body ===")
        print(Fore.GREEN + body)
    else:
        step_prompt = (
            f"Write the essay body for '{details['topic']}' step-by-step, explaining each argument and evidence clearly."
        )
        step_body = generate_response(step_prompt, temperature)
        print(Fore.CYAN + "\n=== Generated Step-by-Step Body ===")
        print(Fore.GREEN + step_body)
    # Conclusion
    conclusion_prompt = (
        f"Write a conclusion for a {details['essay_type']} essay on '{details['topic']}', "
        f"summarizing the key arguments and reinforcing a {details['stance']} stance."
    )
    conclusion = generate_response(conclusion_prompt, temperature)
    print(Fore.CYAN + "\n=== Generated Conclusion ===")
    print(Fore.GREEN + conclusion)
# --- Step 6: Feedback ---
def feedback_and_refinement():
    satisfaction = input(Fore.YELLOW + "\nRate satisfaction (1–5): ")
    if satisfaction.strip() != "5":
        feedback = input(Fore.YELLOW + "What should be improved (tone, clarity, structure)? ")
        print(Fore.CYAN + f"\nThank you! Feedback noted: {feedback}")
    else:
        print(Fore.CYAN + "\n:tada: Glad you liked it!")
# --- Step 7: Main entry point ---
def run_activity():
    print(Fore.CYAN + "\nWelcome to the AI Writing Assistant!\n")
    if not gemini_ready_check():
        sys.exit(1)
    details = get_essay_details()
    generate_essay_content(details)
    feedback_and_refinement()
if __name__ == "__main__":
    run_activity()