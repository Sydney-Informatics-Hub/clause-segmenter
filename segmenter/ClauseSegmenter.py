from typing import Union

import spacy
from spacy import Language
from spacy.tokens import Token, Span, SpanGroup, Doc


class ClauseSegmenter:
    CLAUSE_ROOT_DEPS: list[str] = ['advcl', 'conj']

    def __init__(self, pipeline: Union[Language, str] = 'en_core_web_sm'):
        self.nlp: Language
        if isinstance(pipeline, Language):
            self.nlp = pipeline
        elif isinstance(pipeline, str):
            self.nlp = spacy.load(pipeline)
        else:
            raise TypeError(f"Expected provided pipeline to be either str or SpaCy Language. Instead got {type(pipeline)}")

    def get_pipeline(self) -> Language:
        return self.nlp

    def get_clauses_as_list(self, text: str) -> list[str]:
        doc = self.nlp(text)
        clauses: SpanGroup = SpanGroup(doc)
        for sentence in doc.sents:
            clauses += ClauseSegmenter._retrieve_clauses(doc, sentence.root)

        clause_ls: list[Span] = sorted([span for span in clauses], key=lambda sp: (sp.start, sp.end))
        return [c.text for c in clause_ls]

    def get_clauses_as_spangroup(self, doc: Doc) -> SpanGroup:
        clauses: SpanGroup = SpanGroup(doc)
        for sentence in doc.sents:
            clauses += ClauseSegmenter._retrieve_clauses(doc, sentence.root)

        clause_ls: list[Span] = sorted([span for span in clauses], key=lambda sp: (sp.start, sp.end))
        return SpanGroup(doc, name="clauses", spans=clause_ls)

    @staticmethod
    def _retrieve_clauses(doc: Doc, root: Token) -> SpanGroup:
        clauses: SpanGroup = SpanGroup(doc)

        current_clause_tokens: list[Token] = []
        clause_root_tokens: list[Token] = []
        for child in root.children:
            if ClauseSegmenter._is_child_punct(child):
                continue
            if ClauseSegmenter._is_clause_root(child):
                clause_root_tokens.append(child)
            else:
                current_clause_tokens.append(child)

        if not current_clause_tokens:
            current_clause_tokens = [root]

        leftmost_direct_i = root.i
        rightmost_direct_i = root.i
        for child in current_clause_tokens:
            if child.left_edge.i < leftmost_direct_i:
                leftmost_direct_i = child.left_edge.i
            if child.right_edge.i > rightmost_direct_i:
                rightmost_direct_i = child.right_edge.i

        clauses += [doc[leftmost_direct_i:rightmost_direct_i + 1]]

        for child in clause_root_tokens:
            left_i = child.left_edge.i
            right_i = child.right_edge.i
            child_span = doc[left_i:right_i + 1]

            clauses += ClauseSegmenter._retrieve_clauses(doc, child_span.root)

        return clauses

    @staticmethod
    def _is_child_punct(child: Token) -> bool:
        return child.dep_.lower() == 'punct'

    @staticmethod
    def _is_clause_root(tok: Token) -> bool:
        tok_dep: str = tok.dep_.lower()
        tok_pos: str = tok.pos_.lower()
        if tok.left_edge.tag_.lower() == 'to':
            return False
        return (tok_dep in ClauseSegmenter.CLAUSE_ROOT_DEPS) or ((tok_dep == 'ccomp') and (tok_pos == 'verb'))


if __name__ == '__main__':
    text_ipt = input('Enter text: \n')
    print()
    segmenter = ClauseSegmenter()
    clauses_ls = segmenter.get_clauses_as_list(text_ipt)
    for clause in clauses_ls:
        print(clause)
