from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import requests
import json
import pprint


from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib import messages



# Create your views here.



def index (request):
    catalog_product = ()
    type_products = LoadTypeProducts()
    
    list_product_vip = ListAllSponsored()

    data = LoadProduct()
    paginator = Paginator(data, 24)

    page = request.GET.get('page')

    try:
        Product = paginator.page(page)
    except PageNotAnInteger:
        Product = paginator.page(1)
    except EmptyPage:
        Product = paginator.page(paginator.num_pages)


    return render(request, 'app/home.html', {
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(), 
        'listproduct': Product,
        'list_product_vip1': list_product_vip[0:6],
        'list_product_vip2': list_product_vip[6:12],
    })

def type_products(request, id_type_product):

    data = LoadProductByType(id_type_product)
    paginator = Paginator(data, 24)

    page = request.GET.get('page')

    try:
        Product = paginator.page(page)
    except PageNotAnInteger:
        Product = paginator.page(1)
    except EmptyPage:
        Product = paginator.page(paginator.num_pages)

    return render(request, 'app/list.html', {
       'typeproduct': LoadTypeProducts(),
       'brand': LoadBrand(), 
       'listproduct' : Product,
    })

def brand(request, id_brand):

    data = LoadProductByBrand(id_brand)

    paginator = Paginator(data, 24)

    page = request.GET.get('page')

    try:
        Product = paginator.page(page)
    except PageNotAnInteger:
        Product = paginator.page(1)
    except EmptyPage:
        Product = paginator.page(paginator.num_pages)

    return render(request, 'app/list.html', {
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(), 
        'listproduct' : Product,
    })

def register(request):
    if request.method == 'POST':
        email = request.POST.get('r_email')
        password = request.POST.get('r_pass')
        confirm_password = request.POST.get('r_confirm')

        if email == "" :
            messages.warning(request, message="Email is not emty!", extra_tags='alert')
            return redirect('/login')

        if password == "" or len(password) < 6:
            messages.warning(request, message="Password is not emty or min length smaller 6!", extra_tags='alert')
            return redirect('/login')

        if confirm_password == "" or len(confirm_password) < 6 :
            messages.warning(request, message="Confirm is not emty or min length smaller 6", extra_tags='alert')
            return redirect('/login')

        if confirm_password != password:
            messages.warning(request, message="The password and confirmation password do not match", extra_tags='alert')
            return redirect('/login')
        
        if Register(email, password, confirm_password):
            messages.success(request, message="Register is success!", extra_tags='alert')
            return redirect('/')
        else:
            messages.warning(request, message="Email is exists in system!", extra_tags='alert')
            return redirect('/login')


    return redirect('/')

def login(request):

    if 'token' in request.session:
        return redirect('/account')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Login(request, email, password):
            if(Check_Activated(request.session['token']) == True):
                request.session['activated'] = True
                return redirect('/')
            else:
                request.session['activated'] = False
                messages.warning(request, message="Account is not activated!", extra_tags='alert')
                return redirect('/')
        else:
            messages.warning(request, message="Check your information again!", extra_tags='alert')

    return render(request, 'app/login.html', {
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(), 
    })

def logout(request):
    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    else:
        del request.session['token']
        del request.session['activated']
    return redirect('/')

def search(request):
    if request.method == "POST": 
        request.session['r'] = request.POST.get("r")
    try:
        keyword = request.session['r']
    except:
        messages.warning(request, message='You must put keyword', extra_tags='alert')
        return redirect('/')
    data =  Search_Name(keyword)

    paginator = Paginator(data, 1)

    page = request.GET.get('page')

    try:
        Product = paginator.page(page)
    except PageNotAnInteger:
        Product = paginator.page(1)
    except EmptyPage:
        Product = paginator.page(paginator.num_pages)
    return render(request, 'app/list.html', {
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(), 
        'listproduct' : Product,
    })

