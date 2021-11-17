from django import forms
from notes.models import Note


class NoteEditForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('title', 'text')  # необходимые поля

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field_name.title
            if field_name == 'title':
                field.widget.attrs['class'] = 'form-control input-title'
            elif field_name == 'text':
                field.widget.attrs['class'] = 'form-control input-text'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            field.label = ''
        # self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
