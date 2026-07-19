"""
Service: Groq (Llama 3) wrapper — fast conversational + summarisation LLM.

Used by the Citizen Fraud Shield and the explanation node of the orchestrator.

Functions (planned)
-------------------
- summarise_message(text, lang)     -> concise summary of a panicked victim's
                                       message in the target language.
- generate_verdict_explanation(signals) -> human-readable "why this is/ isn't
                                       a scam" narrative for citizens/police.
- classify_scam_type(text)          -> quick LLM tag when zero-shot is
                                       insufficient (e.g., novel scripts).

Design notes
------------
- Use langchain-groq or a direct API call; GROQ_MODEL from settings.
- Keep prompts in app/prompts/ for easy iteration during the hackathon.

TODO
----
[ ] Implement the functions with tight, few-shot prompts.
[ ] Add multilingual system prompt covering the 12 target languages.
"""
