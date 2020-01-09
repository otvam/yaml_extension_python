import yaml
import ast
import os


class Loader(yaml.Loader):
    """
    This Python class offers extension to the YAML format:
        - include YAML file in YAML file
        - include relative filesystem paths
        - include Python expression

    The extensions can be used as:
        include_var: !include 'sub.yaml' #include the content file sub.yaml
        path_var: !path 'sub.yaml' # parse the relative path with respect to the YAML file
        exec_var: !exec '[1, 2, 3]' # evaluate the Python expression

    This class:
        - was tested on "MS Windows" but should run with Linux
        - was tested with Python 3.7 but should run with Python 2.7

    This class uses "ast.literal_eval" for a "safe" parsing of Python expression. However the capabilities are limited.
    For an advanced parsing "pyparsing" could be used.
    """

    def __init__(self, stream):
        """
        Constructor of the Loader class.
        """

        # get the path of the YAML file for relative paths
        self._root = os.path.split(stream.name)[0]
        if (len(self._root) > 0) and (self._root[-1] == os.path.sep):
            self._root = self._root[0:-1]

        # call the contructor of the parent
        super(Loader, self).__init__(stream)

        # add the extension to the YAML format
        Loader.add_constructor("!include", lambda self, node: Loader.__yaml_handling(self, node, self.__extract_yaml))
        Loader.add_constructor("!path", lambda self, node: Loader.__yaml_handling(self, node, self.__extract_path))
        Loader.add_constructor("!exec", lambda self, node: Loader.__yaml_handling(self, node, self.__extract_exec))

    def __yaml_handling(self, node, fct):
        """
        Apply a function to a YAML for list, dict, scalar.
        """

        if isinstance(node, yaml.ScalarNode):
            return fct(self.construct_scalar(node))

        elif isinstance(node, yaml.SequenceNode):
            result = []
            for filename in self.construct_sequence(node):
                result.append(fct(filename))
            return result

        elif isinstance(node, yaml.MappingNode):
            result = {}
            for k, v in self.construct_mapping(node).iteritems():
                result[k] = fct(v)
            return result

        else:
            raise yaml.constructor.ConstructorError("invalid node")

    def __extract_path(self, filename):
        """
        Find the path with respect to the YAML file path.
        """

        return os.path.join(self._root, filename)

    def __extract_yaml(self, filename):
        """
        Load an included YAML file.
        """

        filepath = self.__extract_path(filename)
        with open(filepath, "r") as f:
            content = yaml.load(f, Loader)
            return content

    def __extract_exec(self, str):
        """
        Apply the interpreter to a Python expression.
        """

        return ast.literal_eval(str)


def load_yaml(filename):
    """
    Load a YAML file with file include, relative paths, and expression parsing.
    """

    content = yaml.load(open(filename), Loader)
    return content
