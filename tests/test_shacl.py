from pathlib import Path

import pytest
from rdf_utils.constraints import check_shacl_constraints
from rdf_utils.namespace import URL_SECORO_MM
from rdf_utils.resolver import install_resolver
from rdflib import Dataset

ROOT = Path(__file__).parent.parent
COMMON = [
    "environments/secorolab.env.json",
    "agents/isaac-sim.agn.json",
    "scenes/secorolab-env.scene.json",
    "scenes/isaac-agents.scene.json",
]
SHAPES = {
    f"{URL_SECORO_MM}/{path}": "turtle"
    for path in (
        "acceptance-criteria/bdd/bdd.shacl.ttl",
        "acceptance-criteria/bdd/environment.shacl.ttl",
        "acceptance-criteria/bdd/agent.shacl.ttl",
        "acceptance-criteria/bdd/execution-context.shacl.ttl",
        "languages/python.shacl.ttl",
        "observation.shacl.ttl",
        "time-constraint.shacl.ttl",
    )
}
BUNDLES = {
    "pickplace": COMMON
    + [
        "templates/pickplace.tmpl.json",
        "variations/pickplace-secorolab-isaac.var.json",
    ],
    "sorting": COMMON
    + ["templates/sorting.tmpl.json", "variations/sorting-secorolab-isaac.var.json"],
    "grc-pass": COMMON
    + ["templates/pickplace.tmpl.json", "variations/pickplace-grc-demo-pass.var.json"],
    "grc-fail": COMMON
    + ["templates/pickplace.tmpl.json", "variations/pickplace-grc-demo-fail.var.json"],
    "ros-execution": COMMON
    + [
        "templates/pickplace.tmpl.json",
        "variations/pickplace-secorolab-isaac.var.json",
        "execution/pickplace-secorolab-ros.obs.json",
    ],
}


@pytest.mark.parametrize("files", BUNDLES.values(), ids=BUNDLES)
def test_model_bundle_conforms_to_shacl(files):
    install_resolver()
    graph = Dataset()
    for path in files:
        graph.parse(ROOT / path, format="json-ld")

    check_shacl_constraints(graph, SHAPES)
