from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from apps.models import *

# Create your views here.
def index(request):
    try:
        obj_user = signup.objects.get(login_id=request.session['lid'])
        return render (request, 'index.html', {'user':obj_user})
    except signup.DoesNotExist:
        return HttpResponse("User not found")


def contact(request):
    obj_user = signup.objects.get(login_id = request.session['lid'])
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
        
        login = Login(
            email = email,
            password = confirmPassword,
            type = 'Customer'
        )
        login.save()
        
        objsignup = signup(
            name = name,
            email = email,
            password = confirmPassword,
            gender = gender,
            pro_pic = profile_pic,
            login_id = login.id
        )
        objsignup.save()

        return HttpResponse("""<script>alert("register successfully");window.location="/loginview/"</script>""")

def loginview(request):
    return render (request, 'login.html')

def loginform(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    try:
        obj_user = Login.objects.get(email=email)
        if obj_user.password == password:
            request.session['lid'] = obj_user.id
            if obj_user.type == 'Customer':
                return HttpResponse(f"""<script>alert("login successfully");window.location="/index/"</script>""") 
            else:
                return HttpResponse(f"""<script>alert("login successfully");window.location="/add_product_view/"</script>""")
        else:
            return HttpResponse("""<script>alert("please enter correct password");window.location="/loginview/"</script>""")
    except signup.DoesNotExist:
        return HttpResponse("""<script>alert("email dosn't mach");window.location="/loginview/"</script>""")
    
def messege_send(request):
    messege = request.POST.get("message")
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    
    user_obj = signup.objects.get(login_id=request.session['lid'])
    contact_obj = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            messege=messege,
            user = user_obj,
        )
    return HttpResponse(f"""<script>alert("Messege send Successfully");window.location="/contact/"</script>""")


def seller_regv(request):
    return render (request, 'seller_reg.html')

def seller_reg(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    gender = request.POST.get("gender")
    state = request.POST.get("state")
    address = request.POST.get("address")
    pincode = request.POST.get("pincode")
    password = request.POST.get("confirmPassword")
    pro_pic = request.FILES.get("photo")
    licence = request.FILES.get("licence")
    id_proof = request.FILES.get("id_proof")
    if password != password:
        return HttpResponse("""<script>alert("Password is not match");window.location="/seller_regv/"</script>""")
    login = Login(
        password = password,
        email = email,
        type = 'Seller'
    )
    login.save()
    sellersignup = SellerSignup(
            name = name,
           email = email,
          gender = gender,
           state = state,
         address = address,
         pincode = pincode,
        password = password,
         pro_pic = pro_pic,
        b_licenc = licence,
         id_prof = id_proof,
        login_id = login.id,
    )
    sellersignup.save()
    return HttpResponse("""<script>alert("Seller Signup Successfull");window.location="/loginview/"</script>""")


def add_product_view(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'add_product.html', {'cat':subcategories})

def add_product(request):
    pro_name = request.POST.get("name")
    pro_price = request.POST.get("price")
    pro_description = request.POST.get("description")
    pro_image = request.FILES.get("image")
    
    subcategory_id = request.POST.get("subcategory") 
    var_product = Product(
        name = pro_name,
        description = pro_description,
        price = pro_price,
        image = pro_image,
        subcategory_id=subcategory_id,
    )
    var_product.save()
    return HttpResponse("""<script>alert("product added");window.location="/add_product_view/"</script>""")