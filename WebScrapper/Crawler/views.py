from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View
from .models import Athletes,Matchinfo,Meet,ParticipatingNation,Personalbest,Ranking,Recordlist,Records
from Crawler.forms import ContactForm,AthleteSortForm
# Create your views here.

class MyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Crawler/home.html')

class AthletesListView(View):
    def get(self, request, **kwargs):
        if request.method == 'GET':
            form = AthleteSortForm()
            athletesList = Athletes.objects.distinct()
            return render(request, 'Crawler/athletes.html', {'athletesList': athletesList, 'form': form})

    def post(self, request):
        form =AthleteSortForm(request.POST)
        if form.is_valid():
            athletes = form.cleaned_data['ath_sort']
            athletesList = Athletes.objects.filter(name=athletes)
            return render(request, 'Crawler/athletesSearch.html', {'athletesList': athletesList})

class AthletesDetailsView(View):
    def get(self, request, athletes_id):
        personal_best = Personalbest.objects.filter(athletes=athletes_id).values()
        name = Athletes.objects.get(athletes_id=athletes_id)
        return render(request, 'Crawler/personalbest.html', {'personal_best': personal_best, 'name': name.name})

class RecordListView(View):
    def get(self, request, **kwargs):
        recordlist = Recordlist.objects.all().values()
        return render(request, 'Crawler/recordlist.html', {'recordlist': recordlist})

class RecordDetailView(View):
    def get(self, request, id):
        record=Records.objects.filter(recordlist_id=id).values()
        recordname= Recordlist.objects.get(id=id)
        return render(request, 'Crawler/records.html', {'record': record, 'recordname': recordname.recordlist})


class CalenderView(View):
    def get(self, request, **kwargs):
        match=Matchinfo.objects.all().values()
        return render(request, 'Crawler/calender.html', {'match': match})

class RankingView(View):
    model = Ranking
    template_name = 'Crawler/ranking.html'
    def get(self, request, *args, **kwargs):
        ranking =Ranking.objects.all().values()
        coursedic = Ranking.objects.values('course').distinct()
        genderdic = Ranking.objects.values('gender').distinct()
        yeardic = Ranking.objects.values('ranking_year').distinct()
        return render(request, self.template_name, {'ranking': ranking, 'coursedic': coursedic, 'genderdic': genderdic, 'yeardic': yeardic})

    def post(self, request):
        if request.method == 'POST':
                course = request.POST['course']
                year = request.POST['ranking_year']
                gender = request.POST['gender']
                ranking = Ranking.objects.filter(course=course).filter(ranking_year=year).filter(gender=gender).values()
                return render(request, 'Crawler/rankingcondition.html', {'ranking': ranking})

class MeetView(View):
    def get(self, request, **kwargs):
        meet = Meet.objects.all().values()
        typedic = Meet.objects.values('meet_type').distinct()
        return render(request, 'Crawler/meet.html', {'meet': meet, 'typedic':typedic})
    def post(self, request):
        if request.method == 'POST':
                type = request.POST['meet_type']
                meet = Meet.objects.filter(meet_type=type).values()
                return render(request, 'Crawler/meetfilter.html', {'meet_type': meet})

class MeetDetailView(View):
    def get(self, request, meets_id):
        medal = ParticipatingNation.objects.filter(meet_id=meets_id).values()
        return render(request, 'Crawler/medal.html', {'medal': medal})

class EmailView(View):
    def get(self, request):
        if request.method == 'GET':
            form = ContactForm()
            return render(request, "Crawler/email.html", {'form': form})

    def post(self,request):
            form = ContactForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['Subject']
                from_email = settings.EMAIL_HOST_USER
                message = form.cleaned_data['Comments']
                try:
                    send_mail(subject, message, from_email, ['li1j5@uwindsor.ca', settings.EMAIL_HOST_USER], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            return HttpResponse('Thank you for your message,We will reply to you as soon as possible.')
