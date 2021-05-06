from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.http import HttpResponseRedirect

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
def homePage(request):
    count = 0;
    if 'loggedInId' not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('/')
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'cartItems': Product.objects.filter(purchased_by=User.objects.get(id=request.session['loggedInId'])),
        'allProducts': Product.objects.all(),
        'orderedItems': OrderedItem.objects.filter(user=User.objects.get(id=request.session['loggedInId'])),
        'featuredProducts': Product.objects.filter(featured=True),
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
        newProduct = Product.objects.create(prodName=request.POST['pName'], description=request.POST['description'], image=request.POST['pImage'], price=request.POST['price'], category=request.POST['category'], type=request.POST['type'], created_by=User.objects.get(id=request.session['loggedInId']))
        # Store the id of the logged in user using session
    return redirect("/home")

# ADD PRODUCT TO A LIST OF FEATURED PRODUCTS
def featureProduct(request, prodId):
    product = Product.objects.get(id=prodId)
    product.featured = True
    product.save()
    return redirect('/home')


# DELETE ITEM
def deleteProduct(request, prodId):
    productToDelete = Product.objects.get(id=prodId)
    productToDelete.delete()
    return redirect('/home')

# SHOPPING CART PAGE
def cartPage(request):
    total = 0
    tax = 0
    orderTotal = 0.00
    shipping = 0
    for product in OrderedItem.objects.filter(user=User.objects.get(id=request.session['loggedInId'])):
        total += product.item.price * product.quantity
        tax += (float(product.item.price * product.quantity) * .06)

    tax = round(tax, 2)
    orderTotal = float(total) + tax
    orderTotal = round(orderTotal, 2)
    subtotal = round(orderTotal + tax, 2)
    if float(subtotal) >= 50:
        shipping = 0
    else:
        shipping = 10
    orderTotal += shipping
    if shipping == 0:
        orderTotal = subtotal
    else:
        orderTotal = round(subtotal + shipping, 2)
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'allProducts': Product.objects.all(),
        'total': total,
        'tax': tax,
        'orderTotal': orderTotal,
        'shipping': shipping,
        'subtotal': subtotal,
        'cartItems': Product.objects.filter(purchased_by=User.objects.get(id=request.session['loggedInId'])),
        'orderedItems': OrderedItem.objects.filter(user=User.objects.get(id=request.session['loggedInId']))
    }
    return render(request, "cart.html", context)


# ADD TO CART
def addToCart(request, prodId):
    # item = OrderedItem.objects.create(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
    item = OrderedItem.objects.filter(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
    if item.exists():
        item = OrderedItem.objects.get(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
        item.quantity += 1
        item.save()
    else:
        item = OrderedItem.objects.create(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# REMOVE FROM CART
def removeFromCart(request, prodId):
    item = OrderedItem.objects.get(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
    item.delete()
    return redirect('/cart')

# INCREASE QUANTITY OF ITEM IN CART BY 1
def addQuantity(request, prodId):
    item = OrderedItem.objects.filter(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
    if item.exists():
        item = OrderedItem.objects.get(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
        item.quantity += 1
        item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# REDUCE QUANTITY OF ITEM IN CART BY 1
def removeQuantity(request, prodId):
    item = OrderedItem.objects.filter(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
    if item.exists():
        item = OrderedItem.objects.get(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=prodId))
        if item.quantity <= 1:
            item.delete()
        else:
            item.quantity -= 1
            item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# VIEW A SINGLE PRODUCT
def view(request, id):
    context = {
        'product': Product.objects.get(id=id),
        'orderedItems': OrderedItem.objects.filter(user=User.objects.get(id=request.session['loggedInId'])),
        'inCart': OrderedItem.objects.filter(user=User.objects.get(id=request.session['loggedInId']), item=Product.objects.get(id=id)),
    }
    return render(request, 'view.html', context)

# LOGOUT OF ACCOUNT
def logout(request):
    request.session.clear()
    return redirect("/")