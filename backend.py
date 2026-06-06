import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
# 1. Load the secret API key from your .env file into the system memory
load_dotenv(override=True) 

# 2. Initialize the AI client (it automatically detects the key in memory)
client = genai.Client()
# Schema to extract a single academic concept
class ConceptExtraction(BaseModel):
    concept_title: str
    brief_definition: str

# Schema to force the model to return a list of multiple concepts
class ExtractionResponse(BaseModel):
    extracted_concepts: list[ConceptExtraction]

# Schema for the final semantic grading
class EvaluationResult(BaseModel):
    overall_score: int
    identified_gaps: list[str]
    hallucinations: list[str]
    feynman_feedback: str
# 3. The Deterministic Extraction Function
def extract_source_concepts(text: str) -> ExtractionResponse:
    prompt = f"Extract the core academic concepts from the following text. Be concise.\n\nText: {text}"
    
    # We force the model into JSON mode and pass our Pydantic schema
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ExtractionResponse,
        ),
    )
    
    # The SDK automatically parses the JSON back into our strict Python object
    return response.parsed

# This is where the evaluation logic will go once the user submits their explanations in the Streamlit app
def evaluate_user_explanations(concepts: list, explanations: dict) -> EvaluationResult:
    # Build a structured prompt detailing both the ground-truth and the user's attempt
    formatted_comparison = ""
    for idx, concept in enumerate(concepts):
        title = concept.concept_title
        original_def = concept.brief_definition
        user_attempt = explanations.get(title, "").strip() or "No explanation provided."
        
        formatted_comparison += f"Concept: {title}\n"
        formatted_comparison += f"Target Definition: {original_def}\n"
        formatted_comparison += f"User's Explanation: {user_attempt}\n"
        formatted_comparison += "--- \n"

    evaluation_prompt = f"""
    Act as an elite academic mentor grading a student's understanding using the Feynman Technique. 
    Review the following concepts. Compare the student's explanation against the target definition.
    
    Identify:
    1. Knowledge Gaps: Important facts or core ideas from the target definition that the student left out.
    2. Hallucinations: Factually incorrect statements or fabricated ideas introduced by the student that aren't true.
    3. Constructive Feedback: A friendly, encouraging explanation of what they missed or got wrong, explaining it simply as if they are 12 years old.
    4. Provide an overall score from 0 to 100 based on their performance across all terms.

    Data to evaluate:
    {formatted_comparison}
    """

    # Force the model to return our strict evaluation schema
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=evaluation_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EvaluationResult,
        ),
    )
    
    return response.parsed
# 4. Local Terminal Verification (Testing Block)
if __name__ == "__main__":
    sample_text = "Photosynthesis is the process used by plants to convert light energy into chemical energy. Cellular respiration is the process of breaking down sugar into a form that the cell can use as energy."
    
    print("Sending request to Gemini...\n")
    structured_data = extract_source_concepts(sample_text)
    
    # We can now confidently iterate over the object!
    for concept in structured_data.extracted_concepts:
        print(f"Title: {concept.concept_title}")
        print(f"Definition: {concept.brief_definition}\n")