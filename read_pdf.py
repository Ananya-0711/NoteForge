import pymupdf

pdf_path = "data/CN/computer-networks-tanenbaum-5th-edition.pdf"

document = pymupdf.open(pdf_path)

print("Number of pages:", len(document))

for i in range(min(5, len(document))):
    page = document[i]
    text = page.get_text()

    print("\n--- PAGE", i + 1, "---")
    print("Characters extracted:", len(text))
    print(repr(text[:300]))

document.close()