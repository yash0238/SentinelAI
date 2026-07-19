"""
Prompt templates for the Citizen Fraud Shield (Groq / Llama 3).

Keeping prompts in code (not scattered inline) lets us iterate quickly during
the hackathon and keep tone/safety consistent.

Planned prompts
---------------
- SYSTEM_MULTILINGUAL: sets role as a calm, trustworthy fraud-advisory
  assistant; instructs to reply in the user's language; never gives legal or
  financial advice, only guidance and NCRB reporting steps.
- CLASSIFY_SCAM_TYPE: few-shot prompt to tag scam scripts.
- SUMMARISE_PANIC_MESSAGE: condense a distressed message into key facts.
- EXPLAIN_VERDICT: turn fused signals into a plain-language explanation.

TODO
----
[ ] Draft and refine each template string.
[ ] Add few-shot examples for the 12 target languages where feasible.
"""
