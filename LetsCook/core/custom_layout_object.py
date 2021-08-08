from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from django.template.loader import render_to_string


class Formset(LayoutObject):
    """
    Finds keyword in context and applies html.
    Allows to set the order of the fields,
    wraps them in divs or other structures,
    adds html, sets ids, classes or attributes.
    """
    template = "shared/formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})
