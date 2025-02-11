# Install sparQ

## Get the code:

```bash
git clone https://github.com/sparqone/sparq
cd sparq
```

### Install **uv**

https://docs.astral.sh/uv/getting-started/installation

### Run the app

```bash
uv run app.py
```

Access the application at http://localhost:8000

## Run the tests

```bash
uv run pytest
```

## Dependencies

### Updating dependencies

```bash
uv lock
```

### Adding new packages

```bash
uv add <package-name>
```

### Syncing your local environment

```bash
uv sync
```

## Notes

You can also still activate the environment and run the app manually:

```bash
. .venv/bin/activate
```
