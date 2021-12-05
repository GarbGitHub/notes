from django import forms
from notes.models import Note


class NoteEditForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('title', 'text', 'is_favorites')  # необходимые поля

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'title':
                field.widget.attrs['class'] = 'form-control input-title'
                field.widget.attrs['placeholder'] = field.label
            elif field_name == 'text':
                field.widget.attrs['class'] = 'form-control input-text'
                field.widget.attrs['placeholder'] = field.label
            elif field_name == 'is_favorites':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''
            field.label = ''

        # self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})


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
