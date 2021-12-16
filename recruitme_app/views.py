from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.db.models import Q

from recruitme_app.forms import UserRegistrationForm, WorkerProfileForm, LoginForm, JobProfileForm, JobApplyForm, \
    SkillsForm, RequirementsForm, ResponseForm
from recruitme_app.models import JobProfile, WorkerProfile, Apply, UserProfile, SkillTag, Requirements


class HomeView(View):

    def get(request):
        jobs = JobProfile.objects.all()
        return render(request, 'recruitme_app/home.html', context={'jobs': jobs})


class RegistrationView(View):
    """Registrating user"""

    def get(self, request):
        form = UserRegistrationForm()
        return render(request=request, template_name='recruitme_app/registration.html', context={'register_form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request=request, template_name='recruitme_app/registration.html', context={'register_form': form})


class LoginView(View):
    """User login view"""

    def get(self, request):
        form = LoginForm
        return render(request, 'recruitme_app/loginuser.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'recruitme_app/loginuser.html',
                              {'form': form, 'error': 'User doesn`t exist or password is incorrect. Please try again.'})


class WorkerRegistrationView(View):
    """Adding personal dates of worker"""

    def get(self, request):
        skills = SkillTag.objects.filter(owner=request.user)
        if WorkerProfile.objects.filter(workername=request.user).exists():
            worker = WorkerProfile.objects.get(workername=request.user)
            form = WorkerProfileForm(instance=worker)
        else:
            form = WorkerProfileForm()
        return render(request=request, template_name='recruitme_app/worker_profile.html',
                      context={'worker_form': form, 'skills': skills})

    def post(self, request):
        if WorkerProfile.objects.filter(workername=request.user).exists():
            worker = WorkerProfile.objects.get(workername=request.user)
            form = WorkerProfileForm(request.POST, request.FILES, instance=worker)
        else:
            form = WorkerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            worker_profile = form.save(commit=False)
            worker_profile.workername = request.user
            worker_profile.save()
            form.save_m2m()
            return redirect('home')
        return render(request=request, template_name='recruitme_app/worker_profile.html', context={'worker_form': form})


class SkillsRegistrationView(View):
    """Adding skills for worker"""

    def get(self, request):
        form = SkillsForm()
        skills = SkillTag.objects.filter(owner=request.user)
        return render(request=request, template_name='recruitme_app/skills.html',
                      context={'skills_form': form, 'skills': skills})

    def post(self, request):
        form = SkillsForm(request.POST)
        if form.is_valid():
            if not SkillTag.objects.filter(tagname=request.POST.get('tagname')).exists():
                form.save()
            tag = get_object_or_404(SkillTag, tagname=request.POST.get('tagname'))
            tag.owner.add(request.user)
            return redirect('skills')
        return render(request=request, template_name='recruitme_app/skills.html', context={'skills_form': form, 'message': 'Enter correct data please'})


class JobRegistrationView(View):
    """Adding new job position"""

    def get(self, request):
        form = JobProfileForm()

        return render(request=request, template_name='recruitme_app/job_registration.html',
                      context={'job_form': form})

    def post(self, request):
        form = JobProfileForm(request.POST)
        if form.is_valid():
            job_position = form.save(commit=False)
            job_position.employername = request.user
            job_position.save()
            form.save_m2m()
            return redirect('home')
        return render(request=request, template_name='recruitme_app/job_registration.html', context={'job_form': form})


class RequirementsRegistrationView(View):
    """Add requirements to job position"""

    def get(self, request, id):
        form = RequirementsForm()
        job = get_object_or_404(JobProfile, id=id)
        requirements = Requirements.objects.filter(job=job)
        return render(request=request, template_name='recruitme_app/requirements.html', context={'form': form, 'requirements': requirements, 'job': job})

    def post(self, request, id):
        form = RequirementsForm(request.POST)
        job = get_object_or_404(JobProfile, id=id)
        if form.is_valid():
            if not Requirements.objects.filter(rname=request.POST.get('rname')).exists():
                form.save()
            requirement = get_object_or_404(Requirements, rname=request.POST.get('rname'))
            requirement.job.add(job)
            return redirect(request.META.get('HTTP_REFERER'))
        return render(request=request, template_name='recruitme_app/requirements.html', context={'form': form, 'message': 'Enter correct data please'})


class JobListView(View):
    """Viewing list of jobs for workers"""

    def get(self, request):
        if request.user.is_authenticated:
            jobs = JobProfile.objects.all()
            paginator = Paginator(jobs, 10)
            page_number = request.GET.get('page')
            page_object = paginator.get_page(page_number)
            jobs_c = JobProfile.objects.filter(employername=request.user)
            paginator_c = Paginator(jobs_c, 10)
            page_number_c = request.GET.get('page')
            page_object_c = paginator_c.get_page(page_number_c)
            return render(request, 'recruitme_app/home.html',
                          context={'page_object': page_object, 'page_object_c': page_object_c})
        return render(request, 'recruitme_app/home.html')


class SearchJobView(View):
    """View for search jobs by requirements"""

    def get(self, request):
        model = JobProfile
        query = request.GET.get('search_job')
        if query is not None:
            results = model.objects.filter(Q(offer_name__icontains=query) | Q(description__icontains=query))
        else:
            results = model.objects.none()
        return render(request, 'recruitme_app/search_job.html', context={'results': results})


class SearchCvView(View):
    """View for search CV`s"""

    def get(self, request):
        model = WorkerProfile
        query = request.GET.get('search_cv')
        if query is not None:
            results = model.objects.filter(Q(offer_name__icontains=query) | Q(description__icontains=query))
        else:
            results = model.objects.none()
        return render(request, 'recruitme_app/search_cv.html', context={'results_cv': results})


class JobDetail(View):
    """Viewering details of job"""

    def get(self, request, id):
        applies = Apply.objects.filter(job=id)
        job = get_object_or_404(JobProfile, id=id)
        requirements = Requirements.objects.filter(job=job)
        skills = SkillTag.objects.filter(owner=request.user)
        match = 100
        if len(requirements) > 0:
            matches_qset = set()
            for skill in skills:
                for requirement in requirements:
                    if str(skill) == str(requirement):
                        matches_qset.add(skill)
            match = (len(matches_qset) / len(requirements)) * 100
        if Apply.objects.filter(worker=request.user, job=id):
            return render(request, 'recruitme_app/job_detail.html',
                          context={'job': job,
                                   'message': 'You had already applied for this position',
                                   'applies': applies,
                                   'requirements': requirements,
                                   'skills': skills,
                                   'match': match,
                                   })
        apply_form = JobApplyForm()
        job_registration_form = JobProfileForm(instance=job)
        return render(request, 'recruitme_app/job_detail.html',
                      context={'job': job,
                               'apply_form': apply_form,
                               'job_registration_form': job_registration_form,
                               'applies': applies,
                               'requirements': requirements,
                               'skills': skills,
                               'match': match,
                               }
                      )

    def post(self, request, id):
        """Appliyng to the job position"""
        if request.user.user_type == 'HJ':
            model = JobProfile.objects.filter(id=id)
            model.update(offer_name=request.POST.get('offer_name'), description=request.POST.get('description'))
            return redirect('home')
        else:
            apply_form = JobApplyForm(request.POST, request.FILES)
            if apply_form.is_valid():
                apply_profile = apply_form.save(commit=False)
                apply_profile.worker = request.user
                apply_profile.job = JobProfile.objects.filter(id=id)[0]
                apply_profile.save()
                apply_form.save_m2m()
                return redirect(request.META.get('HTTP_REFERER'))
            return render(request, 'recruitme_app/job_detail.html', context={'apply_form': apply_form})


def apply_view(request, id):
    application = get_object_or_404(Apply, id=id)
    application.read = True
    application.read_date = timezone.now()
    response_form = ResponseForm()
    return render(request, 'recruitme_app/apply.html',
                  {'application': application, 'response_form': response_form})


def response(request, id):
    """Employer response"""
    application = Apply.objects.filter(id=id)
    print(application)
    if request.POST.get('employer_comment') != '':
        application.update(state=request.POST.get('state'), employer_comment=request.POST.get('employer_comment'),
                           read_date=timezone.now())
    else:
        print('here')
        return render(request, 'recruitme_app/apply.html',
                      {'error': 'You have to write a comment'})
        # return redirect(request.META.get('HTTP_REFERER'))#render(request, 'recruitme_app/apply.html', {'error': 'You have to write a comment'})
    return redirect(request.META.get('HTTP_REFERER'))


def delete(request, id):
    """Deleting job object"""
    job = get_object_or_404(JobProfile, id=id, employername=request.user)
    job.delete()
    return redirect('home')

def delete_skill(request, tagname):
    """Deleting skill"""
    skill = get_object_or_404(SkillTag, tagname=tagname, owner=request.user)
    skill.owner.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

def delete_requirement(request, rname, id):
    """Deleting requirement"""
    job = get_object_or_404(JobProfile, id=id, employername=request.user)
    requirement = get_object_or_404(Requirements, rname=rname, job=job)
    requirement.job.remove(job)
    return redirect(request.META.get('HTTP_REFERER'))