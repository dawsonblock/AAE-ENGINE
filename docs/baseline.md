# Test Baseline

This document describes how to reproduce the project’s test baseline without committing
environment-specific logs or local paths.

## How to run the tests

From the project root:

```bash
pytest
```

## Expected outcome

- All tests should collect and run successfully.
- The test run should complete without unexpected errors.
- Any known, acceptable warnings (for example, about deprecated options) should be
  documented here rather than by pasting full warning stacks.

Example of a stable baseline description:

- Python version: a supported version listed in this project’s documentation
- Test command: `pytest`
- Summary: `N passed, 0 failed` (exact counts may vary as tests are added or removed)

## Environment notes

- Avoid committing full `pytest` logs, `pip list` output, or absolute local paths
  (such as those under a home directory) into version control.
- If detailed logs are needed for debugging or CI, store them as build artifacts
  or add them to `.gitignore` instead of documenting them verbatim here.

This file is intended to provide a concise, reproducible description of how to run
the tests and what success looks like, independent of any one developer’s machine.
click                   8.3.1
coverage                7.13.3
cyclonedx-python-lib    11.6.0
datasets                4.5.0
defusedxml              0.7.1
dill                    0.4.0
distlib                 0.4.0
distro                  1.9.0
docker                  7.1.0
fastcore                1.12.11
filelock                3.20.3
frozenlist              1.8.0
fsspec                  2025.10.0
ghapi                   1.0.10
gitdb                   4.0.12
GitPython               3.1.46
grpclib                 0.4.9
h11                     0.16.0
h2                      4.3.0
hf-xet                  1.2.0
hpack                   4.1.0
httpcore                1.0.9
httpx                   0.28.1
huggingface_hub         1.4.0
hyperframe              6.1.0
identify                2.6.16
idna                    3.11
iniconfig               2.3.0
jiter                   0.13.0
license-expression      30.4.4
markdown-it-py          4.0.0
mdurl                   0.1.2
modal                   1.3.2
msgpack                 1.1.2
multidict               6.7.1
multiprocess            0.70.18
nodeenv                 1.10.0
numpy                   2.4.2
openai                  2.17.0
packageurl-python       0.17.6
packaging               26.0
pandas                  3.0.0
pip                     26.0.1
pip-api                 0.0.34
pip_audit               2.10.0
pip-requirements-parser 32.0.1
platformdirs            4.5.1
pluggy                  1.6.0
pre_commit              4.5.1
propcache               0.4.1
protobuf                6.33.5
py-serializable         2.1.0
pyarrow                 23.0.0
pydantic                2.12.5
pydantic_core           2.41.5
Pygments                2.19.2
pyparsing               3.3.2
pytest                  9.0.2
pytest-cov              7.0.0
python-dateutil         2.9.0.post0
python-dotenv           1.2.1
PyYAML                  6.0.3
requests                2.32.5
rfsn-learner            0.2.0           /Users/dawsonblock/Downloads/rfsn_kernel_learner_build
rich                    14.3.2
ruff                    0.15.0
shellingham             1.5.4
six                     1.17.0
smmap                   5.0.2
sniffio                 1.3.1
sortedcontainers        2.4.0
soupsieve               2.8.3
swebench                4.1.0
synchronicity           0.11.1
tenacity                9.1.3
toml                    0.10.2
tomli                   2.4.0
tomli_w                 1.2.0
tqdm                    4.67.3
typer                   0.21.1
typer-slim              0.21.1
types-certifi           2021.10.8.3
types-toml              0.10.8.20240310
typing_extensions       4.15.0
typing-inspection       0.4.2
unidiff                 0.7.5
urllib3                 2.6.3
virtualenv              20.36.1
watchfiles              1.1.1
xxhash                  3.6.0
yarl                    1.22.0
