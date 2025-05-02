from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from apps.models import *

# Create your views here.
def index(request, id):
    try:
        obj_user = signup.objects.get(id=id)
        return render (request, 'index.html', {'user':obj_user})
    except signup.DoesNotExist:
        return HttpResponse("User not found")


def contact(request, id):
    obj_user = signup.objects.get(id=id)
    return render (request, 'contact.html', {'user':obj_user})

def signupview(request):
    return render (request, 'signup.html')

def signupform(request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")
        gender = request.POST.get("gender")
        profile_pic = request.FILES.get("photo")
        if password != confirmPassword:
            return HttpResponse("""<script>alert("password is not match");window.location="/signup/"</script>""")
        
        objsignup = signup(
            name = name,
            email = email,
            password = confirmPassword,
            gender = gender,
            pro_pic = profile_pic,
        )
        objsignup.save()
        return HttpResponse("""<script>alert("register successfully");window.location="/loginview/"</script>""")

def loginview(request):
    return render (request, 'login.html')

def loginform(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    try:
        obj_user = signup.objects.get(email=email)
        if obj_user.password == password:
            request.session['lid'] = obj_user.id
            return HttpResponse(f"""<script>alert("login successfully");window.location="/index/{obj_user.id}/"</script>""")
        else:
            return HttpResponse("""<script>alert("please enter correct password");window.location="/loginview/"</script>""")
    except signup.DoesNotExist:
        return HttpResponse("""<script>alert("email dosn't mach");window.location="/loginview/"</script>""")
    
def messege_send(request):
    messege = request.POST.get("message")
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    
    user_id = request.session.get('lid')
    user_obj = signup.objects.get(id=user_id)
    contact_obj = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            messege=messege,
            user = user_obj,
        )
    return HttpResponse(f"""<script>alert("Messege send Successfully");window.location="/contact/{user_id}/"</script>""")
        