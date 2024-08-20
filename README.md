# Clause Segmenter

A clause segmenting tool utilising Python's SpaCy

## Installation

```shell
python3 -m pip install clause-segmenter
```

## Documentation

Documentation can be found [here](https://sydney-informatics-hub.github.io/clause-segmenter/DOCS.html)

## Usage

A code snippet example that uses the ClauseSegmenter

```python
from clause_segmenter import ClauseSegmenter

text = "When I want to leave the house, I have to check if it's raining, so I know whether to bring an umbrella."
segmenter = ClauseSegmenter()
clauses_ls = segmenter.get_clauses_as_list(text)
for clause in clauses_ls:
    print(clause)
```

Output:
```
When I want to leave the house
I have to check if it's raining
so I know whether to bring an umbrella
```

## Tests

```shell
python3 clause_segmenter/tests/tests.py
```

## Contributing

The package for this project is hosted on PyPi: https://pypi.org/project/clause-segmenter/

Dependencies, publishing, and version numbering is handled by [Poetry](https://python-poetry.org)

To publish a new version:

```shell
poetry config pypi-token.pypi <TOKEN>
poetry version minor
poetry publish --build
```

## Authors

  - **Hamish Croser** - [h-croser](https://github.com/h-croser)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details