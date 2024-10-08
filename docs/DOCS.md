# clause_segmenter Documentation

---

## Docs

### clause_segmenter.ClauseSegmenter

A text segmentation tool used to segment text into clauses.
The spaCy dependency parser and part-of-speech tagger are used to identify clauses.
There are two public methods provided for segmenting: get_clauses_as_list and get_clauses_as_spangroup

Can be imported using:

```python
from clause_segmenter import ClauseSegmenter
```

---

### ClauseSegmenter.\_\_init\_\_

Initialises the ClauseSegmenter with a configurable spaCy Language pipeline. If the pipeline argument is a string, then a download of the model through spaCy will be attempted before loading it as a pipeline.

Params
-  pipeline: Language or str – The spaCy Language or identifier of the Language to be used by the ClauseSegmenter. Defaults to 'en_core_web_sm'

Examples

```python
segmenter = ClauseSegmenter()
```

```python
segmenter = ClauseSegmenter(pipeline='en_core_web_lg')
```

```python
segmenter = ClauseSegmenter(pipeline=spacy.load('en_core_web_md'))
```

---

### CorpusLoader.get_pipeline

Returns: Language - the spaCy Language pipeline used by the ClauseSegmenter instance

Example

```python
segmenter = ClauseSegmenter()
pipeline = segmenter.get_pipeline()
```

---

### CorpusLoader.get_clauses_as_list

Converts the provided text to a spaCy Doc using the preconfigured Language pipeline and returns a list of strings, where each element is a clause.

Params
-  text: str – The input text that will be segmented into clauses.

Returns: list[str] - A list of strings, where each element is a clause. The clauses are sorted first by clause start token index, and then by clause end token index.

Example

```python
text: str = "When I want to leave the house, I have to check if it's raining, so I know whether to bring an umbrella."
segmenter = ClauseSegmenter()
clause_list: list[str] = segmenter.get_clauses_as_list(text)
```

---

### CorpusLoader.get_clauses_as_spangroup

Accepts a Doc object and returns a SpanGroup, where each Span element is a clause. A SpanGroup object functions only as long as the Doc object used to create it exists, so a reference to the provided doc should be maintained as long as the returned SpanGroup is needed.

Params
-  doc: Doc – The input text that will be segmented into clauses as a spaCy Doc.

Returns: SpanGroup - A SpanGroup whose Span elements are the segmented clauses. The clauses are sorted first by clause start token index, and then by clause end token index.

Example

```python
pipeline: Language = spacy.load('en_core_web_sm')
doc: Doc = pipeline("When I want to leave the house, I have to check if it's raining, so I know whether to bring an umbrella.")
segmenter = ClauseSegmenter(pipeline=pipeline)
clause_spans: SpanGroup = segmenter.get_clauses_as_spangroup(doc)
```

---

## Notes

### spaCy Pipelines

When constructing the ClauseSegmenter, by default the spaCy 'en_core_web_sm' Language is used, with a new instance created for each ClauseSegmenter instance.
If more than one ClauseSegmenter instance is created, it is recommended to pass the constructor a reference to an initialised spaCy Language.
A spaCy Language passed to the ClauseSegmenter constructor must contain 'tagger' and 'parser' components in its pipeline.

Additionally, if a string argument is passed for the pipeline parameter (such as the default argument), the ClauseSegmenter constructor will attempt to load the model. If the model is not already downloaded in the current environment, it will be downloaded and then loaded. Since this download occurs at runtime, an internet connection will be required. To avoid this, run the following command to ensure the model is available at runtime:

```shell
python3 -m spacy download en_core_web_sm
```

## Example usage

```python
from clause_segmenter import ClauseSegmenter

text = "When I want to leave the house, I have to check if it's raining, so I know whether to bring an umbrella."
segmenter = ClauseSegmenter()
clauses_ls = segmenter.get_clauses_as_list(text)
for clause in clauses_ls:
    print(clause)
```