def search_price(request):
    if request.method == "POST": 
        request.session['price'] = request.POST.get("price")
    try:
        x = request.session['price'].split(',',1)
        min = x[0]
        max = x[1]
    except:
        messages.warning(request, message='You must put price', extra_tags='alert')
        return redirect('/')
    data =  Search_Price(min,max)

    paginator = Paginator(data, 1)

    page = request.GET.get('page')

    try:
        Product = paginator.page(page)
    except PageNotAnInteger:
        Product = paginator.page(1)
    except EmptyPage:
        Product = paginator.page(paginator.num_pages)
    return render(request, 'app/list.html', {
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(), 
        'listproduct' : Product,
    })
    

def product_detail(request, id_product):
    data = ProductInfo(id_product)
    if data == False:
        messages.warning(request, message='Product not exists in system', extra_tags='alert')
        return redirect('/')
    

    return render(request, 'app/product-details.html', {
        'product_info': data,
        'info_merchant': GetInfoMerchant(id_product),
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(),
        'get_rating': GetRating(id_product)
    })

def account(request):
    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    token =  request.session['token']

    try:
        user_info = GetInfoUser(request.session['token'])
    except:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        name =  request.POST.get('name')
        phone = request.POST.get('phone')
        id_card = request.POST.get('id_card')
        address = request.POST.get('address')

        if email == "":
            messages.warning(request, message="Email is not emty!", extra_tags='alert')
            return redirect('/account')

        if name == "":
            messages.warning(request, message="Name is not emty!", extra_tags='alert')
            return redirect('/account')

        if phone == "":
            messages.warning(request, message="Phone is not emty", extra_tags='alert')
            return redirect('/account')

        if id_card == "":
            messages.warning(request, message="ID Card is not emty!", extra_tags='alert')
            return redirect('/account')

        if address == "":
            messages.warning(request, message="Address is not emty", extra_tags='alert')
            return redirect('/account')

        if(EditProfile(name, address, email,phone,id_card, token)):
            messages.success(request, message='Edit is sucess', extra_tags='alert')
            return redirect('/')
        else:
            messages.warning(request, message='Error!', extra_tags='alert')
            return redirect('/')

    return render(request, 'app/account.html',{
        'user_info': user_info,
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(), 
    })


def change_pass(request):
    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')

    token = request.session['token']

    if request.method == 'POST':
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')
        confirm = request.POST.get('confirm')
        result = ChangePass(new_pass, old_pass, confirm, token)
        if result == True:
            messages.success(request, message='Change Password is success!', extra_tags='alert')
            return redirect('/change_pass')
        else:
            try:
                if result['ModelState']['model.NewPassword'] :
                    message = result['ModelState']['model.NewPassword'][0]
                    messages.warning(request, message=message, extra_tags='alert')
                    return redirect('/change_pass')
                if result['ModelState']['model.ConfirmPassword']:
                    message = result['ModelState']['model.ConfirmPassword'][0]
                    messages.warning(request, message=result['ModelState']['model.ConfirmPassword'], extra_tags='alert')
                    return redirect('/change_pass')
                if result['ModelState']['model.OldPassword'] :
                    message = result['ModelState']['model.OldPassword'][0]
                    messages.warning(request, message=message, extra_tags='alert')
                    return redirect('/change_pass')
            except:
                messages.warning(request, message='Error old password!', extra_tags='alert')
                return redirect('/change_pass')
    return render(request, 'app/change_pass.html')


def bill(request):

    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    token =  request.session['token']

    list_bill = ListOrder(token)    

    paginator = Paginator(list_bill, 10)

    page = request.GET.get('page')

    try:
        bill = paginator.page(page)
    except PageNotAnInteger:
        bill = paginator.page(1)
    except EmptyPage:
        bill = paginator.page(paginator.num_pages)



    return render(request, 'app/bill.html',{
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(), 
        'list_order': bill,
    })

