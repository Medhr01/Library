from django.shortcuts import render, redirect
import os
from django.conf import settings
from .models import *
from .forms import *
from datetime import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
import barcode
import barcode.writer
from barcode.writer import ImageWriter, SVGWriter
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

# Create your views here.
@login_required
def home(request):
    clients = Client.objects.count()
    livres = Livre.objects.count()
    exemplaires = Exemplaire.objects.count()
    emprunts = Emprunt.objects.count()
    return render(request, 'index.html', {'Clients':clients, 'Livres':livres, 'Exemplaires':exemplaires, 'Emprunts':emprunts})

def user_login(request):
    msg = " "
    if request.method == "POST":
        usern = request.POST["username"]
        passw = request.POST["password"]

        user = authenticate(request, username=usern, password=passw)
        
        if user is not None:
            login(request, user)
            next_page = request.POST.get('next', 'home')
            return redirect('home') 
            
        else:
            msg = "Wrong Username or password !"
    return render(request, "login.html", {'msg':msg})


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

@login_required
def Clients(request):
    clients = Client.objects.all()
    if request.method == 'POST':
        form = ClientForm(request.POST, initial={'status':'Active'})
        
        client = form.save()
        #Génératin de CodeBar pour nouveu client
        client_id = client.id
        code128_class = barcode.get_barcode_class('code128')
        barcode_instance = code128_class(str(client_id), writer=ImageWriter())
        file_path = os.path.join(settings.STATIC_ROOT, 'IDS', f'user_{client_id}')
        barcode_instance.save(file_path, options={'module_width': 0.5, 'module_height': 20, 'quiet_zone': 1})
        
        return redirect('Clients')
           
            
    else:
        form=ClientForm(initial={'status':'Active'})
    
    return render(request, 'clients.html', {'clients': clients, 'form':form})
@login_required
def delete_client(request, id):
    
    user = Client.objects.get(pk=id)
    #delete Codebar
    file_path = os.path.join(settings.STATIC_ROOT, 'IDS', f'user_{id}.png')
    if os.path.exists(file_path):
        os.remove(file_path)
        
    user.delete()
    return redirect('Clients')
@login_required
def edit_client(request, id):
    user = Client.objects.get(pk=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=user)
        
        form.save()
        return redirect('Clients')
    else:
        form = ClientForm(instance=user)
    return render(request, 'Client.html', {'form':form, 'client':user})
@login_required
def actdes(request, id):
    user = Client.objects.get(pk=id)
    if request.GET.get("action") == "act" : 
        user.activer()
    else:
        user.desactiver()

    
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

@login_required
def Livres(request):
    livres = Livre.objects.all()
    form = livre_f(request.POST)
    
    if form.is_valid():
        form.save()

    
    return render(request, 'Livres.html', {'livres': livres,'form':form})

@login_required
def livre(request, ISBN):
    livre = Livre.objects.get(ISBN=ISBN)
    if request.method == 'POST':
        form = livre_f(request.POST, instance=livre)
        form.save()
        return redirect('Livres')
    else:
        form = livre_f(instance=livre)

    return render(request, 'Livre.html', {'livre': livre, 'form': form})
@login_required
def delete_livre(request, id):
    livre = Livre.objects.get(pk=id)
    livre.delete()

    return redirect("Livres")


@login_required
def emprunt_client(request, id):
    livres = Livre.objects.filter(pret=True).values
    client = Client.objects.get(pk=id)

    count = Emprunt.objects.filter(Client=client, Date_retourne=None).count()

    return render(request, 'rent_u.html', {'livres':livres, 'client':client, 'count':count})
@login_required
def emprunt_livre(request, id):
    clients = Client.objects.filter(statut="Active")
    livre = Livre.objects.get(pk=id)
    exemplaire = Exemplaire.objects.filter(livre=livre, statut='Disponible').last()
    
    return render(request, 'rent_liv.html', {'livre':livre, 'exemplaire':exemplaire, 'clients': clients})
@login_required
def emprunt(request, id):
    if request.POST.get("form") == "livre":
        exemplaire = Exemplaire.objects.get(id=request.POST.get("exemplaire_id"))
        client = Client.objects.get(pk=id)
        page_prec = "Livres"

    elif request.POST.get("form") == "user":
        livre = Livre.objects.get(pk=id)
        exemplaire = Exemplaire.objects.filter(livre=livre, statut='Disponible').last()
        client = Client.objects.get(id=request.POST.get("client"))
        page_prec = "Clients"
        
    date_r = datetime.now() + timedelta(weeks=2)
    
    Emprunt.objects.create(
                Exemplaire=exemplaire,
                Client=client,
                mUser=request.user,
                Date_retourn=date_r
            )
    exemplaire.emprunt_exmp()
    return redirect(page_prec)

@login_required
def emps_hist(request):
    emps = Emprunt.objects.all()

            
    return render(request, 'emprunt_hist.html', {'emps':emps})
@login_required
def return_emp(request, id):
    emp = Emprunt.objects.get(pk=id)
    act = request.GET.get("act")
    
    emp.return_exmp(act)

    return redirect('Emprunt_hist')



@login_required
def exemplaires(request):
    exmps = Exemplaire.objects.all()

    return render(request, 'Exemplaires.html', {'exemplaires': exmps})
@login_required
def pret(request, id):
    livre = Livre.objects.get(pk=id)
    pret = request.GET.get("pret") 
    
    livre.prett(pret)
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
@login_required
def modifier_exmp(request, id):
    ob = Exemplaire.objects.get(pk = id)
    if request.GET.get("act") == "renv" :
        ob.renouvler()
    else:
        ob.retirer()

    return redirect("Exemplaires")



        
