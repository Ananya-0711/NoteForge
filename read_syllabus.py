def read_syllabus(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    topics = []

    for line in lines:
        if line.strip():
            indentation = len(line) - len(line.lstrip())
            topic = line.strip()

            topics.append({
                "topic": topic,
                "indentation": indentation,
                "children": []
            })

    return topics


def build_tree(topics):
    root = []
    stack = []

    for item in topics:
        while stack and item["indentation"] <= stack[-1]["indentation"]:
            stack.pop()

        if stack:
            stack[-1]["children"].append(item)
        else:
            root.append(item)

        stack.append(item)

    return root


syllabus_path = "data/CN/syllabus.txt"

topics = read_syllabus(syllabus_path)
tree = build_tree(topics)


def print_tree(nodes, level=0):
    for node in nodes:
        print("  " * level + "- " + node["topic"])
        print_tree(node["children"], level + 1)


print_tree(tree)