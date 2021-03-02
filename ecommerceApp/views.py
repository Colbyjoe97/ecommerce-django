from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# LOGIN PAGE
def index(request):
    return render(request, "login.html")


# LOGIN TO ACCOUNT
def login(request):
    validatorErrors = User.objects.loginValidator(request.POST)
    if len(validatorErrors) > 0:
        for key, value in validatorErrors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        matchingEmails = User.objects.filter(email=request.POST['userEmail'])
        request.session['loggedInId'] = matchingEmails[0].id
    return redirect('/home')


# REGISTRATION PAGE
def registerPage(request):
    return render(request, "register.html")


# REGISTER
def register(request):
    validatorErrors = User.objects.registrationValidator(request.POST)
    if len(validatorErrors) > 0:
        for key, value in validatorErrors.items():
            messages.error(request, value)
        return redirect("/register")
    else:
        hashedPass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(first_name = request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'],  birthday = request.POST['birthday'],admin = False, password=hashedPass)

        # Store the id of the logged in user using session
    request.session['loggedInId'] = newUser.id
    return redirect("/home")


# ADMIN REGISTRATION PAGE
def adminRegisterPage(request):
    return render(request, "adminRegister.html")


# CREATE ADMIN ACCOUNT
def createAdmin(request):
    validatorErrors = User.objects.registrationValidator(request.POST)
    if len(validatorErrors) > 0:
        for key, value in validatorErrors.items():
            messages.error(request, value)
        return redirect("/register")
    else:
        hashedPass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(first_name = request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'],  birthday = request.POST['birthday'], admin = True, password=hashedPass)

        # Store the id of the logged in user using session
    request.session['loggedInId'] = newUser.id
    return redirect("/home")



# SUCCESSFUL LOGIN / REGISTER
def success(request):
    if 'loggedInId' not in request.session:
        messages.error(request, "You must be logged in first")
        return redirect('/')
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'allProducts': Product.objects.all(),
    }
    return render(request, "home.html", context)


# PRODUCT CREATION PAGE
def createPage(request):
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
    }
    return render(request, "create.html", context)


# CREATE PRODUCT
def createProduct(request):
    validatorErrors = Product.objects.productValidator(request.POST)
    if len(validatorErrors) > 0:
        for key, value in validatorErrors.items():
            messages.error(request, value)
        return redirect("/createItem")
    else:
        newProduct = Product.objects.create(prodName=request.POST['pName'], description=request.POST['description'], image=request.POST['pImage'], price=request.POST['price'], created_by=User.objects.get(id=request.session['loggedInId']))
        # Store the id of the logged in user using session
    return redirect("/home")


# LOGOUT OF ACCOUNT
def logout(request):
    request.session.clear()
    return redirect("/")