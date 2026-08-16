import pymupdf

def extract_text(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        pages.append({
            "page": page_number + 1,
            "text": text
        })

    document.close()

    return pages


pdf_path = "data/CN/computer-networks-tanenbaum-5th-edition.pdf"

pages = extract_text(pdf_path)

print("Total pages:", len(pages))
print("Page 5:")
print(pages[4]["text"])