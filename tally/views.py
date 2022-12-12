import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import logging
logging.basicConfig(level=logging.INFO) 
import random
from langdetect import detect
from decimal import Decimal


from .models import *
from .forms import *
from .helpers import veryfi, get_ip_currency


def index(request): 
    if request.method == 'POST':
        image = request.FILES.get('image')
        
        try:
            currency_symbol = get_ip_currency(request)        
            bill_header = Bill_Header.objects.create(image = image, user_id = request.user.id, currency_symbol=currency_symbol )                
        except IntegrityError as e:
            messages.add_message(request, messages.ERROR,e)
            return render(request, 'tally/index.html')      

        # Post the lines 
        # get the data from veryfi
        data = veryfi(bill_header.image.path)
        # detect the language     
        lang = detect(data["line_items"][0]["description"])  
        # reverse the line order if hebrew as veryfi sends hebrew in the wrong order      
        if lang == 'he':
            lines = reversed(data["line_items"])
        else:
            lines = data["line_items"]
        # save the line items 
        for line in lines: 
            if line["total"] != None:
                description = line["description"][:20].replace('\n',' ')
                try:                     
                    lines = Bill_Lines.objects.create(bill_id=bill_header.id,item=description,total=line["total"] ,quantity=line["quantity"])
                except:
                    messages.add_message(request, messages.ERROR,'Line not added.')
                    continue 
        # delete the image for Debuging KEEP        
        # bill_header.image.delete(save=True)
        return render(request, 'tally/bill.html', {
                        'form': BillForm(instance=bill_header),
                        'type': 'edit_header',  
                        'bill_id': bill_header.id,
                        'no_cancel': 'no_cancel'

                    })        
    else:        
        return render(request, 'tally/index.html')

def login_view(request):

    if request.method == 'POST':
        # Attempt to sign user in
        email = request.POST['email']
        password = request.POST['password']        
        user = authenticate(request, email=email, password=password)       

        # Check if the authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'tally/login.html', {
                'message': "Invalid username and/or password."
            })
    else:
        return render(request, 'tally/login.html')
     

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        form =  CreateRegisterForm(request.POST) 

        if form.is_valid(): 
            password = form.cleaned_data['password']
            confirmation_password = form.cleaned_data['password_confirmation']                     
            # Ensure password matches confirmation
            if password != confirmation_password:                
                return render(request, 'tally/register.html', {
                    'form': form,
                    'passworderror': "Passwords must match." })         
            # save the form data       
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            try:
                user.save()
            except IntegrityError as e:
                messages.add_message(request, messages.ERROR,e)                
                return render(request, 'tally/register..html', {
                'form': form,                                                         
                })     
            login(request, user)
            return HttpResponseRedirect(reverse('index'))           
        else:             
            return render(request, 'tally/register.html', {
                    'form': form,                                   
                })             
    else:       
        return render(request, 'tally/register.html', {
        'form': CreateRegisterForm(), 
        
        })

@login_required
def settings(request):
    # check if the user exists  
    try:
        userid =  User.objects.get(id=request.user.id)
    except:        
        messages.add_message(request, messages.ERROR,"User is not found.") 
        return render(request, 'tally/register.html', {
                    'form': CreateRegisterForm(edit=True), 
                    'edit': 'edit',               
                }) 

    if request.method == 'POST':
        form =  CreateRegisterForm(request.POST,edit=True,instance=userid) 
        if form.is_valid():                   
            # update form data
            try:        
                form.save() 
            except IntegrityError as e:
                messages.add_message(request, messages.ERROR,e)                               
                return render(request, 'tally/register.html', {
                'form': form,
                'edit':'edit',                                                         
                })      

            return HttpResponseRedirect(reverse('index'))           
        else:             
            return render(request, 'tally/register.html', {
                    'form': form,
                    'edit': 'edit',                                    
                })  
    # GET 
    else:
        form =  CreateRegisterForm(instance=userid, edit=True)
        return render(request, 'tally/register.html', {
                        'form': form,  
                        'edit': 'edit',                                                     
                    })  

