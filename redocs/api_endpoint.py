from rest_framework.serializers import BaseSerializer, ChoiceField, RelatedField, ManyRelatedField
from inspect import getdoc
from django.contrib.admindocs.views import simplify_regex


class ApiEndpoint:
    def __init__(self, pattern, prefix=None):
        self.pattern = pattern
        self.view = pattern.callback
        self.methods = self._get_allowed_methods()
        self.complete_path = self._get_complete_path(pattern, prefix)
        self.name = self._get_endpoint_name()
        self.docstring = str(self._get_doc())

        if hasattr(self.view.cls, 'extra_url_params'):
            self.extra_url_params = self.view.cls.extra_url_params

        if hasattr(self.view.cls, 'authentication_classes') and self.view.cls.authentication_classes is not None:
            self.authentication_classes = [(cls.__name__, getdoc(cls)) for cls in self.view.cls.authentication_classes]

        if hasattr(self.view.cls, 'permission_classes') and self.view.cls.permission_classes is not None:
            self.permission_classes = [(cls.__name__, getdoc(cls)) for cls in self.view.cls.permission_classes]

        if hasattr(self.view.cls, 'serializer_class') and self.view.cls.serializer_class is not None:
            if not set(self.methods) == {'GET', 'OPTIONS'}:
                self.input_fields = self._get_serializer_fields(self.view.cls.serializer_class())
            else:
                self.output_fields = self._get_serializer_fields(self.view.cls.serializer_class())

        if hasattr(self.view.cls, 'response_serializer_class'):
            self.output_fields = self._get_serializer_fields(self.view.cls.response_serializer_class())

    def _get_doc(self):
        no_description = "No description provided by developer"
        try:
            return self.view.cls.__doc__ if self.view.cls.__doc__ is not None else no_description
        except AttributeError:
            return no_description

    def _get_endpoint_name(self):
        if self.pattern.name:
            return self.pattern.name.replace('-', ' ').replace('_', ' ').title()
        return self.pattern.lookup_str

    def _get_allowed_methods(self):
        if hasattr(self.view, 'cls'):
            return [m.upper() for m in self.view.cls.http_method_names if hasattr(self.view.cls, m)]
        else:
            return []

    @staticmethod
    def _get_complete_path(pattern, prefix=None):
        try:
            regex = pattern._regex if hasattr(pattern, "_regex") else pattern.pattern._regex
        except:
            regex = pattern._route if hasattr(pattern, "_route") else pattern.pattern._route
        return prefix + simplify_regex(regex)[1:]

    def _get_serializer_fields(self, serializer):
        fields = []

        if hasattr(serializer, 'get_fields'):
            for key, field in serializer.get_fields().items():
                to_many_relation = True if hasattr(field, 'many') else False
                sub_fields = []

                if to_many_relation:
                    sub_fields = self._get_serializer_fields(field.child) if isinstance(field, BaseSerializer) else None
                else:
                    sub_fields = self._get_serializer_fields(field) if isinstance(field, BaseSerializer) else None
                field_data = {
                    "name": key,
                    "read_only": field.read_only,
                    "type": str(field.__class__.__name__),
                    "sub_fields": sub_fields,
                    "required": field.required,
                    "to_many_relation": to_many_relation,
                    "help_text": str(field.help_text),
                    "write_only": field.write_only
                }
                if isinstance(field, ChoiceField) and not isinstance(field, (RelatedField, ManyRelatedField)):
                    field_data['choices'] = field.choices

                if isinstance(field, RelatedField):
                    if hasattr(field, 'queryset') and hasattr(field.queryset, 'model'):
                        field_data['help_text'] = ('{}\nRequires/renders pk(id) of {} as integer'.format(
                            field.help_text if field.help_text else "",
                            field.queryset.model.__name__)
                        )
                    elif hasattr(serializer.Meta.model, key):
                        field_data['help_text'] = ('{}\nRequires/renders pk(id) of {} as integer'.format(
                            field.help_text if field.help_text else "",
                            getattr(serializer.Meta.model, key).field.related_model.__name__)
                        )
                elif isinstance(field, ManyRelatedField):
                    if hasattr(field, 'queryset') and hasattr(field.queryset, 'model'):
                        field_data['help_text'] = ("{}\nRequires/renders list of pk's(id's) of {} objects.".format(
                            field.help_text if field.help_text else "",
                            field.child_relation.queryset.model.__name__)
                        )
                    elif hasattr(serializer.Meta.model, key):
                        field_data['help_text'] = ('{}\nRequires/renders pk(id) of {} as integer'.format(
                            field.help_text if field.help_text else "",
                            getattr(serializer.Meta.model, key).field.related_model.__name__)
                        )

                fields.append(field_data)

        return fields


