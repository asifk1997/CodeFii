from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from  .forms import ProblemsetForm, ProblemForm, UserForm, SubmissionForm
from . models import Problemset, Problem ,Submission
from . import  forms
import requests
import json
import  datetime

TEXT_FILE_TYPES = ['pdf','txt']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_problemset(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = ProblemsetForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            problemset = form.save(commit=False)
            problemset.user = request.user
            problemset.problemset_logo = request.FILES['problemset_logo']
            file_type = problemset.problemset_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'problemset': problemset,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_problemset.html', context)
            problemset.save()
            return render(request, 'music/detail.html', {'problemset': problemset})
        context = {
            "form": form,
        }
        return render(request, 'music/create_problemset.html', context)


def create_problem(request, problemset_id):
    form = ProblemForm(request.POST or None, request.FILES or None)
    problemset = get_object_or_404(Problemset, pk=problemset_id)
    if form.is_valid():
        problemsets_problems = problemset.problem_set.all()
        for s in problemsets_problems:
            if s.problem_title == form.cleaned_data.get("problem_title"):
                context = {
                    'problemset': problemset,
                    'form': form,
                    'error_message': 'You already added that problem',
                }
                return render(request, 'music/create_problem.html', context)
        problem = form.save(commit=False)
        problem.problemset = problemset
        #problem.problem_file = request.FILES['text_file']
        #file_type = problem.text_file.url.split('.')[-1]
        # file_type = file_type.lower()
        # if file_type not in TEXT_FILE_TYPES:
        #     context = {
        #         'problemset': problemset,
        #         'form': form,
        #         'error_message': 'Audio file must be WAV, MP3, or OGG',
        #     }
        #     return render(request, 'music/create_problem.html', context)

        problem.save()
        return render(request, 'music/detail.html', {'problemset': problemset})
    context = {
        'problemset': problemset,
        'form': form,
    }
    return render(request, 'music/create_problem.html', context)


def delete_problemset(request, problemset_id):
    problemset = Problemset.objects.get(pk=problemset_id)
    problemset.delete()
    problemsets = Problemset.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'problemsets': problemsets})


def delete_problem(request, problemset_id, problem_id):
    problemset = get_object_or_404(Problemset, pk=problemset_id)
    problem = Problem.objects.get(pk=problem_id)
    problem.delete()
    return render(request, 'music/detail.html', {'problemset': problemset})


def detail(request, problemset_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        problemset = get_object_or_404(Problemset, pk=problemset_id)
        return render(request, 'music/detail.html', {'problemset': problemset, 'user': user})



def problemdetail(request, problemset_id,problem_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        problem=get_object_or_404(Problem,pk=problem_id)
        form = SubmissionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.verdict=False
            submission.time=datetime.datetime.now()
            submission.save()

            return render(request, 'music/problemdetail.html', {'submission': submission})
        pn=problem.problem_title
        sub1 = Submission.objects.filter(problem__problem_title=pn).order_by('id')
        context = {
            'sub1':sub1,
            "form": form,
        }

        return render(request, 'music/problemdetail.html', context)



def solution_verdict(request,problemset_id,problem_id,submission_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        problem=get_object_or_404(Problem,pk=problem_id)
        p=problem.problem_expected_output.read()
        exp_out=str(p)
        submission=get_object_or_404(Submission,pk=submission_id)
        t=submission.code.read()
        d = t.decode('ASCII')
        exp_out=str(exp_out)
        exp_out=exp_out[2:-1]
        submission.my_output=exp_out
        payload = {"script": d,
                    "language": "c",
                   "versionIndex": "0",
                   "clientId": "c502938ae0bff7cc4d2d17553ea8a8bb",
                   "clientSecret": "85ce5b166d02a25e092f0057d3daebcf6f7b22cfd28d905d1f2b25166c915782",
                   }
        response = requests.post('https://api.jdoodle.com/execute', json=payload)
        data = json.loads(response.text)
        out=str(data['output'])
        if (data['output']==exp_out):
            submission.verdict=True
        else:
            submission.verdict=False
        submission.save()
        return render(request,'music/solution_verdict.html',{'out':out,'problem':problem,'submission':submission,'exp_out':exp_out})

def favorite(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    try:
        if problem.is_favorite:
            problem.is_favorite = False
        else:
            problem.is_favorite = True
        problem.save()
    except (KeyError, Problem.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_problemset(request, problemset_id):
    problemset = get_object_or_404(Problemset, pk=problemset_id)
    try:
        if problemset.is_favorite:
            problemset.is_favorite = False
        else:
            problemset.is_favorite = True
        problemset.save()
    except (KeyError, Problemset.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        problemsets = Problemset.objects.all()
        problem_results = Problem.objects.all()
        query = request.GET.get("q")
        if query:
            problemsets = problemsets.filter(
                Q(problemset_title__icontains=query) |
                Q(curator__icontains=query)
            ).distinct()
            problem_results = problem_results.filter(
                Q(problem_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'problemsets': problemsets,
                'problems': problem_results,
            })
        else:
            return render(request, 'music/index.html', {'problemsets': problemsets})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                problemsets = Problemset.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'problemsets': problemsets})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                problemsets = Problemset.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'problemsets': problemsets})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def problems(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            problem_ids = []
            for problemset in Problemset.objects.all():
                for problem in problemset.problem_set.all():
                    problem_ids.append(problem.pk)
            users_problems = Problem.objects.filter(pk__in=problem_ids)
            if filter_by == 'favorites':
                users_problems = users_problems.filter(is_favorite=True)
        except Problemset.DoesNotExist:
            users_problems = []
        return render(request, 'music/problems.html', {
            'problem_list': users_problems,
            'filter_by': filter_by,
        })


def pdf_view(request):

    try:
        return FileResponse(open(file, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()