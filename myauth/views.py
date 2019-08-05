from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from category.forms import CategoryForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from books.models import Book, Category
from students.models import Student
from borrow.models import Borrow
from django.db.models import Sum
from datetime import datetime



# Create your views here.
def signin(request):
    if request.method=='GET':
        return render(request,'signin.html')
    else:
        u=request.POST.get("username")
        p=request.POST.get("password")
        user=authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            return redirect('books')
        return render(request,'signin.html',{'errmsg':'your username or password is incorrect'})

def signup(request):
    if request.method=='GET':
        context = {
            'form':UserCreationForm()
        }

        return render(request,'signup.html',context)
    else:
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request,'signup.html',{'form':form})

@login_required(login_url='login')
def category(request):
    if request.method=='GET':
        context ={
            'form':CategoryForm(),
            'cat':Category.objects.filter(user_id=request.user.id),
        }
        return render(request,'category.html',context)
    else:
        form=CategoryForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user_id=request.user.id
            data.save()
            return redirect('category')
        return render(request,'category.html',{'form':form})

def mylogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def books(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        cat = Category.objects.get(id=int(request.POST['category_id']))
        description = request.POST['description']
        available = int(request.POST['quantity'])

        book = Book(title=title, author=author, description=description, available=available)
        book.save()
        if book.categories.add(cat):
            return redirect('/books')
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, "books.html", {"books": books, "categories": categories})


def edit_book(request, id):
    book = Book.objects.filter(id=id).get()
    return JsonResponse(
        {'title': book.title, 'author': book.author, 'description': book.description, 'available': book.available})

def delete_book(request, id):
    book = Book.objects.filter(id=id).get()
    book.delete()
    return redirect('/books')

@login_required(login_url='login')
def students(request):
    if request.method == "POST":
        sid = request.POST["sid"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        department = request.POST["department"]
        section = request.POST["section"]
        year = request.POST["year"]

        student = Student(student_id=sid, firstname=firstname, lastname=lastname, department=department,
                          section=section, year=year)
        student.save()
        return redirect("students")
    students = Student.objects.all()
    return render(request, "students.html", {"students": students})

@login_required(login_url='login')
def borrow(request):
    if request.method == "POST":
        student_id = request.POST['student_id']
        student = Student.objects.get(id=student_id)
        status = "Borrowed"
        books_id = request.POST.getlist('selector')
        for book_id in books_id:
            book = Book.objects.get(id=book_id)
            b = Borrow(qty=1, status=status)
            b.save()
            b.student.add(student)
            b.book.add(book)
            return redirect("borrows")
    students = Student.objects.all()
    books = Book.objects.all()
    datas = []
    for book in books:
        left = Borrow.objects.filter(status="Borrowed", book__title=book.title).aggregate(Sum('qty'))
        if left['qty__sum'] is None:
            l = 0
        else:
            l = int(left['qty__sum'])
        datas.append(book.available - l)
    return render(request, "borrow.html", {"datas": zip(books, datas), "students": students})

@login_required(login_url='login')
def returning(request):
    if request.method == "POST":
        b_id = int(request.POST["borrow_id"])
        borrow = Borrow.objects.get(id=b_id)
        borrow.date = datetime.now()
        borrow.status = "Returned"
        borrow.save()
        return redirect("returns")
    borrows = Borrow.objects.all()
    return render(request, "return.html", {"borrows": borrows})