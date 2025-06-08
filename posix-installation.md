# Install browser-ai for MacOS and Linux systems

Initialize your uv project:

```bash
uv init .
```

Create a virtual environment:

```bash
uv venv -p 3.13
```

Activate the environment:

```bash
source .venv/bin/activate
```

Now eliminate `toga-winforms` from the [pyproject.toml](pyproject.toml) file, and then run:

```bash
uv add toga
```

If you are on Linux, you most definitely will need more installation steps, and you can find them all on [Toga's official documentation](https://toga.readthedocs.io/en/stable/tutorial/tutorial-0.html), by selecting `Linux` as your operating system.

After completing this step, run:

```bash
uv sync
```

You should be all set, and you can now return to the [README](./README.md#set-env-variables)
