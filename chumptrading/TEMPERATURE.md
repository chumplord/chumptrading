In the OpenAI API, the temperature parameter controls how “creative” or “random” the model’s responses are.

Here’s how it works:

- Low temperature (e.g., 0.0–0.3)
- More deterministic — the model will usually give the same output for the same input
- Sticks closely to the most probable words in its vocabulary
- Good for exact, reproducible code generation or factual answers
- Medium temperature (e.g., 0.5–0.7)
- Balances creativity and reliability
- Allows some variation in the output
- Good for iterating strategies where you want improvements but not complete randomness
- High temperature (e.g., 0.8–1.0+)
- Very creative and varied outputs
- More likely to explore unusual or riskier solutions
- Good for brainstorming many unique strategy ideas, but output can be less reliable or consistent

In Your Case (Strategy Evolution):

- When refining an existing strategy → use temperature=0.3–0.5
- This keeps changes incremental and preserves good logic from the parent strategy
- When creating first-generation strategies → use temperature=0.7–0.9
- This ensures a diverse initial population and encourages exploring different trading ideas