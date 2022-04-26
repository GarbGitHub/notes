from django import forms

from notes.models import Note, Tag


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'title':
                field.widget.attrs['class'] = 'form-control search'
                field.widget.attrs['placeholder'] = field.label
                field.widget.attrs['maxlength'] = "128"

            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''
            field.label = ''


class TagUpdateForm(TagCreateForm):
    class Meta:
        model = Tag
        fields = ('title',)


class NoteCreateForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'text', 'tags', 'created', 'is_favorites']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_tags = Tag.get_tag(kwargs['initial']['user_pk'])
        self.fields['tags'].queryset = user_tags

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

            elif field_name == 'tags':
                if len(user_tags) > 0:
                    field.widget.attrs.update({'class': 'selectpicker dropup'})
                    field.widget.attrs['data-dropup-auto'] = "false"
                    field.widget.attrs['title'] = "Добавить теги"
                    field.widget.attrs['data-width'] = "auto"
                    field.widget.attrs['data-size'] = "5"
                else:
                    field.widget.attrs['style'] = "display:none"
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''
            field.label = ''


class NoteUpdateForm(NoteCreateForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'tags', 'is_favorites']


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
