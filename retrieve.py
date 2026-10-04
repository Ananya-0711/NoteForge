import re

from read_pdf import extract_text


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def is_numbered_heading(line):
    line = line.strip()

    return bool(
        re.match(
            r"^(?:SEC\.\s*)?\d+(?:\.\d+)+\s+",
            line,
            re.IGNORECASE
        )
    )


def clean_heading(line):
    line = line.strip()

    line = re.sub(
        r"^(?:SEC\.\s*)?\d+(?:\.\d+)+\s*",
        "",
        line,
        flags=re.IGNORECASE
    )

    return normalize(line)


def find_section(pages, section_title):

    target = normalize(section_title)

    # -------------------------------------------------
    # INTERNET
    # Exact textbook heading:
    # 1.5.1 The Internet
    # -------------------------------------------------

    if target == "internet":

        for index, page in enumerate(pages):

            # Skip table of contents and front matter
            if page["page"] < 40:
                continue

            for line in page["text"].splitlines():

                line = line.strip()

                # Match:
                # 1.5.1 The Internet
                # 1.5.1 THE INTERNET

                if re.match(
                    r"^1\.5\.1\s+The Internet\b",
                    line,
                    re.IGNORECASE
                ):
                    return index

        return None

    # -------------------------------------------------
    # ARPANET
    # -------------------------------------------------

    if target == "arpanet":

        example_networks_found = False

        for index, page in enumerate(pages):

            for line in page["text"].splitlines():

                cleaned = normalize(line)

                if cleaned == "example networks":
                    example_networks_found = True

                if (
                    example_networks_found
                    and cleaned == "the arpanet"
                ):
                    return index

        return None

    # -------------------------------------------------
    # OTHER TOPICS
    # -------------------------------------------------

    heading_variants = {

        "network hardware": {
            "network hardware"
        },

        "network software": {
            "network software"
        },

        "osi": {
            "the osi reference model",
            "osi reference model"
        },

        "tcp ip reference models": {
            "the tcp ip reference model",
            "tcp ip reference model"
        },

        "twisted pairs": {
            "twisted pair",
            "twisted pairs"
        },

        "coaxial cable": {
            "coaxial cable"
        },

        "fiber optics": {
            "fiber optics",
            "fiber optic"
        },

        "wireless transmission": {
            "wireless transmission"
        },

        "design issues": {
            "data link layer design issues"
        },

        "framing": {
            "framing"
        },

        "error detection and correction": {
            "error detection and correction"
        }
    }

    variants = heading_variants.get(
        target,
        {target}
    )

    for index, page in enumerate(pages):

        lines = page["text"].splitlines()

        for line_number, line in enumerate(lines):

            line = line.strip()

            if not line:
                continue

            cleaned = clean_heading(line)

            if cleaned in variants:
                return index

            # Handle headings split across two lines.
            if line_number + 1 < len(lines):

                next_line = lines[
                    line_number + 1
                ].strip()

                combined = normalize(
                    line + " " + next_line
                )

                combined = re.sub(
                    r"^(?:SEC\.\s*)?\d+(?:\.\d+)+\s*",
                    "",
                    combined,
                    flags=re.IGNORECASE
                )

                combined = normalize(combined)

                if combined in variants:
                    return index

    return None


def get_section(pages, start_index):

    section_pages = []

    for index in range(
        start_index,
        len(pages)
    ):

        page = pages[index]

        if index > start_index:

            for line in page["text"].splitlines():

                if is_numbered_heading(line):
                    return section_pages

        section_pages.append(page)

    return section_pages


# -----------------------------------------------------
# RETRIEVAL TEST
# -----------------------------------------------------

if __name__ == "__main__":

    pdf_path = (
        "data/CN/"
        "computer-networks-tanenbaum-5th-edition.pdf"
    )

    pages = extract_text(pdf_path)

    topics = [

        "Network Hardware",
        "Network Software",
        "OSI",
        "TCP/IP Reference Models",
        "ARPANET",
        "Internet",
        "Twisted Pairs",
        "Coaxial Cable",
        "Fiber Optics",
        "Wireless Transmission",
        "Design Issues",
        "Framing",
        "Error Detection and Correction"

    ]

    print("\n--- RETRIEVAL TEST ---")

    for topic in topics:

        start_index = find_section(
            pages,
            topic
        )

        if start_index is None:

            print(f"❌ {topic}")

        else:

            print(
                f"✅ {topic} → page "
                f"{pages[start_index]['page']}"
            )