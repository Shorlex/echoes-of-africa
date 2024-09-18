from django import forms
from .models import Hero, HeroImage, Comment

class HeroForm(forms.ModelForm):
    # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)
    
    class Meta:
        model = Hero
        fields = ['name', 'nationality', 'year_of_birth', 'year_of_death', 'body', 'banner']

class HeroImageForm(forms.ModelForm):
    # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    class Meta:
        model = HeroImage
        fields = ("image",)

    # def save(self, commit=True):
    #     hero = super().save(commit=commit)
    #     images = self.files.getlist('images')
    #     for image in images:
    #         HeroImage.objects.create(hero=hero, image=image)
    #     return hero

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment", "parent"]
        widgets = {
            "comment": forms.Textarea(attrs={'rows': 1}),
            "parent": forms.HiddenInput()
        }
