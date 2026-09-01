#!/usr/bin/env python3
"""Dependency-free HTML + accessibility validator (closes GAP-002).

Uses only the Python standard library so it runs on a bare CI runner, unlike
the browser-backed suites. Checks structure that a static grep cannot see:

  V-001  tags nest and close correctly
  V-002  no duplicate id attributes
  V-003  every <img> has a non-empty alt (or explicit alt="" for decoration)
  V-004  every <a> has an href
  V-005  <html lang> is set
  V-006  exactly one <h1>
  V-007  heading levels never skip (h2 -> h4)
  V-008  every button has a discernible name
  V-009  a <main> landmark exists, exactly once
  V-010  every aria-describedby / aria-labelledby points at a real id

Exit status: 0 clean, 1 problems found (each printed with its V-id).
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
# Elements whose content is raw text, not markup.
RAW = {"script", "style"}


class Validator(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.problems = []
        self.ids = {}
        self.id_refs = []          # (attr, value, line)
        self.headings = []
        self.h1_count = 0
        self.main_count = 0
        self.button_depth = 0
        self.button_text = ""
        self.button_line = 0
        self.button_has_label = False
        self.in_raw = None

    def fail(self, vid, message):
        self.problems.append(f"{vid}  line {self.getpos()[0]}: {message}")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.in_raw:
            return
        if tag in RAW:
            self.in_raw = tag

        if "id" in a:
            if a["id"] in self.ids:
                self.fail("V-002", f'duplicate id "{a["id"]}" '
                                   f'(first at line {self.ids[a["id"]]})')
            else:
                self.ids[a["id"]] = self.getpos()[0]

        for ref_attr in ("aria-describedby", "aria-labelledby"):
            if ref_attr in a:
                for token in a[ref_attr].split():
                    self.id_refs.append((ref_attr, token, self.getpos()[0]))

        if tag == "img" and "alt" not in a:
            self.fail("V-003", f'<img src="{a.get("src", "?")}"> has no alt')
        if tag == "a" and "href" not in a:
            self.fail("V-004", "<a> without href")
        if tag == "html" and not a.get("lang"):
            self.fail("V-005", "<html> without lang")
        if tag == "main":
            self.main_count += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self.headings.append((level, self.getpos()[0]))
            if level == 1:
                self.h1_count += 1
        if tag == "button":
            self.button_depth += 1
            self.button_text = ""
            self.button_line = self.getpos()[0]
            self.button_has_label = bool(a.get("aria-label"))

        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        # <tag /> — self-closing, never pushed on the stack.
        saved = self.stack[:]
        self.handle_starttag(tag, attrs)
        self.stack = saved

    def handle_data(self, data):
        if self.button_depth:
            self.button_text += data

    def handle_endtag(self, tag):
        if self.in_raw:
            if tag == self.in_raw:
                self.in_raw = None
            else:
                return
        if tag in VOID:
            return
        if tag == "button":
            self.button_depth = max(0, self.button_depth - 1)
            if not self.button_text.strip() and not self.button_has_label:
                self.problems.append(
                    f"V-008  line {self.button_line}: <button> has no text or aria-label")
        if not self.stack:
            self.fail("V-001", f"</{tag}> with nothing open")
            return
        open_tag, open_line = self.stack.pop()
        if open_tag != tag:
            self.fail("V-001",
                      f"</{tag}> closes <{open_tag}> opened at line {open_line}")

    def finish(self):
        for tag, line in self.stack:
            self.problems.append(f"V-001  line {line}: <{tag}> never closed")
        if self.h1_count != 1:
            self.problems.append(f"V-006  expected exactly one <h1>, found {self.h1_count}")
        if self.main_count != 1:
            self.problems.append(f"V-009  expected exactly one <main>, found {self.main_count}")
        previous = None
        for level, line in self.headings:
            if previous is not None and level > previous + 1:
                self.problems.append(
                    f"V-007  line {line}: heading jumps h{previous} -> h{level}")
            previous = level
        for attr, token, line in self.id_refs:
            if token not in self.ids:
                self.problems.append(
                    f'V-010  line {line}: {attr}="{token}" points at no element')
        return self.problems


def validate(path: Path) -> list:
    parser = Validator()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser.finish()


# Governance tooling must itself be tested (constitution TESTING.md): a
# validator that reports nothing would look identical to a clean page.
SELFTEST_CASES = [
    ("V-001", "<html lang='en'><body><main><h1>x</h1><div><p>unclosed</div></main></body></html>"),
    ("V-002", "<html lang='en'><body><main><h1 id='d'>a</h1><p id='d'>b</p></main></body></html>"),
    ("V-003", "<html lang='en'><body><main><h1>a</h1><img src='x.jpg'></main></body></html>"),
    ("V-004", "<html lang='en'><body><main><h1>a</h1><a>no href</a></main></body></html>"),
    ("V-005", "<html><body><main><h1>a</h1></main></body></html>"),
    ("V-006", "<html lang='en'><body><main><h2>no h1</h2></main></body></html>"),
    ("V-007", "<html lang='en'><body><main><h1>a</h1><h3>skipped</h3></main></body></html>"),
    ("V-008", "<html lang='en'><body><main><h1>a</h1><button></button></main></body></html>"),
    ("V-009", "<html lang='en'><body><h1>a</h1></body></html>"),
    ("V-010", "<html lang='en'><body><main><h1>a</h1><button aria-describedby='ghost'>x</button></main></body></html>"),
]


def selftest() -> int:
    failures = 0
    for expected, markup in SELFTEST_CASES:
        parser = Validator()
        parser.feed(markup)
        parser.close()
        problems = parser.finish()
        if any(p.startswith(expected) for p in problems):
            print(f"  PASS  selftest {expected} detected")
        else:
            failures += 1
            print(f"  FAIL  selftest {expected} NOT detected (got: {problems})")

    # A clean document must report nothing at all.
    parser = Validator()
    parser.feed("<html lang='en'><body><main><h1>a</h1>"
                "<img src='x.jpg' alt='x'><a href='#x'>y</a>"
                "<button>press</button></main></body></html>")
    parser.close()
    clean = parser.finish()
    if clean:
        failures += 1
        print(f"  FAIL  selftest clean document reported problems: {clean}")
    else:
        print("  PASS  selftest clean document reports nothing")
    return 1 if failures else 0


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    targets = sorted((root / "site").glob("*.html"))
    if not targets:
        print("  FAIL  no HTML files found to validate")
        return 1

    failed = False
    for target in targets:
        problems = validate(target)
        name = target.relative_to(root).as_posix()
        if problems:
            failed = True
            print(f"  FAIL  {name}")
            for problem in problems:
                print(f"          {problem}")
        else:
            print(f"  PASS  {name}  (structure, ids, alt text, headings, landmarks)")
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
