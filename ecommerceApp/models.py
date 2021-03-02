from django.db import models
import re
import datetime
import bcrypt

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        matchingEmails = User.objects.filter(email = postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(postData['fname']) == 0:
            errors['fnameReq'] = "First Name is required"
        elif len(postData['fname']) < 3:
            errors['fnameLen'] = "First Name must be at least 3 characters"

        if len(postData['lname']) == 0:
            errors['lnameReq'] = "Last Name is required"
        elif len(postData['lname']) < 3:
            errors['lnameLen'] = "Last Name must be at least 3 characters"

        if len(postData['email']) == 0:
            errors['emailReq'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['emailPattern'] = "Email is not valid"
        elif len(matchingEmails) != 0:
            errors['emailUsed'] = "Email already in use"

        if len(postData['birthday']) == 0:
            errors['birthdayReq'] = "Birthday is required"
        elif postData['birthday'] > str(datetime.datetime.now()):
            errors['futurebirthday'] = "Birth year cannot be in the future"

        if len(postData['password']) == 0:
            errors['passReq'] = "Password is required"
        elif len(postData['password']) < 8:
            errors['passReq'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['confirmPass']:
            errors['passMatch'] = "Passwords do not match"

        return errors

    def loginValidator(self, postData):
        matchingEmails = User.objects.filter(email = postData['userEmail'])
        errors = {}

        if len(postData['userEmail']) == 0:
            errors['loginEmailReq'] = "Email is required"
        elif len(matchingEmails) == 0:
            errors['loginEmailPattern'] = "Email is not registered"
        if len(postData['pass']) == 0:
            errors['passwordReq'] = "Password required"
        elif not bcrypt.checkpw(postData['pass'].encode(), matchingEmails[0].password.encode()):
            errors['badPass'] = "Password is incorrect"
        return errors

class ProductManager(models.Manager):
    def productValidator(self, postData):
        errors = {}

        if len(postData['pName']) == 0:
            errors['pNameReq'] = "Product name is required"
        if len(postData['pImage']) == 0:
            errors['pImgReq'] = "Image URL is required"
        if len(postData['description']) == 0:
            errors['descReq'] = "Description is required"
        if len(postData['price']) == 0:
            errors['priceReq'] = "Price is required"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField()
    admin = models.BooleanField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Product(models.Model):
    prodName = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=5000)
    price = models.DecimalField(decimal_places=2, max_digits=3 )
    created_by = models.ForeignKey(User, related_name="products_created", on_delete=models.CASCADE)
    purchased_by = models.ManyToManyField(User, related_name="items_purchased")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()