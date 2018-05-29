from django.conf import settings
from importlib import import_module
from django.utils.module_loading import import_string
try:
    from django.urls import URLPattern as RegexURLPattern
    from django.urls import URLResolver as RegexURLResolver
except:
    from django.core.urlresolvers import RegexURLResolver, RegexURLPattern	    
from rest_framework.views import APIView
from .api_endpoint import ApiEndpoint
from django.contrib.admindocs.views import simplify_regex


class ApiParser(object):
    def __init__(self, *args, **kwargs):
        self.endpoints = {}
        try:
            root_urlconf = import_string(settings.ROOT_URLCONF)
        except ImportError:
            # Handle a case when there's no dot in ROOT_URLCONF
            root_urlconf = import_module(settings.ROOT_URLCONF)
        if hasattr(root_urlconf, 'urls'):
            self.patterns = root_urlconf.urls.urlpatterns
        else:
            self.patterns = root_urlconf.urlpatterns

    def parse(self):
        self._parse(self.patterns, self.endpoints)

    def _parse(self, urlpatterns, parent_node, prefix=''):
        for pattern in urlpatterns:
            if isinstance(pattern, RegexURLResolver):
                child_node_name = self._get_pattern_name(pattern)

                if parent_node.get(child_node_name, None) is None:
                    parent_node[child_node_name] = {}

                self._parse(
                    urlpatterns=pattern.url_patterns,
                    parent_node=parent_node[child_node_name] if child_node_name else parent_node,
                    prefix='%s/%s' % (prefix, child_node_name)
                )

            elif isinstance(pattern, RegexURLPattern) and self._is_drf_pattern(pattern):
                api_endpoint = ApiEndpoint(pattern, prefix)
                parent_node[api_endpoint.name] = api_endpoint

    @staticmethod
    def _is_drf_pattern(pattern):
        if hasattr(pattern.callback, 'cls') and issubclass(pattern.callback.cls, APIView):
            return True
        if hasattr(pattern.callback, 'view_class') and issubclass(pattern.callback.view_class, APIView):
            return True
        return False

    @staticmethod
    def _get_pattern_name(pattern):
        if hasattr(pattern, '_regex'):
            return simplify_regex(pattern._regex)[1:]
        if hasattr(pattern, 'pattern'):
            _pattern = pattern.pattern
            if hasattr(_pattern, '_route'):
                return str(_pattern._route)
        return ''


