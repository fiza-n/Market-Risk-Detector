frontend/ — Everything the buyer sees: the paste-a-listing form, the results screen with the score/flags, the feedback buttons, and the shareable result card. Owner: Ummama.
backend/routes/ — The HTTP endpoints the frontend calls. Receives the submitted listing, triggers your scam analysis and Fiza's price analysis, saves the final result, and handles the feedback vote. Owner: Ummama.
backend/price_intelligence/ — Compares a listing's price against typical price ranges for its category and flags it if it's abnormally high or low. Owner: Fiza.
backend/scam_detection/ — Sends the listing text to the LLM (Groq/Llama), applies the scam-pattern logic (advance-payment pressure, JazzCash/EasyPaisa demands, Urdu-English mixed red flags), and returns a risk score plus flags. Also where the feedback loop that improves detection lives. Owner: you (Javeria).
backend/db/ — Handles the actual MongoDB connection and reading/writing data (submissions, feedback, price reference data). Owner: Fiza.
backend/merge/ — Takes your score and Fiza's score, combines them into one final score/verdict/flag-list matching the required output shape. Owner: not yet decided.
backend/tests/ — Automated tests for the above. Shared, everyone tests their own part.
docs/ — The two spec documents everyone builds from. Shared, reference only, not code.