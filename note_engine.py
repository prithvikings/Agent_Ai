from llama_index.core.tools import FunctionTool
import os

note_file = os.path.join("data", "notes.txt")

def save_note(note):
    os.makedirs("data", exist_ok=True)  # Ensure 'data' folder exists
    if not os.path.exists(note_file):
        with open(note_file, "w") as f:
            pass  # Just create the file if it doesn't exist

    with open(note_file, "a") as f:
        f.writelines([note + "\n"])

    return "Note saved."

note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="This tool can save a text-based note to a file for the user.",
)
