from django import forms

class AthleteSortForm(forms.Form):
    ath_sort = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={'placeholder':'Please input athletes name:'}))

class RankingForm(forms.Form):
    LongCourse = 1
    ShortCourse = 2
    Men = 3
    Women = 4
    COURSE_CHOICE = ((1, 'Long Course(50m)'), (2, 'Short Course(25m)'))
    GENGER_CHOICE = ((3, 'Men'), (4, 'Women'))
    YEAR_CHOICE = ('2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005')
    course = forms.ChoiceField(choices=COURSE_CHOICE, widget=forms.RadioSelect(), label='Course')
    ranking_year = forms.ChoiceField(choices=YEAR_CHOICE, widget=forms.RadioSelect(), label='Ranking_year')
    gender = forms.ChoiceField(choices=YEAR_CHOICE, widget=forms.RadioSelect(), label='Gender')

class ContactForm(forms.Form):
    To = forms.CharField(required=True, initial='gavinli.615@gmail.com')
    Subject = forms.CharField(required=True)
    Comments = forms.CharField(widget=forms.Textarea)