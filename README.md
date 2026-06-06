# SimplifAI: Deterministic Active Recall Engine

## Overview
SimplifAI is an educational technology prototype engineered to enforce the **Feynman Technique** of active recall. The application combats the illusion of competence by bypassing standard passive reading and open-ended chatbot interfaces. Instead, it forces users to articulate complex academic concepts from memory and mathematically evaluates their comprehension against a strictly parsed semantic baseline.

## Developer Context
* **Author:** Noble Poly
* **Academic Affiliation:** Electrical and Computer Engineering - TKM College of Engineering
* **Engineering Focus:** Highly constrained, deterministic AI orchestration and full-stack application lifecycle management.

## System Architecture & Tech Stack
The system completely abandons superficial, probabilistic LLM text generation in favor of strict data contracts and controlled generation. 
* **Frontend Presentation:** Streamlit
* **AI Reasoning Engine:** Google Gemini 2.5 Flash API
* **Data Validation & Typing:** Pydantic (Enforcing Object-Oriented JSON Schemas)
* **Secrets Management:** Python-dotenv

## Operational Boundaries
This prototype was developed under strict constraints to demonstrate core AI pipeline orchestration. 
* **Out of Scope:** Persistent database storage (e.g., PostgreSQL/MongoDB) and multi-user authentication are currently out of scope. 
* **State Management:** All application states and pedagogical data are managed temporarily in-memory utilizing Streamlit's advanced `st.session_state` API, resetting upon application refresh.

## Cost-Optimization & Lifecycle Mechanics
Streamlit operates on a fundamentally stateless, top-down execution paradigm, meaning the script reruns entirely upon every user interaction. 

To prevent catastrophic API token consumption and massive latency, the architecture leverages `st.session_state` as a persistent memory bank. When the language model extracts the initial Pydantic data objects, they are securely cached. The frontend subsequently renders the Active Recall form strictly from this safe, local cache. This clean separation of concerns completely eliminates redundant, costly network calls to the probabilistic backend while the user types their explanations.