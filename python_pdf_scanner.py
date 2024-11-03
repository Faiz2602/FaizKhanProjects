import pdfplumber
import tkinter as tk
from tkinter import filedialog, scrolledtext

# FUNCTION TO LOAD PDF AND EXTRACT TEXT FROM PAGES
def load_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return pages

# FUNCTION TO EXTRACT TITLE, AUTHORS, HEADINGS, AND REFERENCES
def extract_data_from_pdf(file_path):
    pages = load_pdf(file_path)
    first_page_text = pages[0] if pages else ""
    entire_text = "\n".join(pages)

    # EXTRACT TITLE AND AUTHORS FROM FIRST PAGE
    title = first_page_text.splitlines()[0] if first_page_text else "Title not found"
    authors = first_page_text.splitlines()[1] if len(first_page_text.splitlines()) > 1 else "Authors not found"

    # EXTRACT HEADINGS AND REFERENCES
    headings = [line for page in pages for line in page.splitlines() if line.isupper() and len(line.split()) < 10]
    references = []
    reference_section = False
    for line in entire_text.splitlines():
        if "REFERENCES" in line.upper():
            reference_section = True
        elif reference_section and line.strip():
            references.append(line)

    return title, authors, headings, references

# GUI APPLICATION CLASS
class PDFScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Scanner")
        self.root.geometry("800x700")
        self.root.configure(bg="#2E3440")

        # TITLE LABEL
        title_label = tk.Label(
            root, text="PDF Research Paper Scanner",
            font=("Helvetica", 18, "bold"), fg="#88C0D0", bg="#2E3440"
        )
        title_label.pack(pady=20)

        # UPLOAD BUTTON
        self.upload_button = tk.Button(
            root, text="Upload PDF", command=self.upload_pdf,
            bg="#5E81AC", fg="white", font=("Helvetica", 14, "bold"), width=15, height=2
        )
        self.upload_button.pack(pady=20)

        # LOADING INDICATOR
        self.loading_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#2E3440", fg="#A3BE8C")
        self.loading_label.pack()

        # RESULTS TEXT BOX
        self.results_text = scrolledtext.ScrolledText(
            root, width=80, height=20, bg="#3B4252", fg="white",
            font=("Courier", 10), wrap=tk.WORD
        )
        self.results_text.pack(pady=20)

        # MADE BY LABEL
        made_by_label = tk.Label(
            root, text="Made by Faiz Khan 24BCE10703",
            font=("Helvetica", 10), fg="#A3BE8C", bg="#2E3440"
        )
        made_by_label.pack(pady=10)

    # FUNCTION TO HANDLE PDF UPLOAD
    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.results_text.delete("1.0", tk.END)
            self.loading_label.config(text="Loading... Please wait.")
            self.root.update()

            try:
                title, authors, headings, references = extract_data_from_pdf(file_path)
                display_text = (
                    f"Title:\n{title}\n\nAuthors:\n{authors}\n\nHeadings:\n" +
                    "\n".join(headings) + "\n\nReferences:\n" + "\n".join(references)
                )
                self.results_text.insert(tk.END, display_text)
            except Exception as e:
                self.results_text.insert(tk.END, f"Error: {e}\n")
            finally:
                self.loading_label.config(text="")

# MAIN FUNCTION TO RUN THE APP
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFScannerApp(root)
    root.mainloop()
