## `import_it.py`

Script to determine the import statement to import a name from a repository.

Requires ripgrep >=0.10.0.

### Usage

```sh
$ pip install import_it  # or `pip install .` from this directory
$ import_it main .
from import_it import main
# To get a relative import path, pass a 3rd argument, the filepath the import will go
$ import_it trim_prefix . ./import_it/example.py
from .utils import trim_prefix
```

See https://github.com/razzius/.spacemacs.d for editor integration details.