def bill_info(request, id_bill):

    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')

    token =  request.session['token']

    list_bill = ListOrder(token)
    
    data = []
    for item in list_bill:

        if int(item['orderID']) == int(id_bill):
            data = item
    if not data:
        messages.warning(request, message='Bill is not exists!', extra_tags='alert')
        return redirect('/')



    return render(request, 'app/bill_info.html',{
        'typeproduct': LoadTypeProducts(),
        'brand': LoadBrand(), 
        'data': data,
    })

def cart(request):

    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    else:
        if  request.session['activated'] == False:
            messages.warning(request, message='You must activated account', extra_tags='alert')
            return redirect('/')
        else:
            token = request.session['token']
    
    list_product_in_cart = ListProductInCart(token)

    total_cart = 0
    for item in list_product_in_cart:
        total_cart = total_cart + item['sumprice']
    

    return render(request, 'app/cart.html',{
        'list_product_in_cart': list_product_in_cart,
        'total_cart': total_cart,
        'taikhoan': GetInfoUser(token),
    })

def add(request, id_product, qty):
    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    else:
        if  request.session['activated'] == False:
            messages.warning(request, message='You must activated account', extra_tags='alert')
            return redirect('/')
        else:
            token = request.session['token']
    if ProductInfo(id_product) == False:
        messages.warning(request, message='Product is not exists', extra_tags='alert')
        return redirect('/')


    if AddProductInCart(token, id_product, qty):
        messages.success(request, message='Add success', extra_tags='alert')
        return redirect('/cart')
    else:
        messages.success(request, message='Error', extra_tags='alert')
        return redirect('/')

    return redirect('/cart')

def submit(request):
    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    else:
        if  request.session['activated'] == False:
            messages.warning(request, message='You must activated account', extra_tags='alert')
            return redirect('/')
        else:
            token = request.session['token']

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        total = request.POST.get('total')
        data = Order(name, address, phone, token)
        if data:
            messages.success(request, message='Order is success', extra_tags='alert')
            return render(request, 'app/message_bill.html',{
                'data': data[0],
                'total': total,
            })
        else:
            messages.warning(request, message='Error!', extra_tags='alert')
            return redirect('/cart')

    return redirect('/')

def remove(request, id_product):
    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    else:
        if  request.session['activated'] == False:
            messages.warning(request, message='You must activated account', extra_tags='alert')
            return redirect('/')
        else:
            token = request.session['token']

    if ProductInfo(id_product) == False:
        messages.warning(request, message='Product is not exists', extra_tags='alert')
        return redirect('/')
    
    if RemoveProductInCart(token, id_product):
        messages.success(request, message='Remove success', extra_tags='alert')
        return redirect('/cart')
    else:
        messages.success(request, message='Error', extra_tags='alert')
        return redirect('/')

    return redirect('/')


def rating(request, id_product):

    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/product_detail/'+id_product)
    token = request.session['token']

    if request.method == 'POST':
        rating = request.POST.get('rating')
        result = CheckRating(id_product, token)
        if result["rated"] == True:
            messages.warning(request, message='You was rated!', extra_tags='alert')
            return redirect('/product_detail/'+id_product)
        else:
            if Rating(id_product, rating, token):
                messages.success(request, message='Thank you!', extra_tags='alert')
                redirect('/product_detail/'+id_product)
            else:
                messages.warning(request, message='Error!', extra_tags='alert')
                redirect('/product_detail/'+id_product)

    return redirect('/product_detail/'+id_product)

def emailconfirm(request):
    user_id = request.GET.get('userId')
    token = request.GET.get('token')
    if ActivatedAccount(user_id, token):
        messages.success(request, message='Success! Please login again', extra_tags='alert')
        return redirect('/')

    else:
        messages.warning(request, message='Error!', extra_tags='alert')
        return redirect('/')

    return redirect('/')


def requestmerchentaccount(request):
    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    token = request.session['token']
    result = RequestMerchentAccount(token)
    print result
    if  result == True:
        messages.success(request, message='Request was send!', extra_tags='alert')
        return redirect('/')
    else:
        messages.warning(request, message=result, extra_tags='alert')
        return redirect('/')

    return redirect('/')

