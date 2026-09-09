import os
from dotenv import load_dotenv
from pathlib import Path
# uv add llama_cloud
from llama_cloud import LlamaCloud

load_dotenv()

client = LlamaCloud(api_key=os.getenv('LLAMA_PARSE_API_KEY'))

# PDF File Path
pdf_path = Path(__file__).parent.parent / "pdfs" / "ai-future-pdf.pdf"

# Upload
file_obj = client.files.create(file=str(pdf_path), purpose="parse")

# Submit + poll + get (parsing.parse wraps create / wait_for_completion / get)
# Raises on FAILED or CANCELLED. Tune polling_interval=, timeout= if needed.
result = client.parsing.parse(
    file_id=file_obj.id,
    # The parsing tier. Options: fast, cost_effective, agentic, agentic_plus,
    tier="agentic",
    # The version of the parsing tier to use. Use 'latest' for the most recent version,
    version="latest",
    # Options for controlling how we process the document,
    processing_options={
        "cost_optimizer": {
          "enable": True
        }
    },
    # expand: which fields to materialize (markdown_full, text_full, items, *_content_metadata, ...),
    expand=["markdown_full", "text_full"],
)

# Persist markdown and text to disk
output_dir = Path(__file__).parent.parent / 'parsed_data'
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "output.md").write_text(result.markdown_full or "", encoding="utf-8")
(output_dir / "output.txt").write_text(result.text_full or "", encoding="utf-8")
print(f"Wrote {len(result.markdown_full or '')} chars of markdown, {len(result.text_full or '')} chars of text")