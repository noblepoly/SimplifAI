from pydantic import BaseModel

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