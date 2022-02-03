from django import forms
from notes.models import Note


class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text', 'created', 'is_favorites')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'title':
                field.widget.attrs['class'] = 'form-control input-title'
                field.widget.attrs['placeholder'] = field.label
                field.widget.attrs['maxlength'] = "128"

            elif field_name == 'created':
                field.widget.attrs['class'] = 'd-none'
                field.required = False

            elif field_name == 'text':
                field.widget.attrs['class'] = 'form-control input-text'
                field.widget.attrs['placeholder'] = field.label

            elif field_name == 'is_favorites':
                field.widget.attrs.update({'class': 'form-check-input'})

            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''
            field.label = ''


class NoteUpdateForm(NoteCreateForm):
    class Meta:
        model = Note
        fields = ('title', 'text', 'is_favorites')


class NoteBasketForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('is_active',)  # необходимые поля

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoteReturnBasketForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('is_active',)  # необходимые поля

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
