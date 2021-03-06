import os
import nbformat
from nbconvert import HTMLExporter
import yaml


def get_project_root():
    """Return the root path for the project."""
    curdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(curdir, os.pardir))

def load_config(path):
    """Load the configuration from config."""
    return yaml.load(open(path, 'r'), Loader=yaml.Loader)

def convert_notebook(report_in_path, report_out_path, **kwargs):

    curdir = os.path.abspath(os.getcwd())
    indir, _ = os.path.split(report_in_path)
    outdir, _ = os.path.split(report_out_path)
    os.makedirs(outdir, exist_ok=True)

    config = {
        "ExecutePreprocessor": {"enabled": True},
        "TemplateExporter": {"exclude_output_prompt": True, "exclude_input": True, "exclude_input_prompt": True},
    }

    nb = nbformat.read(open(report_in_path), as_version=4)
    html_exporter = HTMLExporter(config=config)

    # change dir to notebook dir, to execute notebook
    os.chdir(indir)
    body, resources = (
        html_exporter
        .from_notebook_node(nb)
    )

    # change back to original directory
    os.chdir(curdir)

    with open(report_out_path, 'w') as fh:
        fh.write(body)