@login_required
def password_update(request):
    # check if the user exists  
    try:
        userid =  User.objects.get(id=request.user.id)
    except:        
        messages.add_message(request, messages.ERROR,"User is not found.") 
        return render(request, 'tally/register.html', {
                    'form': CreateRegisterForm(update_password=True), 
                    'edit': 'edit',              
                }) 

    if request.method == 'POST':
        form =  CreateRegisterForm(request.POST,update_password=True,instance=userid) 
        if form.is_valid():                   
            # update form data        
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            try:
                user.save()
            except IntegrityError as e: 
                messages.add_message(request, messages.ERROR,e)                
                return render(request, 'tally/register.html', {
                'form': form,
                'edit':'edit',               
                }) 
       
            return HttpResponseRedirect(reverse('login'))           
        else:             
            return render(request, 'tally/register.html', {
                    'form': form,
                    'edit': 'edit',                                    
                })  

    # GET
    else:
        form =  CreateRegisterForm(instance=userid, update_password=True)
        return render(request, 'tally/register.html', {
                        'form': form,  
                        'edit': 'edit',                                                   
                    })                    


@login_required
def bill_header(request):   
    if request.method == 'POST':
        form =  BillForm(request.POST) 
        if form.is_valid():                   
            # update form data    
            data = form.cleaned_data    
            bill = form.save(commit=False)
            bill.user_id =  request.user.id
            bill.currency_symbol = get_ip_currency(request)

            try:
                bill.save()
                # get random color for user
                color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
                # add the user to the bill                        
                Bill_User.objects.create(name = request.user.first_name,
                                user_id = request.user.id, 
                                bill_id = bill.id,
                                tip = data['tip'],
                                color = color) 

            except IntegrityError as e:
                messages.add_message(request, messages.ERROR,e)                 
                return render(request, 'tally/bill.html', {
                    'form': form,                                                            
                }) 
            return HttpResponseRedirect(reverse('bill',args=(bill.id,)))           
        else:             
            return render(request, 'tally/bill.html', {
                    'form': form,                                                       
                }) 
            
    # GET
    else:       
        return render(request, 'tally/bill.html', {
                        'form': BillForm(),
                        'type': 'new_bill' ,                                                                
                    })


@login_required
def bill_header_update(request,bill_id):     
     # check if the bill exists  
    try:
        bill_header =  Bill_Header.objects.get(id=bill_id)
    except:        
        messages.add_message(request, messages.ERROR,"Bill is not found.") 
        return HttpResponseRedirect(reverse('bill_header'))      

    if request.method == 'POST':
        form =  BillForm(request.POST,instance=bill_header) 
        if form.is_valid():  
            # update form data        
            bill = form.save(commit=False)
            bill.id =  bill_id
            try:
                bill.save() 
                # update tip for all users if checked
                if  request.POST.get('update_tips') == 'on':
                    Bill_User.objects.filter(bill_id=bill_id).update(tip=bill.tip)
                # update the discount for all items 
                if  request.POST.get('update_discounts') == 'on':
                    Bill_Lines.objects.filter(bill_id=bill_id).update(discount=bill.discount)
                    
                # check if the logged in user exists in the bill, if not add bill user     
                if  not Bill_User.objects.filter(bill_id=bill_id, user_id=request.user.id).exists():   
                    # get random color for user
                    color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
                    # add the user to the bill                        
                    Bill_User.objects.create(name = request.user.first_name,
                                    user_id = request.user.id, 
                                    bill_id = bill_id,
                                    tip = request.POST.get('tip'),
                                    color = color)   
            except IntegrityError as e:
                messages.add_message(request, messages.ERROR,e)                 
                return render(request, 'tally/bill.html', {
                    'form': form,                                                            
                })
                                
            # show the bill 
            return HttpResponseRedirect(reverse('bill',args=(bill.id,)))      
        else:             
            return render(request, 'tally/bill.html', {
                    'form': form,     
                    'type': 'edit_header',                                                  
                }) 
    # GET
    else:             
        return render(request, 'tally/bill.html', {
                        'form': BillForm(instance=bill_header),
                        'type': 'edit_header',  
                        'bill_id': bill_header.id                                                                
                    }) 


def bill_view(request,bill_id):
    # check if the bill exists  
    try:        
        bill_header =  Bill_Header.objects.get(id=bill_id)
    except  Bill_Header.DoesNotExist:         
        messages.add_message(request, messages.ERROR,f"Bill {bill_id} is not found.")        
        return HttpResponseRedirect(reverse('index'))

    user_count = Bill_User.objects.filter(bill_id=bill_id).count()
  
    return render(request, 'tally/bill.html', {                    
                    'type': 'bill_view', 
                    'bill_header' :bill_header,
                    'bill_user_count' : user_count, 
                    'form': BillDetailForm(), 
                    'form_user': BillUserForm(initial={'tip':bill_header.tip})                                          
                })
                 
