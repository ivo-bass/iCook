class AddBootstrapFormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    def add_form_control(self):
        for _, field in self.fields.items():
            try:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = ''
                field.widget.attrs['class'] += ' form-control'
            except:
                continue