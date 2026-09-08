# 🧾 FairSplit AI

A lightweight human-in-the-loop restaurant bill splitter.

## What it does

1. Upload a bill photograph.
2. AI extracts line items, quantities, prices, subtotal, tax, service charge and total.
3. Every extracted value can be reviewed and corrected before calculation.
4. Assign each item to one or more people.
5. Shared items are split between the selected people.
6. GST/tax and service charge are distributed proportionally to what each person actually consumed.
7. Shows a detailed per-person breakdown.
8. Flags a printed-total mismatch.
9. Exports the final split as CSV.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Optional AI OCR

Set your Gemini API key:

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
streamlit run app.py
```

Or put it in `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY="YOUR_KEY"
```

Without an API key, the app still runs using its demo bill, so the complete assignment flow can be demonstrated.

## Demo flow

Use 3 members:
- You
- Friend 1
- Friend 2

Upload any image, click **Use demo bill**, review the extracted values, assign items, then click **Calculate fair split**.

## Future upgrades

- Multi-photo bill stitching for long receipts
- Better confidence highlighting per field
- OCR benchmarking against 12-bill ground truth
- UPI payment links
- QR code for settling balances
- Tip handling
- Percentage-based GST components (CGST/SGST)
- Duplicate item detection
- Handwriting-aware OCR
