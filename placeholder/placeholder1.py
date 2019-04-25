from django.http import HttpResponse
import sys
from django.conf.urls import url
from django.conf import settings
from django.core.wsgi import get_wsgi_application

import os

from django import forms 
from django.conf.urls import url
#pillow
from io import BytesIO
from PIL import Image

DEBUG = os.environ.get('DEBUG','on') == 'on'
#SECRET_KEY = os.environ.get('SECRET_KEY',os.urandom(32))
SECRET_KEY = os.environ.get('SECRET_KEY','9qu3=*m2xv-@rmp#txf=f^gr6jr4u(9=$4-rlf_2=c$6z5d^g(')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)
class ImageForm(forms.Form):
    height = forms.IntegerField(min_value=1,max_value=2000)
    width = forms.IntegerField(min_value=1,max_value=2000)

    def generate(self,image_format = 'PNG'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        image = Image.new('RGB',(width,height))
        content = BytesIO()
        image.save(content,image_format)
        content.seek(0)
        return content


def placeholder(request,width,height):
    form = ImageForm({'height':height,'width':width})
    if form.is_valid():
        image = form.generate()
        #
        return HttpResponse(image,content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Imgae Request')

def index(request):
    return HttpResponse("Hello Wold")

def placeholder(request,width,height):
    return HttpResponse('Ok')


urlpatterns = ( 
                url(r'^$',index,name='homepage'),
                url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$',placeholder,name='placeholder'),
                )
application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)