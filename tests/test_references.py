from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from find_references import find_references, read_catalog  # noqa: E402
from validate_artifacts import validate_package  # noqa: E402


class ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = read_catalog(ROOT / "assets/reference-index.jsonl")

    def test_search_finds_uploadable_architecture_references(self):
        found = find_references("retrieval", self.entries, limit=4, kind="concept")
        self.assertTrue(found)
        self.assertTrue(any(row["asset_id"] == "concept.rag_pipeline" for row in found))
        for row in found:
            self.assertTrue((ROOT / row["preview_path"]).is_file())
            self.assertEqual(row["kind"], "concept")

    def test_unknown_term_does_not_fabricate_matches(self):
        self.assertEqual(find_references("nonexistenttermxyz", self.entries), [])

    def test_package_links_and_catalog_resolve(self):
        result = validate_package(ROOT)
        self.assertGreater(result["reference_entries"], 0)


if __name__ == "__main__":
    unittest.main()
