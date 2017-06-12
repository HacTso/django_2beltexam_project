from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
# from django.db.models import Count
# Create your views here.
def index(request):
	return render(request, 'django_2beltexam/index.html')
    # return render(request, 'django_2beltexam/index.html', context)

def register_process(request):
	context = {
		'username' : request.POST['username'], 
		'email' : request.POST['email'], 
		'password' : request.POST['password'], 
		'confirm_password' : request.POST['confirm_password']
		}

	user = User.objects.register(context)
	if 'error' in user:
		messages.error(request, user['error'])
		return redirect('/')

	if 'loginUser' in user:
		request.session['id'] = user['loginUser'].id
    	request.session['name'] = user['loginUser'].username
    	return redirect('/quotes')

def login_process(request):
    context = { 
        'email' : request.POST['email'], 
        'password' : request.POST['password'] 
    }
    user = User.objects.login(context)

    if 'error' in user:
        messages.error(request, user['error'])
        return redirect('/')

    if 'loginUser' in user:
        request.session['id'] = user['loginUser'].id
        request.session['name'] = user['loginUser'].username
    	return redirect('/quotes')
        

def quotes_process(request):
	if request.method == "GET":
		return redirect('/')
	# print "we are making a secret", request.POST
	# print request.session['id']
	# print request.POST['secret']
	# result = Quote.objects.validate(request.POST['message'], request.session['id'])
	
	# if 'error' in result:
	# 	messages.error(request, result['error'])
 #        return redirect('/quotes')
        
 #    if 'quotation' in result:
 #        request.session['id'] = result['quotation'].id
 #        request.session['name'] = result['quotation'].username
 #    	return redirect('/quotes')



def quotes(request):
	if checkForLogin(request):
		# allquotes = Quote.objects.all().order_by('-id')
		# allfavor = ?
		context = {
			# "quotes" : allquotes,
			"currentuser" : User.objects.get(id=request.session['id'])
		}
		print context
		return render(request, 'django_2beltexam/quotes.html', context)
	else:
		return redirect('/')


# def popular(request):
# 	if checkForLogin(request):
# 		return render(request, 'django_2beltexam/popular.html')
# 	else:
# 		return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def checkForLogin(request):
	if 'id' not in request.session:
		messages.error(request, "Please login to view the requested page", exta_tags="register_process")
		return False
	return True




















