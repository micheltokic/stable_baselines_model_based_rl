# Model Based Reinforcement Learning for Stable Baselines
A model based RL extension for stable baselines.

## Development
For development, clone this repository and install requirements via pip:
```
pip install -r requirements.txt
```
This will install all required dependencies for the package + all development
dependencies, as well as installing the package in editable mode (develop mode).

Running `pip install -e .` will not install develop dependencies, as they are
stored in the requirements.txt file only.

### Tests
Unit tests are located in the `./tests` directory. They can be executed using
the following command:
```
python -m pytest ./tests
```

## Documentation
MkDocs is used for generating the (user) documentation. The source markdown files
are stored in the `./docs` directory. All required dependencies for building the
docs are required via the `requirements.txt` (develop dependencies).  
More information about MkDocs: https://www.mkdocs.org/

### Serve Docs
To serve the docs with hot reloading run: `mkdocs serve`

### Api Documentation
The **lazydocs** package is used for automatic generation of API docs. To
generate latest version of the API docs run:
```
lazydocs \
    --overview-file="README.md" \
    --output-path="./docs/api" \
    --src-base-url="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/" \
    ./stable_baselines_model_based_rl
```
This will generate the api docs for the entire stable_baslines_model_based_rl
module and also create an overview page containing links to all packages, modules,
functions, etc.

### Automatic Docs Generation & GitHub Pages
The GitHub Workflow (`docs`) automatically generates the API docs, builds the MkDocs
and "deploys" it to the gh-pages branch, which means it'll be deployed to GitHub Pages

### PDF Generation
To export the documentation as PDF file, first follow all requirement instructions
as described here: https://github.com/orzih/mkdocs-with-pdf#requirements.  
The PDF file will only be created if a specific environment variable
(`DOCS_PDF_EXPORT`) is set:  
```shell
export DOCS_PDF_EXPORT=1
mkdocs build
```
The generated PDF file is located in the `site` directory.

The manual GitHub Actions workflow `docs_pdf_generation` can be triggered to create the PDF version
of the documentation. After the job finished, the PDF is availalble as job artifact.
