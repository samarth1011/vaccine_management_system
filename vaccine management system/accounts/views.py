
# Create your views here.
from django.conf.urls import url
from django.db.models.query import InstanceCheckMeta
from django.shortcuts import render, redirect, render_to_response 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .tasks import sleepy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage, message

# Create your views here.
from .models import *
from .forms import *
# from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.views import View

# from .tokens import AppTokenGenerator,token_generator


@unauthenticated_user
def registerPage(request):
	user = request.user
	# parent_id = request.session.get('ref_profile')
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			print("for calid")
			if user is not None:
				# recommended_by_profile = Customer.objects.get(id = customer_id)
				user = form.save()
				user = User.objects.get(id = user.id)
				# registered_Customer = Customer.objects.get(user = registered_user)
				# registered_Customer.refered_by = recommended_by_profile.user
				# registered_Customer.save()
				username = form.cleaned_data.get('username')
				group = Group.objects.get(name='customer')
				user.groups.add(group)
				print("parent added to customer")
				create_parent = Parent(user = user,email = user.email)
				create_parent.save()
				print("parent created")
                    # customer_group.customer.add(user)
            # user.groups.add(group)


				messages.success(request, 'Account was created for ' + username)

				return redirect('login')
			else:
				redirect('register')

				# print(user)
				
				# print(user.email)

			
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)





# @unauthenticated_user
# def registerPage2(request,code):
# 	code = str(code)
# 	customer_refered = Customer.objects.get(code = code)
# 	if customer_refered.is_token_valid == False:
# 		return HttpResponse("This Link is no longer valid.. and already used")
# 	# customer_id = request.session.get('ref_profile')
	

# 	print('refcode = ',code)
# 	form = CreateUserForm()
# 	print("in register2")
# 	if request.method == 'POST':
# 		form = CreateUserForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			print(user)
# 			username = form.cleaned_data.get('username')
# 			print(user.email)
# 			group = Group.objects.get(name='customer')
# 			user.groups.add(group)
# 			customer_refered = Customer.objects.get(code = code)
# 			customer_refered.is_token_valid = False
# 			create_customer = Customer(user = user,email = user.email,refered_by = customer_refered.user.username )
# 			create_customer.save()
# 			customer_refered.referals +=1
# 			customer_refered.save()
	
# 			print("customer created")
#                     # customer_group.customer.add(user)
#             # user.groups.add(group)


# 			messages.success(request, 'Account was created for ' + username)

# 			return redirect('login')
		

	# context = {'form':form}
	# return render(request, 'accounts/register.html', context)