def confirmmerchentaccount(request):
    if 'token' not in request.session:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    token = request.session['token']

    if ConfirmMerchentAccount(token):
        messages.success(request, message='Actived success!', extra_tags='alert')
        return redirect('/')
    else:
        messages.warning(request, message='Error', extra_tags='alert')
        return redirect('/')

    return redirect('/')



# function get data ~ Model
def LoadTypeProducts():
    url = 'http://localhost:51717/api/ProductTypes'
    return requests.get(url).json()

def LoadBrand():
    url = 'http://localhost:51717/api/Brands'
    return requests.get(url).json()

def LoadProduct():
    url = 'http://localhost:51717/api/Product'
    return requests.get(url).json()

def LoadProductByType(id_type):
    url = 'http://localhost:51717/api/Products/SearchProduct'
    parameter = {'productTypeid': id_type}
    return requests.get(url, params=parameter).json()

def LoadProductByBrand(id_brand):
    url = 'http://localhost:51717/api/Products/SearchProduct'
    parameter = {'brandId': id_brand}
    return requests.get(url, params=parameter).json()

def Login(request, email, password):
    url = 'http://localhost:51717/token'
    headers = { 'contentType' : 'application/x-www-form-urlencoded'}
    data = {'username': email, 'password': password, 'grant_type': 'password'}
    check = requests.post(url, data=data, headers=headers)
    if check.status_code == requests.codes.ok:
        result = check.json()
        request.session['token'] = result['access_token']
        return True

def Check_Activated(token):
    url = 'http://localhost:51717/api/Account/AmIinole'
    headers = {'Authorization': "Bearer " +token}
    parameter = {'role': 'ActivatedUser'}
    return requests.get(url, params=parameter, headers=headers).json()

def ListAllSponsored():
    url = 'http://localhost:51717/api/SponsoredItems/LoadAllSponsoredItemsInTime'
    return requests.get(url).json()

def Search_Name( keyword):
    url = 'http://localhost:51717/api/Products/SearchProduct'
    parameter = {'name': keyword}
    return requests.get(url, params=parameter).json()

def Search_Price( min, max):
    url = 'http://localhost:51717/api/Products/SearchProduct'
    parameter = {'priceMin': min, 'priceMax': max}
    return requests.get(url, params=parameter).json()

def Register(email, password, pass_confirm):
    url = 'http://localhost:51717/api/Account/Register2'
    data = {'email': email, 'password': password, 'confirmPassword': pass_confirm }
    headers = { 'contentType' : 'application/json'}
    check = requests.post(url, data=data, headers=headers)
    return check.status_code == requests.codes.ok

def EditProfile(name, address, email, phone, cmnd, token):
    url = 'http://localhost:51717/api/UserInfos/CurrentUserInfo'
    headers = {'Authorization': "Bearer " +token}
    data =  {
        'Name': name,
        'HomeAddress': address,
        'Email' : email,
        'PhoneNumber': phone,
        'CMND': cmnd,
    }
    return requests.put(url, data=data, headers= headers).status_code == requests.codes.ok

def GetInfoUser(token):
    url = 'http://localhost:51717/api/UserInfos/CurrentUserInfo'
    headers = {'Authorization': "Bearer " +token}
    return requests.get(url, headers = headers).json()

def ChangePass(newpass, oldpass, confirm, token):
    url = 'http://localhost:51717/api/Account/ChangePassword'
    data = { 'OldPassword': oldpass, 'NewPassword': newpass, 'ConfirmPassword': confirm}
    headers = {'Authorization': "Bearer " +token}
    result = requests.post(url, headers=headers, data=data)
    if result.status_code == requests.codes.ok:
        return True
    else:
        return result.json()

def ProductInfo(id_product):
    url = 'http://localhost:51717/api/Product/' + id_product
    result = requests.get(url)
    if result.status_code == requests.codes.ok:
        return result.json()
    else:
        return False