# save the line item 
def line_json(request,bill_id):    
     # check if the bill exists  
    try:
        bill_header =  Bill_Header.objects.get(id=bill_id)
    except Bill_Header.DoesNotExist:         
        return JsonResponse({"error": f"Bill {bill_id} is not found."}, status=404)

    if request.method == "POST":    
        # get the data 
        data = json.loads(request.body)
        item = data.get('item')
        total = data.get('total')
        quantity = data.get('quantity')
        discount = data.get('discount')
        
        # Post a new line
        try:
            line = Bill_Lines.objects.create(bill_id=bill_id,item=item,total=total,quantity=quantity,discount=discount) 
            return JsonResponse(line.serialize())  

        except:
            return JsonResponse({"error": "Error line not saved."}, status=404)

    # post must be via POST
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

def bill_view_json(request,bill_id):
    
     # check if the bill exists  
    try:
        bill_header =  Bill_Header.objects.get(id=bill_id)
    except Bill_Header.DoesNotExist:         
        return JsonResponse({"error": f"Bill {bill_id} is not found."}, status=404)

    if request.method == "GET":
        bill_lines = Bill_Lines.objects.filter(bill_id=bill_id).order_by('id')
        return JsonResponse([line.serialize() for line in bill_lines], safe=False)
 
    # request must be via GET
    else:
        return JsonResponse({"error": "GET request required." }, status=400)
        
# edit the line item         
def line_edit_json(request,line_id):    
    # check if the line exists     
    try:
        bill_line =  Bill_Lines.objects.get(id=line_id)
    except Bill_Lines.DoesNotExist:         
        return JsonResponse({"error": f"Line is not found."}, status=404)

    # edit an existing line 
    if request.method == "PUT": 
         # get the data 
        data = json.loads(request.body)
        item = data.get('item')
        total = data.get('total')
        quantity = data.get('quantity')
        discount = data.get('discount')

        # update the record 
        line = Bill_Lines.objects.get(id=line_id)    
        line.item = item
        line.total = total
        line.quantity = quantity
        line.discount = discount
        try:
            line.save() 
            return JsonResponse(line.serialize())                
        except:
            return JsonResponse({"error": "Error line not updated."}, status=404)
             
              

    if request.method == 'DELETE':
        data = json.loads(request.body)          
        # line_id = data.line_id
        line = Bill_Lines.objects.get(id=line_id)

        try:
            line.delete()
            return JsonResponse({"message": "Line deleted."}, status=201)
        except:
            return JsonResponse({"error": "Error line not updated."}, status=404)
         
    
    elif request.method == "GET":
        bill_line= Bill_Lines.objects.get(id=line_id)
        return JsonResponse(bill_line.serialize())

    # request must be via GET, PUT or DELETE
    else:
        return JsonResponse({
            "error": "GET, PUT or DELETE request required."}, status=400)
        

# enter bill user or get bill users
def bill_users_json(request,bill_id):
     # check if the bill exists  
    try:
        bill_header =  Bill_Header.objects.get(id=bill_id)
    except Bill_Header.DoesNotExist:         
        return JsonResponse({"error": f"Bill {bill_id} is not found."}, status=404)

    if request.method == "POST":    
        # get the data 
        data = json.loads(request.body)
        name = data.get('name')
        tip = data.get('tip')

         # get random color for user
        color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])        
        # Post a new user
        try:
            user = Bill_User.objects.create(name=name, tip=tip, color=color, bill_id=bill_id)            
            return JsonResponse(user.serialize())                    
        except:
            return JsonResponse({"error": "Error user not saved."}, status=404)
    

    if request.method == "GET":
        bill_users = Bill_User.objects.filter(bill_id=bill_id).order_by('id')        
        return JsonResponse([user.serialize() for user in bill_users], safe=False)
 
    # request must be via GET or POST
    else:
        return JsonResponse({"error": "GET or POST request required." }, status=400)
        

# edit or delete bill user
def user_edit_json(request,user_id):    
    #  check if the user exists  
    try:
        bill_user =  Bill_User.objects.get(id=user_id)
    except Bill_User.DoesNotExist:         
        return JsonResponse({"error": f"User is not found."}, status=404)

    # edit an existing user
    if request.method == "PUT": 
         # get the data 
        data = json.loads(request.body)
        name = data.get('name')
        tip = data.get('tip')

        # update the record 
        user = Bill_User.objects.get(id=user_id)    
        user.name = name
        user.tip = tip       
        try:
            user.save()            
            return JsonResponse(user.serialize())                 
        except:
            return JsonResponse({"error": "Error user not updated."}, status=404)    
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)  
        user = Bill_User.objects.get(id=user_id)
        try:
            user.delete()
            return JsonResponse({"message": "User deleted."}, status=201)
        except:
            return JsonResponse({"error": "Error user not updated."}, status=404)
         
    
    elif request.method == "GET":
        user_line= Bill_User.objects.get(id=user_id)
        return JsonResponse(user_line.serialize())

    # request must be via GET, PUT or DELETE
    else:
        return JsonResponse({ "error": "GET, PUT or DELETE request required."}, status=400)


