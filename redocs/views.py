from django.shortcuts import render
from .api_parser import ApiParser
import json


def walk_endpoints(tree, endpoints=None):
    if endpoints is None:
        endpoints = []

    for k, v in tree.items():
        if type(v) == dict:
            walk_endpoints(v, endpoints)
        else:
            endpoints.append({
                'path': v.complete_path,
                'auth': v.authentication_classes,
                'methods': v.methods,
                'input': v.input_fields if hasattr(v, 'input_fields') else None,
                'doc': v.docstring,
            })

    return endpoints


def get_endpoints(request):
    api_parser = ApiParser()
    api_parser.parse()
    endpoints = walk_endpoints(api_parser.endpoints)

    return render(request, 'redocs/index.html', {
        'endpoints': json.dumps(endpoints),
    })
