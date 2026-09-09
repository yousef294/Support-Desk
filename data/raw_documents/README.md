Raw Documents — Knowledge Base Source
This folder holds the source PDFs ingested by the RAG pipeline. The notebook(notebooks/rag_pipeline.ipynb) reads everything placed here, chunks it, embeds it,and writes the index to backend/data/vector_store/.

The PDFs themselves are gitignored (too large for the repo); only this READMEis tracked. Place the files locally after cloning.

Contents
Product Catalog	50 products — brand, category, price, description, key features (electronics, home, kitchen, health, sports, travel, etc.)
Customer Service FAQ	60 Q&As on account management, orders & payments, shipping & delivery, returns & refunds
How-To Guides	20 step-by-step guides across customer service, product discovery, account security & seller support
Document Details

1. Product Catalog (50 products)
Structured product listings with Brand / Category / Price / Description / KeyFeatures. Covers categories such as Electronics > Audio, Smart Home, MobileAccessories, Wearable Tech, Kitchen > Appliances, Furniture, Luggage & Travel,Sports & Outdoors, and more. Good for questions like "Which headphones supportnoise canceling?" or "How much is the smart thermostat?"

2. Customer Service FAQ (60 questions)
Question-and-answer pairs organized into four sections:

. Account Management (1–15)
. Orders and Payments (16–35)
. Shipping and Delivery (36–50)
. Returns and Refunds (51–60)
. Good for short factual questions like "How long do refunds take?"

3. How-To Guides (20 guides)
Numbered, multi-step procedures organized into four sections:

. Customer Service Automation (1–5) — canceling shipped orders, missing packages, damaged-item refunds, subscription payment updates, changing delivery address
. Product Discovery (6–10) — eco-friendly filters, comparing variants, hidden deals, same-day delivery, virtual try-on
. Account and Security (11–15) — password reset, 2FA, suspended seller accounts, suspicious transactions, phishing protection
. Seller Support (16–20) — product listings, pricing errors, performance reports, negative feedback, appealing deactivations
Good for "walk me through..." style questions.

Adding New Documents
1. Drop the PDF into this folder.
2. Re-run notebooks/rag_pipeline.ipynb to rebuild the vector store.
3. Restart the backend so it reloads the updated index.