@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	childs = Child.objects.all()
	parents = Parent.objects.all()
	
	
	total_customers = parents.count()

	total_orders = childs.count()
	# total_shortlisted = customers.filter(is_shortlisted = True).count()
	# waiting_count = customers.filter(is_waiting = True).count()
	# delivered = orders.filter(status='Delivered').count()
	# pending = orders.filter(status='Pending').count()
	# customer = Customer.objects.get(id=pk)
	# orders = customer.order_set.all()
	# order_count = orders.count()

	context = {'orders':childs, 'customers':parents,
				'total_customers':total_customers,'total_orders':total_orders
	 }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request,pk):
	# sleepy.delay(10)
	parent = Parent.objects.get(id = pk)
	# token=token_generator.make_token(customer)
	orders = parent.child_set.all()
	print(orders)
	

	# customer = Customer.objects.get(id=pk)
	total_orders = orders.count()
	# delivered = orders.filter(status='Delivered').count()
	# pending = orders.filter(status='Pending').count()

	# print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,'customer':parent, 
	}
	return render(request, 'accounts/user.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def accountSettings(request):
# 	customer = request.user.customer
# 	form = CustomerForm(instance=customer)

# 	if request.method == 'POST':
# 		form = CustomerForm(request.POST, request.FILES,instance=customer)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')


# 	context = {'form':form}
# 	return render(request, 'accounts/account_settings.html', context)
from django.http import HttpResponseRedirect
# token_generator = accounts.tokens.AppTokenGenerator()
from accounts.views import Parent
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from .models import *
 
# class AppTokenGenerator(PasswordResetTokenGenerator):
#     # company = Company()
#     def _make_hash_value(self, customer, timestamp):
#         # company = Company()
# 		# print(timestamp)

#         return (
#             six.text_type(customer.pk) + six.text_type(timestamp) +
#             six.text_type(customer.is_shortlisted)
#         )

# token_generator = AppTokenGenerator()



# # @login_required(login_url='login')
# # @allowed_users(allowed_roles=['admin'])
# # def products(request):
# # 	products = Product.objects.all()

# # 	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer(request, pk_test):
	customer = Child.objects.get(id=pk_test)
	
	# orders = parent.child_set.all()
	# order_count = orders.count()
	vaccines = Vaccine.objects.all()
	total_vaccine = vaccines.count()
	print(total_vaccine)
	list_vaccine_pending = []
	child_age = customer.child_age_integer
	# for vaccine in vaccines:
	# 	if int(vaccine.to_be_taken_age) >= int(child_age):
	# 		list_vaccine_pending.append(vaccine)
	

	
	# vaccine_pending = Vaccine.objects.filter(to_be_taken_age =  > child_age)
	total_vaccine_pending = len(list_vaccine_pending)

	# myFilter = OrderFilter(request.GET, queryset=orders)
	# orders = myFilter.qs 

	context = {'customer':customer,'vaccines':vaccines,'total_vaccine_pending':total_vaccine_pending,'list_vaccine_pending':list_vaccine_pending,'total_vaccine':total_vaccine,
	}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
	customer = Parent.objects.get(id=pk)
	# customer = request.user
	form = ChildForm(initial={'customer':customer})
	
	# formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = ChildForm(request.POST)
		

		# formset = OrderFormSet(request.POST, instance=customer)
		if form.is_valid():
			# print("form is valid")
			order = form.save(commit=False)
			order.parent = customer
			order.save()
            
			form.save()
			messages.success(request,"Child Added Successfully",extra_tags="alert alert-success")
			return redirect('/')
		else:
			print("form not vlais")

	context = {'form':form,'customer':customer}
	return render(request, 'accounts/company_form.html', context)

# @login_required(login_url='login')
# # @allowed_users(allowed_roles=['admin'])
# def clientDetails(request,pk):
# 	print("in clien deta")
# 	domain = get_current_site(request).domain
	
# 	customer = Customer.objects.get(id=pk)
# 	active_link = 'http://'+domain+'/register/'+customer.code
# 	# cust_code = customer.code
# 	# customer_diff = Customer.objects.get(id=pk)
# 	# token=token_generator.make_token(customer_diff)
# 	print("token generated")
# 	# if token_generator.check_token(customer,token):
# 	# 	customer_diff.is_token_valid = True
# 	# else:
# 	# 	customer_diff.is_token_valid = False
# 	# print("checked")
	
# 	form = ClientForm(initial={'customer':customer})
	
# 	# formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
# 	#form = OrderForm(initial={'customer':customer})
# 	if request.method == 'POST':
# 		#print('Printing POST:', request.POST)
# 		form = ClientForm(request.POST)
		

# 		# formset = OrderFormSet(request.POST, instance=customer)
# 		if form.is_valid():
# 			# print("form is valid")
# 			client = form.save(commit=False)
# 			client.customer = customer
# 			client.save()
            
# 			form.save()
# 			messages.info(request,"Client Website Added Successfully")
# 			# return redirect('/')
# 		else:
# 			print("form not vlais")

# 		# customer = Customer.objects.get(id = pk)
# 	clients = customer.client_set.all()
# 	# customer = Customer.objects.get(id=pk)
# 	total_clients = clients.count()
# 	# delivered = orders.filter(status='Delivered').count()
# 	# pending = orders.filter(status='Pending').count()

# 	# print('ORDERS:', orders)

# 	context = {'orders':clients,'form':form, 'total_orders':total_clients,'customer':customer,'active_link':active_link,
# 	}
# 	# return render(request, 'accounts/user.html', context)



	
# 	return render(request, 'accounts/client_form.html', context)
# import pyperclip
# def copy_link(request,code):
# 	domain = get_current_site(request).domain
# 	print("in copy_link")
# 	customer = Customer.objects.get(code = code)
# 	active_link = 'http://'+domain+'/register/'+code

# 	pyperclip.copy(active_link)
# 	messages.info(request,f'Link Copied')
# 	return HttpResponseRedirect(reverse('client_details',args=[customer.id]))
		



# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def updateOrder(request, pk):
# 	order = Order.objects.get(id=pk)
# 	form = OrderForm(instance=order)
# 	print('ORDER:', order)
# 	if request.method == 'POST':

# 		form = OrderForm(request.POST, instance=order)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')

# 	context = {'form':form}
# 	return render(request, 'accounts/order_form.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def deleteOrder(request, pk):
# 	order = Order.objects.get(id=pk)
# 	if request.method == "POST":
# 		order.delete()
# 		return redirect('/')

# 	context = {'item':order}
# 	return render(request, 'accounts/delete.html', context)



# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# @shared_task
# def send_mail(request,pk):
		
# 		# messages.info(request,"Sending Mail Please wait..")
# 		# company = Customer()
		
# 		user = request.user
# 		# customer = Customer
# 		customer = Customer.objects.get(id=pk)
# 		orders = customer.order_set.all()
# 		order_count = orders.count()
# 		if order_count == 0:
# 			print("in count")
# 			messages.error(request,"No companies added by customer so cant shortlist",extra_tags="alert alert-danger")
# 			print("messa passed")
# 			return HttpResponseRedirect(reverse('home'))
# 		# customer = Customer.objects.get(id=pk)
# 		uidb64 = urlsafe_base64_encode(force_bytes(customer.pk))
# 		domain = get_current_site(request).domain
# 		link = reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(customer)})
# 		activate_url = 'http://'+domain+link
# 		# return HttpResponse('done')
# 		email_subject = "Congratulation you are shortlisted."
# 		email_body = "Please confirm your seat by clicking this link.\n" + activate_url
		
# 		email = EmailMessage(
# 			email_subject,
# 			email_body,
# 			'samarth.mailme@gmail.com',
# 			[customer.email,'samarth.mailme@gmail.com'],
		
# 		)
# 		email.send(fail_silently=False)
# 		customer.is_mail_send = True
# 		customer.is_waiting = True
# 		customer.save()
		
# 		messages.success(request,f"Email Sent successfully to {customer}".format(customer),extra_tags="alert alert-success")
# 		# return redirect('admin')
# 		return HttpResponseRedirect('/')


# # Generate_link
# def generate_link(request,pk):
# 		customer = Customer.objects.get(id=pk)
# 		# customer = Customer.objects.get(id=pk)
# 		uidb64 = urlsafe_base64_encode(force_bytes(customer.pk))
# 		domain = get_current_site(request).domain
# 		link = reverse('activate2',kwargs={'uidb64':uidb64,'token':token_generator.make_token(customer)})
# 		customer_referal_url = 'http://'+domain+link
# 		messages.info(request,f'Here is your referal link : {customer_referal_url}'.format(customer_referal_url))
# 		return HttpResponseRedirect(reverse('client_details',args=[customer.id]))

# def generate_link2(request,pk):
# 		# code = str(kwargs.get('ref_code'))
# 		customer = Customer.objects.get(id =pk)
# 		new_code = generate_ref_code()
# 		customer.code = new_code
# 		customer.save()
# 		code = str(customer.code)
# 		customer.is_token_valid = True
# 		customer.save()
# 		domain = get_current_site(request).domain
# 		active_link = 'http://'+domain+'/register/'+code
# 		print(active_link)

# 		customer = Customer.objects.get(code = code)
# 		try:

			
# 			request.session['ref_profile'] = customer.id
# 			print('id', customer.id)
# 		except:
# 			pass
# 		# print(request.session.is_valid())
# 		request.session.set_expiry(300) 
# 		print(request.session.get_expiry_age())
# 		print(request.session.get_expiry_date())
		
# 		messages.info(request,f'Link Generated')
# 		return HttpResponseRedirect(reverse('client_details',args=[customer.id]))
		





# class ActivateAccountView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user is not None and account_activation_token.check_token(user, token):
#             company = Company()
#             company.is_shortlisted = True
#             Company.save()
#             # company.save()
#             # login(request, user)
#             return HttpResponse("user shortlisted")
#         else:
#             # invalid link
#             return HttpResponse("invalid user something went wrong")

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# class VerificationView(View):
# 	def get(self,request,uidb64,token):
		
# 		try:
# 			id = force_text(urlsafe_base64_decode(uidb64))
# 			customer = Customer.objects.get(pk = id)
# 			# if token_generator.check_token(customer,token):

			
# 			if not token_generator.check_token(customer,token):
# 				print("token_not ge")
# 				return redirect('home')
# 			# if customer.referals:
# 			# 	return redirect('home')
# 			# customer.referals += 1
# 			# customer.is_waiting = False
# 			# customer.save()
# 			# context = {'recomonding_customer_id':recomonding_customer_id}
# 			# return render(request, 'accounts/register.html', context)
# 			print("token_generated")

# 			return redirect('register2',id)

# 		except Exception as ex:
# 			print("some exp")
# 			pass
# 		return redirect('home')