def ListOrder(token):
    url = 'http://localhost:51717/api/Orders/LoadAllMyOrdersAndOrderItem'
    headers = {'Authorization': "Bearer " +token, 'Content-Type' : 'application/json'}
    return requests.get(url, headers=headers).json()

def ListProductInCart(token):
    url = 'http://localhost:51717/api/Cart/ViewCart'
    headers = {'Authorization': "Bearer " + token}
    x = requests.get(url, headers=headers).json()
    return x

def RemoveProductInCart(token, id_product):
    url = 'http://localhost:51717/api/Cart/RemoveFromCart'
    parmeter = {'pid': id_product }
    headers = {'Authorization': 'Bearer '+token, 'contentType': 'application/json'}
    return requests.get(url, headers=headers, params=parmeter).status_code == requests.codes.ok

def AddProductInCart(token, id_product, quanty):
    url = 'http://localhost:51717/api/Cart/AddToCart'
    parmeter = {'pid': id_product, 'q' : quanty }
    headers = {'Authorization': 'Bearer '+token, 'contentType': 'application/json'}
    return requests.get(url, headers=headers, params=parmeter).status_code == requests.codes.ok

def GetInfoMerchant(id_product):
    url = 'http://localhost:51717/api/Rating/GetAverageRating'
    parmeter = {'productid': id_product }
    return requests.get(url, params=parmeter).json()


def GetRating(id_product):
    url = 'http://localhost:51717/api/Rating/GetAverageRatingsofProduct'
    parmeter = {'pid': id_product}
    headers = {'contentType': 'application/json'}
    return requests.get(url, headers=headers, params=parmeter).json()

def Rating(id_product, rating, token):
    url = 'http://localhost:51717/api/Rating/RateaProduct'
    parmeter = {'pid': id_product, 'r': rating }
    headers = {'Authorization': 'Bearer '+token, 'contentType': 'application/json',}
    return requests.get(url, headers=headers, params=parmeter).status_code == requests.codes.ok


def CheckRating(id_product, token):
    url = 'http://localhost:51717/api/Rating/HaveIrated'
    parameter = {'pid' : id_product}
    headers = {'contentType': 'application/json', 'Authorization': 'Bearer '+token}
    result = requests.get(url, headers=headers, params=parameter)
    if result.status_code == requests.codes.ok:
        return result.json()

def EditRating(id_product, rating, token):
    url = 'http://localhost:51717/api/Rating/EditMyRating'
    parameter = {'pid' : id_product, 'nr': rating}
    headers = {'contentType': 'application/json', 'Authorization': 'Bearer '+token}
    return requests.get(url, headers=headers, params=parameter)

def DelRating(id_product, token):
    url = 'http://localhost:51717/api/Rating/DeleteMyRating'
    parameter = {'pid' : id_product}
    return requests.get(url, headers=headers, params=parameter)



def Order(name, address, phone, token):
    url = 'http://localhost:51717/api/Orders/MakeOrder'
    headers = {'Authorization': 'Bearer '+token, 'contentType': 'application/json',}
    data = {"name": name , "homeAddress": address, "phoneNumber": phone, }
    data = requests.post(url, headers=headers, data=data)
    if data.status_code == requests.codes.ok:
        return data.json()

def ActivatedAccount(userid, token):
    url = 'http://localhost:51717/api/Account/ActivateAccount'
    parmeter = {'userId': userid, 'token': token }
    return requests.get(url, params=parmeter).status_code == requests.codes.ok


def RequestMerchentAccount(token):
    url = 'http://localhost:51717/api/Account/RequestMerchantAccount'
    headers = {'Authorization': 'Bearer '+token, 'contentType': 'application/json'}
    result = requests.get(url,headers=headers)
    

    if result.status_code == requests.codes.ok:
        return True

def ConfirmMerchentAccount(token):
    url = 'http://localhost:51717/api/Account/ConfirmMerchantAccount'
    headers = {'Authorization': 'Bearer '+token, 'contentType': 'application/json'}
    return requests.get(url,headers=headers).status_code == requests.codes.ok
    