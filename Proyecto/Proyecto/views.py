from urllib import request
from django.shortcuts import render
from django.http import HttpResponse

from Proyecto.utils import diabetes_prediction_model
def index(request):
    return HttpResponse("<h1>Hola Mundo </h1")


def contenidoHtml(request):
    contenido=""""
     <html>
     <body>
     <p> Nombre:</p>
     </body>
     </html>
    """
    return HttpResponse(contenido)


from django.shortcuts import render

def prediccion2(request):
    if request.method == 'POST':
        # Recibir los datos del formulario
        diabetes = request.POST.get('diabetes')
        age_category = request.POST.get('age_category')
        bmi = float(request.POST.get('bmi'))
        smoking_history = request.POST.get('smoking_history')
        alcohol_consumption = int(request.POST.get('alcohol_consumption'))
        exercise = request.POST.get('exercise')
        general_health = request.POST.get('general_health')
        depression = request.POST.get('depression')

        # Mapear los valores de las categorías a números
        diabetes = 1 if diabetes == 'si' else 0
        smoking_history = 1 if smoking_history == 'si' else 0
        exercise = 1 if exercise == 'si' else 0
        depression = 1 if depression == 'si' else 0

        # Crear el arra y de datos para la predicción
        new_data = [
            diabetes,
            age_category,  # Asume 1 si no se encuentra la categoría
            bmi,
            smoking_history,
            alcohol_consumption,
            exercise,
            general_health,  # Asume 1 si no se encuentra la categoría
            depression
        ]

        # Llamar a la función de predicción
        resultado, probabilidad = diabetes_prediction_model(new_data)

        # Renderizar el resultado
        return render(request, 'prediccion.html', {
            'prediction': resultado,
            'probability': f'{probabilidad:.2f}%'
        })

    return render(request, 'prediccion.html')

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
  
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
   
def home(request): 
    return render(request, 'home.html')
   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile') #profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request): 
    return render(request, 'profile.html')
   
def signout(request):
    logout(request)
    return redirect('/')