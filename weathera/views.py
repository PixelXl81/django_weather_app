import requests
from django.shortcuts import render

# Create your views here.

def get_weather_data(city):
    api_key = 'your api key '  # کلید API معتبر خود را وارد کنید
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # برای دریافت دما به صورت سانتی‌گراد
    }

    try:
        response = requests.get(base_url, params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "درخواست زمان زیادی گرفت. لطفاً دوباره تلاش کنید."}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"خطای HTTP: {http_err}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"یک خطای دیگر رخ داد: {e}"}
def weather_view(request):
    weather_data = None
    error = None
    if request.method == 'POST':
        city = request.POST.get('city').strip().title()
        data = get_weather_data(city)
        if 'error' in data:
            error = data['error']
        elif data.get('main'):
            weather_data = data
        else:
            error = "شهر پیدا نشد. لطفاً دوباره تلاش کنید."
    return render(request, 'weathera/index.html', {'weather_data': weather_data, 'error': error})
