from django import forms
from plugins.models import Plugin, PluginSetting

class PluginUploadForm(forms.Form):
    """Form for uploading a plugin"""
    plugin_file = forms.FileField(
        help_text="Upload a ZIP file containing the plugin",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class PluginSettingForm(forms.ModelForm):
    """Form for plugin settings"""
    class Meta:
        model = PluginSetting
        fields = ['setting_value']
    
    def __init__(self, *args, **kwargs):
        setting_type = kwargs.pop('setting_type', None)
        setting_choices = kwargs.pop('choices', None)
        setting_required = kwargs.pop('required', False)
        
        super().__init__(*args, **kwargs)
        
        # Customize the field based on setting type
        if setting_type == 'checkbox':
            self.fields['setting_value'] = forms.BooleanField(
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )
        elif setting_type == 'number':
            self.fields['setting_value'] = forms.IntegerField(
                required=setting_required,
                widget=forms.NumberInput(attrs={'class': 'form-control'})
            )
        elif setting_type == 'textarea':
            self.fields['setting_value'] = forms.CharField(
                required=setting_required,
                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            )
        elif setting_type == 'select' and setting_choices:
            self.fields['setting_value'] = forms.ChoiceField(
                choices=setting_choices,
                required=setting_required,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
        else:
            # Default to text input
            self.fields['setting_value'].widget = forms.TextInput(attrs={'class': 'form-control'})
            self.fields['setting_value'].required = setting_required
