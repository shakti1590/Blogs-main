from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from General.models import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


def Home(request):
    recent_post = Post.objects.filter(approved = 'Yes')[:3]
    featured_post = Post.objects.filter(approved = 'Yes', featured='Yes')[:4]
    data={
        'recent_post': recent_post,
        'featured_post': featured_post,
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        subject_user = 'ThankYou for subscribing our newsletter'
        from_email = 'RUBlog <mjprublog@gmail.com>'
        user_email = email
        text_content = '<b>This is an important message.</b>'
        html_content = '<strong>' 'Hey,' '</strong>' '<p>Thank you for subscribing our newsletter. Blogify will always provide you updates about recent publishing of blogs, poems and stories on trending topics.</p>' '<p><br><strong>Regards,</strong><br>Team Blogify<br>CSIT Department<br>MJPRU, Bareilly</p>'
        msguser = EmailMultiAlternatives(subject_user, text_content, from_email, [user_email])
        msguser.attach_alternative(html_content, "text/html")
        msguser.send()
        news = Newsletter(email=email)
        news.save()
    return render(request, "index.html", data)

def ContactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone =  request.POST.get('phone')
        message = request.POST.get('message')
        subject_user = 'ThankYou for contacting us!'
        from_email = 'RUBlog <mjprublog@gmail.com>'
        user_email = email
        text_content = '<b>This is an important message.</b>'
        html_content = '<strong>' 'Dear ' + name + ',' '</strong>' '<p>We appreciate you contacting us about Blogify needs. We are assessing your details. One of our Blogify team members will be getting back to you shortly.</p>' '<p>While we do our best to answer your queries quickly, it may take about 10 hours to receive a response from us during peak hours.Thanks in advance for your patience.</p>' '<p><br><strong>Regards,</strong><br>Team Blogify<br>CSIT Department<br>MJPRU, Bareilly</p>'
        msguser = EmailMultiAlternatives(subject_user, text_content, from_email, [user_email])
        msguser.attach_alternative(html_content, "text/html")
        msguser.send()
        subject_admin = 'Contact Us - Blogify'
        admin_email = 'RUBlog <mjprublog@gmail.com>'
        html_content1 = '<strong>Name: </strong>' + name + '<br><strong>Phone: </strong>' + phone + '<br><strong>Email: </strong>' + email + '<br><strong>Messesge : </strong>'+ str(message)
        msgadmin = EmailMultiAlternatives(subject_admin, text_content, from_email, [admin_email])
        msgadmin.attach_alternative(html_content1, "text/html")
        msgadmin.send()
        con = Contact(name=name, email=email, phone=phone, message=message)
        con.save()
    return render(request, "contact-us.html")

def RequestYourTopic(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone =  request.POST.get('phone')
        category = request.POST.get('category')
        topic = request.POST.get('topic')
        subject_user = 'Regarding your topic request!'
        from_email = 'RUBlog <mjprublog@gmail.com>'
        user_email = email
        text_content = '<b>This is an important message.</b>'
        html_content = '<strong>' 'Dear ' + name + ',' '</strong>' '<p>Thank you for your request to ' '<strong>' + category + '</strong>' ' on topic - ' '<strong>"' + topic + '"</strong>' '. Our writers will try to write on it as soon as possible.</p>' '<p><br><strong>Regards,</strong><br>Team Blogify<br>CSIT Department<br>MJPRU, Bareilly</p>'
        msguser = EmailMultiAlternatives(subject_user, text_content, from_email, [user_email])
        msguser.attach_alternative(html_content, "text/html")
        msguser.send()
        subject_admin = 'New Topic Request - Blogify'
        admin_email = 'RUBlog <mjprublog@gmail.com>'
        html_content1 = '<strong>Name: </strong>' + name + '<br><strong>Phone: </strong>' + phone + '<br><strong>Email: </strong>' + email + '<br><strong>Category: </strong>' + category +'<br><strong>Topic : </strong>'+ str(topic)
        msgadmin = EmailMultiAlternatives(subject_admin, text_content, from_email, [admin_email])
        msgadmin.attach_alternative(html_content1, "text/html")
        msgadmin.send()
        req = Request(name=name, email=email, phone=phone, category=category, topic=topic)
        req.save()
    req = Request.objects.filter(approved = 'Yes')
    data={
        'req': req
    }
    return render(request, "request-your-topic.html", data)    

def SignIn(request):
    if request.method=="POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login (request,user)
            fname = user.first_name
            return redirect('/' , {'fname':fname})
        if user is None:
            messages.error(request, "Bad Credentials")
            return render(request,'index.html')            
    return render(request, "sign-in.html")

def SignUp(request):
    if request.method=="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username).first():
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('/signup/')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric! Special characters (!,@,#,$,&) and spaces are not allowed.")
            return redirect('/signup/')

        if len(username)>10:
            messages.error(request, "Username must be under 10 characters.")
            return redirect('/signup/')

        if not fname.isalpha():
            messages.error(request, "First Name must be Alphabet! Only contains (a-z, A-Z) & spaces are not allowed.")
            return redirect('/signup/')

        if not lname.isalpha():
            messages.error(request, "Last Name must be Alphabet! Only contains (a-z, A-Z) & spaces are not allowed.")
            return redirect('/signup/')

        if email[(len(email)-12) : (len(email)+1)] != "@mjpru.ac.in":
            messages.error(request, "Please enter your university email id to register. (eg. ankit@mjpru.ac.in)")
            return redirect('/signup/')                                  

        if User.objects.filter(email = email).first():
            messages.error(request, "Email already registered!")
            return redirect('/signup/')                     

        if (pass1 != pass2):
            messages.error(request, "Password didn't match!")
            return redirect('/signup/')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been created successfully.")
        return redirect('/signin/')
    return render(request, "signup.html")

def SignOut(request):
    logout(request)
    return redirect('/')      

def Blogs(request):
    post = Post.objects.filter(category = 'Blogs', approved = 'Yes')
    if request.method == "GET":
        st = request.GET.get('search')
        if st != None:
            post = Post.objects.filter(title__icontains=st, category = 'Blogs', approved = 'Yes')
    data={
        'post': post,
    }
    return render(request, "blogs.html", data)

def Poems(request):
    post = Post.objects.filter(category = 'Poems', approved = 'Yes')
    if request.method == "GET":
        st = request.GET.get('search')
        if st != None:
            post = Post.objects.filter(title__icontains=st, category = 'Poems', approved = 'Yes')
    data={
        'post': post,
    }
    return render(request, "poems.html", data)    

def Stories(request):
    post = Post.objects.filter(category = 'Stories', approved = 'Yes')
    if request.method == "GET":
        st = request.GET.get('search')
        if st != None:
            post = Post.objects.filter(title__icontains=st, category = 'Stories', approved = 'Yes')
    data={
        'post': post,
    }
    return render(request, "stories.html", data)

def BlogsDetailsPage(request, auto_slug):
    post = Post.objects.get(auto_slug = auto_slug)
    data={
        'post': post,
    }
    return render(request, "post-details-page.html", data)

def PoemsDetailsPage(request, auto_slug):
    post = Post.objects.get(auto_slug = auto_slug)
    data={
        'post': post,
    }
    return render(request, "post-details-page.html", data) 

def StoriesDetailsPage(request, auto_slug):
    post = Post.objects.get(auto_slug = auto_slug)
    data={
        'post': post,
    }
    return render(request, "post-details-page.html", data) 

def StartPosting(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        date = request.POST.get('date')
        featured_image = request.FILES['image']
        user = request.POST.get('user')
        body = request.POST.get('body')
        post = Post(title=title, category=category, date=date, featured_image=featured_image, user=user, body=body)
        post.save()
    return render(request, "start-posting.html")