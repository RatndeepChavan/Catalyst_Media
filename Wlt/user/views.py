from django.shortcuts import render, redirect
from .admin import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Status, Tran
from django.contrib import messages


# Create your views here.
def hm(request):
    if request.user.is_authenticated :
        return redirect('payment')

    if request.method == 'POST':
        e = request.POST['username']
        p = request.POST['password']
        u = authenticate(email=e, password=p)
        if u :
            login(request=request, user=u)
            return redirect('payment')
        er = 'Invalid username or password'
        return render(request, 'hm.html', {'er':er})
    return render(request, 'hm.html')

def out(request):
    logout(request)
    return redirect('hm')

def sg(request):
    if request.user.is_authenticated: return redirect('payment')

    fm = UserCreationForm()
    if request.method == 'POST':
        fm = UserCreationForm(request.POST)
        if fm.is_valid() :
            fm.save()
            e = fm.cleaned_data['email']
            wal = Status(em=e, st=False, bl=0)
            wal.save()
            messages.success(request, 'Account Created! Now log in...')
            return redirect('hm')
    return render(request, 'sg.html', {'fm':fm})

def payment(request):
    if request.user.is_authenticated:
        d = Status.objects.get(em=request.user)
        t = Tran.objects.filter(us=request.user)
        if d.st :
            return render(request, 'payment.html', {'u':request.user, 'blc' : d.bl, 't':t})

        return render(request, 'payment.html', {'u':request.user, 'dis':True, 'blc' : d.bl, 't':t})
    return redirect('hm')

def enable(request):
    d = Status.objects.get(em=request.user)
    d.st = True
    d.save()
    return redirect('payment')

def disable(request):
    if request.user.is_authenticated:
        d = Status.objects.get(em=request.user)
        d.st = False
        d.save()
        return redirect('payment')
    return redirect('hm')

def add(request):
    if request.user.is_authenticated:
        am = request.POST['amount']
        if am:
            am = int(am)
            t = Tran(us=request.user, am=am)
            t.save()
            s = Status.objects.get(em=request.user)
            s.bl += am
            s.save()
            messages.success(request, 'Credited...')
            return redirect('payment')
        return redirect('payment')
    return redirect('hm')

def remove(request):
    if request.user.is_authenticated:
        am = request.POST['amount']
        if am :
            am = int(am)
            t = Tran(us=request.user, am=-am)
            s = Status.objects.get(em=request.user)
            if am<=s.bl :
                s.bl -= am
                s.save()
                t.save()
                messages.success(request, 'Debited...')
            else : messages.error(request, 'Low balance...')
            return redirect('payment')
        return redirect('payment')
    return redirect('hm')


# API Coding
import io
from rest_framework.parsers import JSONParser
from .serializers import Stsz, Transz
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Api views
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api(request, v):
    dt = request.body
    dt = io.BytesIO(dt)
    dt = JSONParser().parse(dt)
    # print(v, dt)
    us = Status.objects.get(em=request.user)

    if v=='enb':
        sz = Stsz(instance=us, data=dt, partial=True)
        if sz.is_valid():
            sz.save()
            print(us.st, us.em, us.bl)
            rt = JSONRenderer().render('Wallet is enabled')
            return HttpResponse(rt, content_type='application/json')
        rt = JSONRenderer().render(sz.errors)
        return HttpResponse(rt, content_type='application/json')

    elif v=='dis':
        sz = Stsz(instance=us, data=dt, partial=True)
        if sz.is_valid():
            sz.save()
            print(us.st, us.em, us.bl)
            rt = JSONRenderer().render('Wallet is disable')
            return HttpResponse(rt, content_type='application/json')
        rt = JSONRenderer().render(sz.errors)
        return HttpResponse(rt, content_type='application/json')

    elif v=='bal':
        rt = JSONRenderer().render(f'Wallet balance is : {us.bl}')
        return HttpResponse(rt, content_type='application/json')

    elif v=='add':
        if (type(dt) == int or type(dt) == float ) and dt >= 0 :
            us.bl += dt
            us.save()
            t = Tran(us=request.user, am=dt)
            t.save()
            rt = JSONRenderer().render(f'wallet credited for {dt}')
            return HttpResponse(rt, content_type='application/json')

        rt = JSONRenderer().render(f'Please provide positive numeric value')
        return HttpResponse(rt, content_type='application/json')

    elif v=='rmv':
            if (type(dt) == int or type(dt) == float ) and dt >= 0 :
                if dt <= us.bl:
                    us.bl -= dt
                    us.save()
                    t = Tran(us=request.user, am=-dt)
                    t.save()
                    rt = JSONRenderer().render(f'wallet debited for {dt}')
                    return HttpResponse(rt, content_type='application/json')

                rt = JSONRenderer().render(f'Low balance...')
                return HttpResponse(rt, content_type='application/json')

            rt = JSONRenderer().render(f'Please provide positive numeric value')
            return HttpResponse(rt, content_type='application/json')

    rt = JSONRenderer().render('Something went wrong')
    return HttpResponse(rt, content_type='application/json')
