# from django import forms

# from .models import Match, Member


# class MatchForm(forms.ModelForm):

#     class Meta:
#         model = Match
#         fields = ("name", "number_of_court")
    
#     def __init__(self, *args, **kwargs):
#         for field in self.base_fields.values():
#             field.widget.attrs["class"] = "form-control"
#         super().__init__(*args, **kwargs)


# class MemberForm(forms.ModelForm):
    
#     class Meta:
#         model = Member
#         fields = ("name")
