from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model
from campaigns.models import CampaignModel
from events.models import EventModel
from siyazalana_home.forms import EmailForm, SearchForm
from siyazalana_home.models import Blog, Member
from siyazalana_home.tasks import send_email_to_admin
from siyazalana_home.utilities.decorators import user_not_superuser_or_staff
from django.contrib.auth.decorators import login_required

def home(request):
    events = EventModel.objects.all()
    campaigns = CampaignModel.objects.all()
    blogs = Blog.objects.all()[:5]
    return render(request, "home/home.html", {"events": events, "campaigns": campaigns, "posts": blogs})

def about_siyazalana(request):
    members = Member.objects.all()
    blogs = Blog.objects.all()[:5]
    return render(request, "home/about-us.html", {"members": members, "posts": blogs})

def contact(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            send_email_to_admin(form.cleaned_data["subject"], form.cleaned_data["message"], form.cleaned_data["from_email"], form.cleaned_data["name"])
            messages.success(request, "We have successfully receive your email, will be in touch shortly")
            return redirect("siyazalana_home:contact")
        else:
            messages.error(request, "Something went wrong, please fix errors below")
            for err in form.errors:
                messages.error(request, f"{err}")
                return render(request, "home/contact-us.html", {"form": form})
            
    form = EmailForm()
    return render(request, "home/contact-us.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def dashboard(request):
    events = EventModel.objects.all()
    campaigns = CampaignModel.objects.all()
    users = get_user_model().objects.all()
    return render(request, "dashboard/dashboard.html", {"events": events, "campaigns": campaigns, "users": users})

def search(request):

    form = SearchForm()
    query = request.GET.get("query", None)
    query_by = request.GET.get("search_by", None)
    place = request.GET.get("place", None)
    if not query:
        return render(request, "home/search.html")
    
    results_dic = {
        "campaigns" : CampaignModel.objects.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query)),
        "events": EventModel.objects.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query) | Q(event_address__icontains=place or query)),
        "news": Blog.objects.filter(Q(title__icontains=query)),
        }
    context = {}
    if query and query_by:
        context["results"] = results_dic[query_by]
        context["results_type"] = query_by
        context["query"] = query
    elif query:
        if results_dic["campaigns"].count() > 0:
            context["results"] = results_dic["campaigns"]
            context["results_type"] = "campaigns"
            context["query"] = query
        elif results_dic["events"].count() > 0:
            context["results"] = results_dic["events"]
            context["results_type"] = "events"
            context["query"] = query
        elif results_dic["news"].count() > 0:
            context["results"] = results_dic["news"]
            context["results_type"] = "news"
            context["query"] = query
        
        
        
    
    context["form"] = form
    
    return render(request, "home/search.html", context=context)

def terms_and_conditions(request):
    return render(request, "home/terms_and_conditions.html")

def privacy(request):
    return render(request, "home/privacy.html")

def refunds(request):
    return render(request, "home/refunds.html")

def faqs(request):
    blogs = Blog.objects.all()[:5]
    return render(request, "home/faqs.html", {"posts": blogs})
