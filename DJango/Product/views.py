from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import PersonFilter
from account.auth import user_only
from django.contrib.auth import views as auth_views
# Create your views here.


@login_required
@user_only
def index(request):
    items = Product.objects.all()
    context = {
        'products': items, 'active_product': 'active'
    }
    return render(request, 'Product/django_web.html', context)
# ============================================ #


@login_required
@user_only
def post_product_data(request):
    form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'Product/postProduct.html', context)
# ============================================ #


@login_required
@user_only
def post_student(request):
    if request.method == 'POST':
        data = request.POST
        firstname = data['firstname']
        lastname = data['lastname']
        batch = data['batch']
        image_url = data['image_url']
        category = data['category']
        student = Student.objects.create(firstname=firstname, lastname=lastname, batch=batch,
                                         image_url=image_url, category=category)
        if student:
            return redirect('/product/studentForm')

    context = {'active_stu': 'active'}

    return render(request, 'Product/addStudent.html', context)


@login_required
@user_only
def get_student(request):
    students = Student.objects.all()
    context = {'students': students, 'active_student': 'active'}

    return render(request, 'Product/getStudents.html', context)


@login_required
@user_only
def delete_student(request, i_id):
    student = Student.objects.get(id=i_id)
    student.delete()

    return redirect('/product/getForm')


@login_required
@user_only
def update_student(request, i_id):
    student = Student.objects.get(id=i_id)
    if request.method == "POST":
        data = request.POST
        student.firstname = data['firstname']
        student.lastname = data['lastname']
        student.batch = data['batch']
        student.category = data['category']
        student.image_url = data['image_url']
        student.save()

        return redirect('/product/getForm')

    context = {'student': student}

    return render(request, 'Product/updateStudent.html', context)
# ============================================ #


@login_required
@user_only
def get_form(request):
    if request.method == 'POST':
        data = PersonForm(request.POST)
        if data.is_valid():
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Person Added Successfully')
            return redirect('/product/showpersonForm')
        else:
            messages.add_message(request, messages.ERROR, 'Please provide correct details')
            return render(request, 'product/personForm.html', {'form': data})
    context = {'form': PersonForm, 'active_form': 'active'}

    return render(request, 'Product/PersonForm.html', context)


@login_required
@user_only
def show_person_mf(request):
    person = Person.objects.all()
    person_filter = PersonFilter(request.GET, queryset=person)
    person_final = person_filter.qs
    context = {
        'key': person_final,
        'active_person': 'active', 'person_filter': person_filter
    }
    return render(request, 'product/ShowPersonForm.html', context)


@login_required
@user_only
def delete_person_form(request, person_id):
    person = Person.objects.get(id=person_id)
    person.delete()
    return redirect('/product/showpersonForm')


@login_required
@user_only
def update_person_form(request, person_id):
    person = Person.objects.get(id=person_id)
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('/product/showpersonForm')
    context = {'form': PersonForm(instance=person)}
    return render(request, 'Product/UpdatePersonForm.html', context)
# ============================================ #


@login_required
@user_only
def post_file(request):
    if request.method == "POST":
        title = request.POST.get('title')
        file = request.FILES.get('file')
        file_obj = FileUpload(title=title, file=file)
        file_obj.save()
        if file_obj:
            return redirect('/product/getFile')
        else:
            return HttpResponse("File Can not be added")
    context = {'active_file': 'active'}
    return render(request, 'Product/AddFile.html', context)


@login_required
@user_only
def get_file(request):
    files = FileUpload.objects.all()
    context = {'files': files, 'active_file': 'active'}
    return render(request, 'Product/ShowFile.html', context)


@login_required
@user_only
def delete_file(request, file_id):
    file = FileUpload.objects.get(id=file_id)
    file.delete()
    return redirect('/product/getFile')


@login_required
@user_only
def update_file(request, file_id):
    file = FileUpload.objects.get(id=file_id)
    if request.method == 'POST':
        if request.FILES.get('file'):
            file.file.delete()
            file.title = request.POST.get('title')
            file.file = request.FILES.get('file')
            file.save()
        else:
            file.title = request.POST.get('title')
            file.save()
        return redirect('/product/getFile')
    context = {'files': file, 'active_file': 'active'}
    return render(request, 'Product/UpdateFile.html', context)
# ============================================ #


@login_required
@user_only
def get_file_mf(request):
    files = FileUpload.objects.all()
    context = {'files': files, 'activate_fileMF': 'active'}
    return render(request, 'product/ShowFileMF.html', context)


@login_required
@user_only
def post_file_mf(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/product/getFileMF')
    context = {'form': FileForm}
    return render(request, 'product/AddFileMF.html', context)


@login_required
@user_only
def delete_file_mf(request, file_id):
    file = FileUpload.objects.get(id=file_id)
    os.remove(file.file.path)
    file.delete()
    return redirect("/product/getFileMF")


@login_required
@user_only
def update_file_mf(request, file_id):
    instance = FileUpload.objects.get(id=file_id)
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/product/getFileMF')
    context = {'form': FileForm(instance=instance), 'activate_fileMF': 'active'}
    return render(request, 'product/UpdateFileMF.html', context)


@login_required
@user_only
def user_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Update Successful for' + str(request.user.profile.username))
            return redirect('/product/profile')
    context = {'form': form}
    return render(request, 'Product/profile.html', context)


def show_reporter_mf(request):
    reporters = Reporter.objects.all()
    context = {
        'reporters':reporters,
        'activate_reporterMF':'active'
    }
    return render(request, 'product/getReporterMF.html', context)


def post_reporter_mf(request):
    if request.method == 'POST':
        form = ReporterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Reporter Added Successfully')
            return redirect('/product/getReporterMF')
        else:
            messages.add_message(request, messages.ERROR, 'Error in adding reporter')
            return render(request, 'product/postReporterMF.html', {'form':form})
    context = {
        'form' :ReporterForm
    }
    return render(request, 'product/postReporterMF.html',context)


def show_article_mf(request):
    articles = Article.objects.all()
    context = {
        'articles':articles,
        'activate_articleMF':'active'
    }
    return render(request, 'product/getArticleMF.html', context)


def post_article_mf(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Article Added Successfully')
            return redirect('/product/getArticleMF')
        else:
            messages.add_message(request, messages.ERROR, 'Error in adding article')
            return render(request,'product/postArticleMF.html', {'form':form})
    context = {
        'form':ArticleForm,
    }
    return render(request, 'product/postArticleMF.html',context)