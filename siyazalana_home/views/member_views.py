from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from siyazalana_home.forms import MemberForm
from siyazalana_home.models import Member
from siyazalana_home.utilities.decorators import user_not_superuser_or_staff

@login_required
@user_not_superuser_or_staff
def team_members(request):
    members = Member.objects.all()
    return render(request, "dashboard/members/members.html", {"members": members})

def team_member_details(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, "teams/team-member-details.html", {"member": member})

@login_required
@user_not_superuser_or_staff
def create_member(request):
    form = MemberForm()
    if request.method == "POST":
        form = MemberForm(data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Team member was created successfully!")
            return redirect("siyazalana_home:team-members")
        else:
            messages.error(request, "Something went wrong trying to add a member")
            return render(request, "dashboard/members/create-member.html", {"form": form})
        
    return render(request, "dashboard/members/create-member.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def update_member(request, member_id):
    member = get_object_or_404(Member, id = member_id)
    form = MemberForm(instance=member)
    if request.method == "POST":
        form = MemberForm(instance=member, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            form.save()
            messages.success(request, "Team member was updated successfully!")
            return redirect("siyazalana_home:team-members")
        else:
            messages.error(request, "Something went wrong trying to update a member")
            return render(request, "dashboard/members/create-member.html", {"form": form})
        
    return render(request, "dashboard/members/create-member.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def delete_member(request, member_id):
    member = get_object_or_404(Member, id = member_id)
    member.delete()
    messages.success(request, "Member was deleted successfully!")    
    return redirect("siyazalana_home:team-members")