import re

from read_pdf import extract_text


def find_section(pages, section_title):
    section_title = section_title.lower()

    for index, page in enumerate(pages):
        lines = page["text"].splitlines()

        for line in lines:
            line = line.strip()

            # Ignore table-of-contents entries such as:
            # "1.2 NETWORK HARDWARE, 17"
            if "," in line:
                continue

            if (
                section_title in line.lower()
                and re.match(r"^\d+\.\d+\s+[A-Z]", line)
            ):
                return index

    return None


def is_major_section_heading(line):
    line = line.strip()

    return bool(re.match(r"^\d+\.\d+\s+[A-Z]", line))


def get_section(pages, start_index):
    section_pages = []

    for index in range(start_index, len(pages)):
        page = pages[index]
        text = page["text"]

        if index > start_index:
            lines = text.splitlines()

            for line in lines:
                if is_major_section_heading(line):
                    return section_pages

        section_pages.append(page)

    return section_pages


pdf_path = "data/CN/computer-networks-tanenbaum-5th-edition.pdf"

pages = extract_text(pdf_path)

topic = input("Enter a topic: ").strip()

start_index = find_section(pages, topic)

if start_index is None:
    print("Section not found.")
else:
    section_pages = get_section(pages, start_index)

    print("\nSection found.")
    print("Start page:", section_pages[0]["page"])
    print("End page:", section_pages[-1]["page"])

    for page in section_pages:
        print(f"\n--- Page {page['page']} ---")
        print(page["text"])