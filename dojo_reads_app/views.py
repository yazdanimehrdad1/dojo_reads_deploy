from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def register(request):

    errors = User.objects.validator_registration(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session["user_id"] = new_user.id
        request.session["greeting"] =  f'{new_user.first_name}  {new_user.last_name}'
        return redirect('/main')


def login(request):
    errors= User.objects.validator_login(request.POST)

    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session["user_id"] = user.id
        request.session["greeting"] = f'{user.first_name}  {user.last_name}'

        return redirect('/main')

def logout(request):
    request.session.flush()
    return redirect('/')

def face_page(request):
    return render(request, 'login.html')

def main(request):
    context={
        "books": Book.objects.all(),
        "recent_reviews": Review.objects.order_by('created_at').reverse()[:3]

    }
    return render(request, 'main.html', context)

def add_book(request):
    context={
        "authors": Author.objects.all()
    }

    return render(request, 'add_book.html',context)

def create_book(request):
    books_errors = Book.objects.basic_validator(request.POST)
    if len(books_errors)>0:
        for key,value in books_errors.items():
            messages.error(request,value)
        return redirect('/books/add')

    review_errors = Review.objects.basic_validator(request.POST)
    if len(review_errors) > 0:
        for key, values in review_errors.items():
            messages.error(request, values)
        return redirect('/books/add')

    # if request.POST['author_dropdown'] == '-1':
    #     if request.POST['author_name'] == '':
    #         messages.error(request, "Please add an author name or select an existing author.")
    #     else:    
    #         author_errors = Author.objects.basic_validator(request.POST)
    #         if len(author_errors) > 0:
    #             for k, v in author_errors.items():
    #                 messages.error(request, v)
    #     return redirect('/books/add')
    
    if request.POST['author_dropdown'] == '-1':
        author = Author.objects.create(name = request.POST['author_name'])
    else:
        author = Author.objects.get(id= request.POST['author_dropdown'])

    book = Book.objects.create(title = request.POST['title'] , author=author)
    user = User.objects.get(id=request.session['user_id'])
    review = Review.objects.create(content = request.POST['review'], rating = request.POST['rating'], book=book, user= user)

    return redirect(f'/books/{book.id}')

def show_book(request,book_id):
    book = Book.objects.get(id=book_id)
    # author = book.author
    context={
        "book": book
    }
    return render(request, 'show_book.html',context)

def user_page(request,user_id ):
    user = User.objects.get(id=user_id)
    context={
        "user":user
    } 
    return render(request, 'show_user.html', context)   



def delete_review(request, review_id):
    review_to_delete = Review.objects.get(id=review_id)
    review_to_delete.delete()
    
    
    return redirect(f'/main')





def helper(request):
    context={
        "users": User.objects.all(),
        "books": Book.objects.all(),
        "authors": Author.objects.all(),
        "reviews": Review.objects.all()
    }
    return render(request, 'helper.html',context)