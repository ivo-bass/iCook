class AddBootstrapFormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    def add_form_control(self):
        for name, field in self.fields.items():
            if name in ('meal_type',):
                try:
                    if 'class' not in field.widget.attrs:
                        field.widget.attrs['class'] = ''
                    field.widget.attrs['class'] += ' form-select'
                except:
                    continue
            if name in ('public', 'vegetarian'):
                try:
                    if 'class' not in field.widget.attrs:
                        field.widget.attrs['class'] = ''
                    field.widget.attrs['class'] += ' form-check-input'
                except:
                    continue
            else:
                try:
                    if 'class' not in field.widget.attrs:
                        field.widget.attrs['class'] = ''
                    field.widget.attrs['class'] += ' form-control'
                except:
                    continue