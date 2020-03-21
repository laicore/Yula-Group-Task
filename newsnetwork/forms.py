from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import PostModel


class SignUpForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=40, label="Логин:")
    password = forms.CharField(min_length=8, max_length=50,
                               label="Пароль:", widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=8, max_length=50,
                                label="Повторите пароль:", widget=forms.PasswordInput)
    email = forms.EmailField(min_length=5, max_length=50,
                             widget=forms.EmailInput, label='Email:', error_messages={
                                 'invalid': 'Некорретный формат Email.',
                             })

    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            if User.objects.get(username=user):
                raise forms.ValidationError(
                    'Пользователь с таким логином уже существует!')
        except ObjectDoesNotExist:
            return user

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            if User.objects.get(email=email):
                raise forms.ValidationError(
                    'Почта занята другим пользователем!')
        except ObjectDoesNotExist:
            return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password2 != password:
            raise forms.ValidationError(
                'Введеные пароли не совпадают', code=12)
        return password

    def save(self):
        user = User.objects.create_user(self.cleaned_data['username'],
                                        self.cleaned_data['email'],
                                        self.cleaned_data['password'])
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=40, label="Логин:")
    password = forms.CharField(min_length=1, max_length=50,
                               label="Пароль:", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            if User.objects.get(username=username):
                return username
        except ObjectDoesNotExist:
            raise forms.ValidationError('Логин или пароль введен неправильно')

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            if User.objects.get(
                    username=self.data['username']).check_password(password):
                return password
            raise forms.ValidationError('Логин или пароль введен неправильно')
        except ObjectDoesNotExist:
            raise forms.ValidationError('Логин или пароль введен неправильно')

    def save(self):
        return self.cleaned_data


class AddNewsForm(forms.ModelForm):
    def __init__(self, user=None, **kwargs):
        super(AddNewsForm, self).__init__(**kwargs)
        if user:
            self.user = user

    class Meta:
        model = PostModel
        fields = ['name', 'text', 'image']
        widgets = {
            'text': forms.Textarea(),
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        image = 1 if 'image' in self.files else None
        if text is None and image is None:
            print('сработал клин text')
            raise forms.ValidationError(
                'Должен быть заполнен хотя бы текст или загружено изображение')
        return text

    def clean_image(self):
        text = self.data['text']
        image = self.cleaned_data['image']
        if text is '' and image is None:
            print('сработал клин image')
            raise forms.ValidationError(
                'Должен быть заполнен хотя бы текст или загружено изображение')
        return image

    def save(self):
        post = PostModel(**self.cleaned_data, author=self.user)
        post.save()
        return post
