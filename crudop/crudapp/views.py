from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request,'book_list.html',{'books':books})

def book_create(request):
    if request.method=='POST':
        title = request.POST['title']
        author = request.POST['author']
        price = request.POST['price']
        Book.objects.create(title=title, author=author, price=price)
        return redirect('book_list')
    return render(request, 'book_form.html')

def book_update(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.price = request.POST['price']
        book.save()
        return redirect('book_list')
    return render(request, 'book_form.html',{'book':book})

def book_delete(request, id):
    book = get_object_or_404(Book, pk=id)
    book.delete()
    return redirect('book_list')
    

