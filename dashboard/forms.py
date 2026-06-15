from django import forms
from .models import UploadedFile


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ['file']

    def clean_file(self):

        file = self.cleaned_data['file']

        allowed_extensions = [
            '.csv',
            '.xlsx',
            '.xls'
        ]

        if not any(
            file.name.endswith(ext)
            for ext in allowed_extensions
        ):
            raise forms.ValidationError(
                "Only CSV, XLSX and XLS files are allowed."
            )

        return file