# Add line user
def add_line_user_json(request,line_id):
    try:
        line = Bill_Lines.objects.get(id=line_id)
    except Bill_Lines.DoesNotExist:
        return JsonResponse({"error": "Line does not exist."})

    if request.method == 'POST':
        data = json.loads(request.body)      
        user_id = data.get('user_id') 
        # select a single user
        if user_id != 0:  
            bill_user = Bill_User.objects.get(id=user_id).serialize()               
            if  Bill_Lines.objects.filter(users=user_id,id=line_id).exists():                         
                line.users.remove(user_id)
                bill_user["type"] = "remove"            
                return JsonResponse([bill_user],safe = False)           
            else:  
                line.users.add(user_id)                
                bill_user["type"] = "add"        
                return JsonResponse([bill_user],safe = False)  
        # select all users
        else:            
            bill_users = Bill_User.objects.filter(bill_id = line.bill_id)
            bill_users_ser = [user.serialize() for user in bill_users]           
            if  line.users.all().count() == bill_users.count():                         
                    line.users.clear()
                    for user in bill_users_ser: 
                        user["type"] = "remove"            
                    return JsonResponse(bill_users_ser,safe = False)
            else:
                for user in bill_users:
                    line.users.add(user.id)
                for user in bill_users_ser: 
                    user["type"] = "add"            
                return JsonResponse(bill_users_ser,safe = False)
    # only post requests
    else:
        return JsonResponse({"error": "Post request required"}, status=400)         


# get the bill and user's totals 
def bill_totals(request,bill_id):    
    # get the bill header
    bill_dict = Bill_Header.objects.get(id=bill_id).serialize()    

    # bill users
    bill_user = Bill_User.objects.filter(bill_id=bill_id).order_by('name')  
    billUsers_dict = [user.serialize() for user in bill_user]    
    bill_user_count = bill_user.count() 
    bill_user_line_total = 0 
    bill_user_tip_total = 0 
    bill_user_discount_total = 0

    # get the bill user's line items 
    for user in billUsers_dict:             
        items = Bill_Lines.objects.filter(bill=bill_id,users=user["user_id"]).order_by('id')
        items =  [item.serialize() for item in items]
        total_items_cost = 0
        total_discount = 0
        # create a field for split user names 
        for item in items:                    
            names = item['line_users_names'] 
            if  item['line_users_count'] == bill_user_count:
                item['line_users_names']  = 'All'
            else:                 
                names.remove(user['name'])           
                item['line_users_names']   =', '.join(names)
            user_cost = round(item['total']/item['line_users_count'],2)
            item['user_cost'] = user_cost
            total_items_cost += user_cost
            total_discount += round(item['discount_amount']/Decimal(item['line_users_count']),2)

        # get the tip amount
        user_tip_amount = round((total_items_cost - total_discount)  * (user['tip']/100),2)         
    
        # update the user dict
        user['total_items_cost'] = total_items_cost
        user['total_items_tip'] =  user_tip_amount 
        user['line_items'] = items 
        user['discount_amount'] =  total_discount      

        # get the total costs of all users to update the bill dict 
        bill_user_line_total += total_items_cost
        bill_user_tip_total += user_tip_amount
        bill_user_discount_total += total_discount
        bill_dict['user_line_total'] = bill_user_line_total
        bill_dict['user_tip_total'] = bill_user_tip_total
        bill_dict['user_discount_total'] = bill_user_discount_total       

        if bill_user_line_total == 0:
            bill_dict['user_avg_tip'] = 0
        else:   
            bill_dict['user_avg_tip'] = round((bill_user_tip_total/(bill_user_line_total-bill_user_discount_total) ) * 100,2)
        bill_dict['users'] = billUsers_dict
                    
    # logging.info(json.dumps(bill_dict, cls=DjangoJSONEncoder,indent=4))
            
    return JsonResponse(bill_dict,safe = False)

@login_required
# show logged in user's list of bills
def my_bills(request):
    user_id = request.user.id
    bills = Bill_Header.objects.filter(user=user_id).order_by('-id')   

    return render(request, 'tally/bill.html', {                    
                    'type': 'mybills_view', 
                    'bills': bills        
                })

