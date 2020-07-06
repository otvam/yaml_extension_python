# Python Code for Extending the YAML Format

This **Python** class offers extensions to the **YAML** format:
* include YAML file in YAML file
* include relative filesystem paths
* include Python expression

The extensions can be used as:
```
include_var: !include 'sub.yaml' #include the content file sub.yaml
path_var: !path 'sub.yaml' # parse the relative path with respect to the YAML file
exec_var: !exec '[1, 2, 3]' # evaluate the Python expression
```

The example [test_yaml.pym](test_yaml.py) demonstrates the YAML parsing with the extensions.

This class:
* was tested on "MS Windows" but should run with Linux
* was tested with Python 3.6 and 3.7 but should run with Python 2.7

This class uses "ast.literal_eval" for a "safe" parsing of Python expression. However the capabilities are limited.
For an advanced parsing "pyparsing" could be used.

## Author

**Thomas Guillod** - [GitHub Profile](https://github.com/otvam)

## License

This project is licensed under the **BSD License**, see [LICENSE.md](LICENSE.md).
