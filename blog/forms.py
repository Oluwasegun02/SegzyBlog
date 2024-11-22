from django import forms
from .models import BlogPost, Category, Comment, Tag
from ckeditor.widgets import CKEditorWidget

class BlogPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'tags', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_video(self):
        video = self.cleaned_data.get('video', False)
        if video:
            if video.size > 5 * 1024 * 1024:  # Limit video to 5MB
                raise forms.ValidationError("Video file is too large (max 5 MB).")
            # Check if video length is less than or equal to 5 minutes
            if hasattr(video, '_file') and video._file.get_duration() > 300:
                raise forms.ValidationError("Video length cannot exceed 5 minutes.")
        return video


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
