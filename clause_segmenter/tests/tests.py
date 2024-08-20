import unittest
from pathlib import Path

from spacy import Language
from spacy.lang.en import English
from spacy.tokens import SpanGroup, Doc

from clause_segmenter import ClauseSegmenter

CURRENT_DIR: Path = Path(__file__).parent.resolve()


class TestSegmenter(unittest.TestCase):
    INPUTS_DIR: Path = CURRENT_DIR / 'test_files/inputs/'
    EXPECTED_DIR: Path = CURRENT_DIR / 'test_files/expected/'

    def setUp(self):
        self.segmenter: ClauseSegmenter = ClauseSegmenter()

    # get_pipeline() tests

    def test_default_pipeline(self):
        self.assertIsInstance(self.segmenter.get_pipeline(), Language)

    def test_custom_pipeline(self):
        custom_pipeline: Language = English()
        custom_pipeline.add_pipe('tagger')
        custom_pipeline.add_pipe('parser')
        segmenter: ClauseSegmenter = ClauseSegmenter(pipeline=custom_pipeline)

        self.assertEqual(segmenter.get_pipeline(), custom_pipeline)

    # get_clauses_as_list() tests

    def _run_text_test_from_files(self, filename: str):
        input_filepath = TestSegmenter.INPUTS_DIR / filename
        expected_filepath = TestSegmenter.EXPECTED_DIR / filename

        if not input_filepath.exists():
            raise ValueError(f'Test file does not exist: {input_filepath}')
        if not expected_filepath.exists():
            raise ValueError(f'Test file does not exist: {expected_filepath}')

        with open(input_filepath) as f:
            input_text: str = f.read()
        with open(expected_filepath) as f:
            expected_output: list[str] = [line.rstrip('\n') for line in f]

        actual_output: list[str] = self.segmenter.get_clauses_as_list(input_text)

        self.assertEqual(actual_output, expected_output)

    def _run_doc_test_from_files(self, filename: str):
        input_filepath = TestSegmenter.INPUTS_DIR / filename
        expected_filepath = TestSegmenter.EXPECTED_DIR / filename

        if not input_filepath.exists():
            raise ValueError(f'Test file does not exist: {input_filepath}')
        if not expected_filepath.exists():
            raise ValueError(f'Test file does not exist: {expected_filepath}')

        with open(input_filepath) as f:
            input_text: str = f.read()
        with open(expected_filepath) as f:
            expected_output: list[str] = [line.rstrip('\n') for line in f]

        pipeline: Language = self.segmenter.get_pipeline()
        doc: Doc = pipeline(input_text)
        output_spans: SpanGroup = self.segmenter.get_clauses_as_spangroup(doc)
        actual_output: list[str] = [sp.text for sp in output_spans]

        self.assertEqual(actual_output, expected_output)

    def test_1(self):
        self._run_text_test_from_files('1.txt')
        self._run_doc_test_from_files('1.txt')

    def test_2(self):
        self._run_text_test_from_files('2.txt')
        self._run_doc_test_from_files('2.txt')

    def test_3(self):
        self._run_text_test_from_files('3.txt')
        self._run_doc_test_from_files('3.txt')


if __name__ == '__main__':
    unittest.main()
