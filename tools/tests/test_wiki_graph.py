"""Synthetic check for tools/wiki_graph.py. Run: python3 tools/tests/test_wiki_graph.py
All titles and contents are made up; no real notes are used."""
import hashlib, json, subprocess, sys, tempfile, unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import wiki_graph

BOM = b"\xef\xbb\xbf"
PAD = " filler text to pass the emptiness check."
NOTES = {  # file stem -> (text, bom+crlf)
    "Hub One": ("Hub One\nType: Hub\nTags: demo\nSummary: Synthetic hub.\n"
                "- Alpha | topic | Alpha summary | t1, t2 | 2026-01-01\n"
                "- Beta | topic | Beta summary | t1 | 2026-01-02\n"
                "- Ghost | topic | Missing note | t1 | 2026-01-03\n", True),
    "Alpha": ("Alpha\nType: topic\nTags: a, b\nSummary: Alpha note.\n"
              "Fact [verified]. Fact [unverified]. See [[beta]] and [[Nowhere]].\n"
              "```\n[[InFence]]\n```\nRelated: Beta; Dead Related\n" + PAD, True),
    "Beta": ("Beta\nType: topic\nSummary: Beta note." + PAD, False),
    "Lonely": ("Lonely\nType: topic\nSummary: Nobody links here." + PAD, True),
    "Zażółć": ("Dup one\nType: topic" + PAD, False),
    "Zazolc": ("Dup two\nType: topic" + PAD, False),
    "Untyped": ("Untyped\nJust text without a type line." + PAD, False),
    "Tiny": ("Tiny\nType: topic", False),
    "HOT": ("HOT (state on 2026-01-01, 06:50)\nType: meta\n[[Alpha]]" + PAD, True),
    "INDEX-AUTO": ("generated index, must be skipped\nType: topic" + PAD, False),
}


def write_wiki(d):
    for stem, (text, bom_crlf) in NOTES.items():
        raw = text.replace("\n", "\r\n").encode("utf-8")
        (d / f"{stem}.txt").write_bytes(BOM + raw if bom_crlf else text.encode("utf-8"))


def digest(d):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.glob("*"))}


class WikiGraph(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        write_wiki(self.dir)
        self.before = digest(self.dir)
        self.g = wiki_graph.build(wiki_graph.load_notes(self.dir))
        self.nodes = {n["title"]: n for n in self.g["nodes"]}
        self.edges = {(e["source"], e["target"], e["kind"]) for e in self.g["edges"]}

    def tearDown(self):
        self._tmp.cleanup()

    def test_nodes_and_files(self):
        self.assertEqual(self.g["count"], 9)  # INDEX-AUTO skipped
        self.assertNotIn("INDEX-AUTO", self.nodes)
        self.assertEqual(digest(self.dir), self.before)  # note files untouched

    def test_bom_crlf(self):
        a = self.nodes["Alpha"]
        self.assertEqual((a["type"], a["tags"], a["summary"]), ("topic", ["a", "b"], "Alpha note."))
        self.assertEqual((a["verified"], a["unverified"]), (1, 1))
        self.assertNotIn("\r", wiki_graph.clean((self.dir / "Alpha.txt").read_bytes()))

    def test_edges(self):
        self.assertIn(("Alpha", "Beta", "link"), self.edges)  # [[beta]], case-insensitive
        self.assertIn(("Alpha", "Beta", "related"), self.edges)
        self.assertIn(("Hub One", "Alpha", "hub"), self.edges)
        self.assertIn(("HOT", "Alpha", "link"), self.edges)
        self.assertFalse([e for e in self.edges if "InFence" in e])  # code fence ignored

    def test_incoming(self):
        self.assertEqual(self.nodes["Alpha"]["incoming"], 2)  # hub row, HOT link
        self.assertEqual(self.nodes["Beta"]["incoming"], 3)  # hub row, link, related

    def test_lint(self):
        lint = self.g["lint"]
        self.assertCountEqual([d["target"] for d in lint["dead_links"]],
                              ["Ghost", "Nowhere", "Dead Related"])
        self.assertEqual(len(lint["ambiguous_titles"]), 1)  # diacritics-insensitive duplicate
        self.assertEqual(lint["orphans"].count("Lonely"), 1)
        self.assertNotIn("HOT", lint["orphans"])  # meta exempt
        self.assertNotIn("Hub One", lint["orphans"])  # hub exempt
        self.assertEqual(lint["missing_type"], ["Untyped"])
        self.assertEqual(lint["empty"], ["Tiny"])

    def test_title_from_file_name(self):
        self.assertIn("HOT", self.nodes)  # first line has a state suffix; title does not

    def test_deterministic(self):
        again = wiki_graph.build(wiki_graph.load_notes(self.dir))
        self.g.pop("generated_at"), again.pop("generated_at")
        self.assertEqual(self.g, again)

    def test_cli(self):
        out = self.dir.parent / (self.dir.name + ".json")
        try:
            subprocess.run([sys.executable, "-I", str(TOOLS / "wiki_graph.py"), str(self.dir), "-o", str(out)],
                           check=True, capture_output=True)
            g = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(list(g), ["generated_at", "count", "nodes", "edges", "lint"])
            self.assertEqual(g["count"], 9)
        finally:
            out.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
