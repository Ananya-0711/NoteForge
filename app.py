import os

from dotenv import load_dotenv
from google import genai

from read_pdf import extract_text
from retrieve import find_section, get_section

from read_syllabus import read_syllabus, build_tree, print_tree, get_leaf_topics

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

pdf_path = "data/CN/computer-networks-tanenbaum-5th-edition.pdf"

pages = extract_text(pdf_path)

syllabus_path = "data/CN/syllabus.txt"

topics = read_syllabus(syllabus_path)
syllabus_tree = build_tree(topics)

note_topics = get_leaf_topics(syllabus_tree)

print("\n--- NOTE TOPICS ---")

for topic in note_topics:
    print(topic)

print("\n--- SYLLABUS ---")
print_tree(syllabus_tree)

start_index = find_section(pages, topic)

if start_index is None:
    print("Section not found.")
else:
    section_pages = get_section(pages, start_index)

    textbook_content = "\n\n".join(
        page["text"] for page in section_pages
    )

    prompt = f"""
You are NoteForge, an AI tool that creates university exam notes
from a textbook.

Topic:
{topic}

Use ONLY the supplied textbook content.

Create concise, structured exam notes that preserve the important
hierarchy of the textbook section.

Structure:
1. Give a short introductory paragraph defining the main topic.
2. Explain the main classification or organization of the topic
   when the textbook provides one.
3. Give each important type or subtopic its own heading.
4. Under each heading, write ONE concise paragraph.

For each paragraph, prioritize:
- definition
- purpose
- working/principle
- important characteristics or components
- relevant example, when provided by the textbook

Length:
- The introduction should be 2–4 sentences.
- Each subtopic paragraph should normally be 3–5 sentences.
- Include enough information to capture the complete essence of
  the concept, but remove secondary details and lengthy examples.
- Do not turn the notes into a detailed textbook summary.

Accuracy:
- Use ONLY information supported by the supplied textbook.
- Do not use general knowledge to add facts.
- Do not invent information, examples, classifications, or terms.
- Preserve the textbook's terminology and organization.
- Do not copy the textbook word-for-word.

Formatting:
- Use clear headings.
- Use paragraphs, not bullet-point dumping.
- Keep the notes easy to revise before a university exam.

TEXTBOOK CONTENT:
{textbook_content}
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=prompt
    )

    print("\n--- NOTES ---")
    print(interaction.output_text)