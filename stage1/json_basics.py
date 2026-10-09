import json

question = {
    "question": "How has EV adoption changed in India?",
    "topics": ["electric vehicles", "India", "policy"],
    "year_range": {"start": 2015, "end": 2025},
    "needs_data": True,
    "notes": None,
}

# Convert Python dictionary → JSON text
text = json.dumps(question, indent=2)

print(text)
print(type(text))

# Convert JSON text → Python dictionary
back = json.loads(text)

print(type(back))
print(back["year_range"]["start"])
print(back["topics"][0])