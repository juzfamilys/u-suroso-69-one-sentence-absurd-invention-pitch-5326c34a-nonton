"""Apologetic Toaster — a one-sentence absurd invention pitch.

Writes exactly one sentence to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output): a toaster that apologises out loud every time it burns your
bread, then writes a formal letter of complaint to itself and files it
in a drawer you will never open.

Pure Python standard library, deterministic: the same bytes on every run.
"""

import os

ENTRY = (
    "A toaster that apologizes out loud every time it burns your bread, "
    "then writes a formal letter of complaint to itself and files it in "
    "a drawer you will never open."
)


def validate(text):
    """Enforce the competition gate for the entry text.

    The entry must be 1-220 characters, a single line, exactly one
    sentence, and contain no leading or trailing whitespace.
    """
    if not text or text.strip() == "":
        raise ValueError("entry must not be blank")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(text) < 1 or len(text) > 220:
        raise ValueError("entry must be 1-220 characters, got %d" % len(text))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence")


def verify_output(path, expected):
    """Read the entry back from disk and check it byte for byte.

    Returns the decoded text so the caller can validate the gate on
    exactly what landed on disk, not just on the in-memory string.
    """
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != expected:
        raise ValueError("entry on disk does not match the entry bytes")
    if on_disk.endswith(b"\n") or on_disk.endswith(b"\r"):
        raise ValueError("entry file must not end with a newline")
    return on_disk.decode("utf-8")


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read back what landed on disk and re-validate it byte for byte.
    on_disk_text = verify_output(path, data)
    validate(on_disk_text)
    print("Wrote %d bytes to %s" % (len(data), path))


if __name__ == "__main__":
    main()
