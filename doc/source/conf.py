"""Sphinx documentation configuration file."""

import os
import pathlib
from datetime import datetime

import jinja2
import yaml
from ansys_sphinx_theme import ansys_favicon, get_version_match
from tabulate import tabulate as Table

# Constants used for generating documentation
DOC_SOURCE_DIR = pathlib.Path(__file__).parent.parent
DOC_DIR = DOC_SOURCE_DIR.parent
BASE_DIR = DOC_SOURCE_DIR.parent
ACTIONS_PREFIXES = ("get-", "scade-", "create-", "tests-")
ACTIONS_SUFFIXES = ""
ACTIONS_INPUTS_FIELDS = ("description", "required", "default")
ACTIONS_OUTPUTS_FIELDS = ("description",)
# Project information
project = "Ansys SCADE Actions"
copyright = f"(c) 2023-{datetime.today().year} ANSYS, Inc. and/or its affiliates."
author = "ANSYS, Inc."
cname = os.getenv("DOCUMENTATION_CNAME", "nocname.com")

# Read version from VERSION file in base root directory
source_dir = pathlib.Path(__file__).parent.resolve().absolute()
version_file = source_dir / "../../VERSION"
with open(str(version_file), "r") as file:
    __version__ = file.read().splitlines()[0]
release = version = __version__
branch_name = (
    "main"
    if __version__.endswith("dev0")
    else f"release/{get_version_match(__version__)}"
)
actions_version = (
    "main" if __version__.endswith("dev0") else f"v{get_version_match(__version__)}"
)

# Use the default pyansys logo
html_theme = "ansys_sphinx_theme"
html_favicon = ansys_favicon
html_short_title = html_title = project  # necessary for proper breadcrumb title
html_context = {
    "github_user": "ansys",
    "github_repo": "scade-actions",
    "github_version": "main",
    "doc_path": "doc/source",
}


# Specify the location of your GitHub repo
html_theme_options = {
    "github_url": "https://github.com/ansys/scade-actions",
    "use_edit_page_button": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(__version__),
    },
    "logo": "pyansys",
}

# Specify Sphinx extensions to use
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_jinja",
    "sphinx_design",
]

# Specify the static path
html_static_path = ["_static"]
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
]

# Add any paths that contain templates, relative to this directory
templates_path = ["_templates"]

# Specify the suffixes of source filenames
source_suffix = ".rst"

# Specify the master toctree document
master_doc = "index"

# Generate section labels for up to four levels
# autosectionlabel_maxdepth = 2

# TODO: remove this when library is public
linkcheck_ignore = [
    r"https://github.com/ansys/scade-actions*",
]

suppress_warnings = ["design.fa-build"]


def is_valid_action_dir(path):
    """Verify if a directory is a valid action directory.

    The directory is valid if it has a valid action pattern name and contains
    an ``action.yml`` file.

    Parameters
    ----------
    path : ~pathlib.Path
        The ``Path`` instance to verify if contains an ``action.yml`` and has a valid pattern.

    Returns
    -------
    bool
        Returns ``True`` if the directory is a valid one, ``False`` otherwise.

    """
    # Verify that the path is a directory and not a file
    if not path.is_dir():
        return False

    # Verify that the path contains an action.yml file
    if not (path / "action.yml").exists():
        return False

    # Verify if is a public and registered action
    if path.name.startswith(ACTIONS_PREFIXES) or path.name.endswith(ACTIONS_SUFFIXES):
        return True

    return False


def generate_description_from_action_file(action_file):
    """Generate the description of an action from the action file.

    Parameters
    ----------
    action_file : ~pathlib.Path
        A ``Path`` object representing the action file.

    Returns
    -------
    str
        String representing description of the action.

    """
    with open(action_file, "r") as yaml_file:
        file_content = yaml.safe_load(yaml_file)
        description = file_content["description"]
        source_code_link = f"{html_theme_options['github_url']}/blob/{branch_name}/{action_file.parent.name}/action.yml"
        return (
            description
            + f"\n`Source code for this action <{source_code_link}>`__ :fab:`github`"
        )


