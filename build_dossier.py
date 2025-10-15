import os
from markdown_pdf import MarkdownPdf

def create_dossier():
    """
    Generates a single PDF dossier from the markdown files in the briefing_room directory.
    """
    print("--- Generating FoundLab NVIDIA Incident Dossier ---")
    
    briefing_path = "briefing_room"
    output_filename = "FoundLab_NVIDIA_Incident_Dossier.pdf"

    files_to_compile = [
        "00_EXECUTIVE_SUMMARY.md",
        "01_CASE_STUDY_NVIDIA_INCIDENT.md",
        "02_TECHNICAL_WHITEPAPER.md",
        "03_VERITAS_PROTOCOL.md",
    ]

    pdf = MarkdownPdf()

    for md_file in files_to_compile:
        filepath = os.path.join(briefing_path, md_file)
        if os.path.exists(filepath):
            print(f"   > Compiling {filepath}...")
            with open(filepath, 'r', encoding='utf-8') as f:
                # Simple way to add a page break before each new document
                pdf.add_section(f.read(), new_page=True)
        else:
            print(f"   > Warning: {filepath} not found. Skipping.")

    pdf.meta["title"] = "FoundLab NVIDIA Incident Dossier"
    pdf.meta["author"] = "FoundLab"
    
    pdf.save(output_filename)

    print(f"\n--- Dossier Generated Successfully ---")
    print(f"   > Output file: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    # You might need to install the dependency first:
    # pip install markdown-pdf
    create_dossier()