def _generate_io_table_from_action_file(action_file, kind, fields):
    """Generate the RST table containing all the input information for the action.

    Parameters
    ----------
    action_file : ~pathlib.Path
        A ``Path`` object representing the action file.
    kind : str
        Nature of the I/O, either "input" or "output".
    fields : List[str]
        Name of the fields associated to the I/O.

    Returns
    -------
    str
        String representing the RST table.

    """
    field_names = (kind,) + fields
    headers = [field.capitalize() for field in field_names]
    table_content = []

    with open(action_file, "r") as yaml_file:
        file_content: dict = yaml.safe_load(yaml_file)
        ios = file_content.get(kind + "s", None)
        if ios:
            for io_name, values in ios.items():
                values = [
                    values.get(field, None) for field in field_names if field != kind
                ]
                table_row = [io_name]
                table_row.extend(values)
                table_content.append(table_row)
            return str(Table(table_content, headers=headers, tablefmt="grid"))
        else:
            return ""


def generate_inputs_table_from_action_file(action_file):
    """Generate the RST table containing all the input information for the action.

    Parameters
    ----------
    action_file : ~pathlib.Path
        A ``Path`` object representing the action file.

    Returns
    -------
    str
        String representing the RST table.

    """
    return _generate_io_table_from_action_file(
        action_file, "input", ACTIONS_INPUTS_FIELDS
    )


def generate_outputs_table_from_action_file(action_file):
    """Generate the RST table containing all the output information for the action.

    Parameters
    ----------
    action_file : ~pathlib.Path
        A ``Path`` object representing the action file.

    Returns
    -------
    str
        String representing the RST table.

    """
    return _generate_io_table_from_action_file(
        action_file, "output", ACTIONS_OUTPUTS_FIELDS
    )


# Collect all public actions directories and files
public_actions = {
    action_dir: action_dir / "action.yml"
    for action_dir in BASE_DIR.iterdir()
    if is_valid_action_dir(action_dir)
}

# Generate the Jinja contexts for the input tables
jinja_contexts = {
    action_dir.name: {
        "description": generate_description_from_action_file(action_file),
        "inputs_table": generate_inputs_table_from_action_file(action_file),
        "outputs_table": generate_outputs_table_from_action_file(action_file),
    }
    for action_dir, action_file in public_actions.items()
}


def render_example_template_with_actions_version(
    example_template_file, actions_version
):
    """Renders a example template with desired branch name.

    Parameters
    ----------
    example_template_file : ~pathlib.Path
        The ``Path`` for the example template file.
    actions_version : str
        A string representing the actions version.

    Returns
    -------
    example_rendered_file : ~pathlib.Path
        The ``Path`` for the rendered example file.

    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(example_template_file.parent)
    )
    example_template = env.get_template(example_template_file.name)
    content = example_template.render(version=actions_version)
    output_file_name = example_template_file.name[:-4] + "-rendered-example.yml"
    example_rendered_file = example_template_file.parent / output_file_name
    with open(example_rendered_file, "w") as file:
        file.write(content)
    return example_rendered_file


def collect_examples_from_action_name(action_name):
    """Returns a list of example files in the form of ``Path`` instances.

    Parameters
    ----------
    action_name : str
        The name of the action.

    Returns
    -------
    list[~pathlib.Path]
        A list of example files in the form of ``Path`` instances.

    """
    return [
        render_example_template_with_actions_version(path, actions_version)
        for path in DOC_SOURCE_DIR.glob("**/*")
        if path.is_file()
        and path.name.startswith(action_name)
        and not path.name.endswith("-rendered-example.yml")
    ]


def get_example_file_title(example_file):
    """Returns the title from a YML example file.

    Parameters
    ----------
    example_file : ~pathlib.Path
        The ``Path`` for the example file.

    Returns
    -------
    str
        A ``string`` representing the title of the example.

    Notes
    -----
    The string in the 'title' key of the example YML file is used. This key is
    contained within the first section of the action file, whose name is
    unknown. For this reason, the first key of the file is guessed and used
    then to retrieve the value of the 'title' key.

    """
    with open(example_file, "r") as yaml_file:
        file_content = yaml.safe_load(yaml_file)
        first_key = next(iter(file_content))
        return file_content[first_key]["name"]


# Add examples files and titles to the Jinja context for the action
for action_dir in public_actions:
    action_name = action_dir.name
    examples = collect_examples_from_action_name(action_name)
    if not len(examples):
        continue

    # Append examples to context
    jinja_contexts[action_name]["examples"] = [
        [file.name, get_example_file_title(file)] for file in examples
    ]
