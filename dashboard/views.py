import pandas as pd
import os

from django.conf import settings
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import (
    UploadedFile,
    Visualization
)

from .utils import generate_chart

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.forms import (
    UserCreationForm
)

from django.contrib.auth.decorators import (
    login_required
)

from .forms import UploadFileForm

from .models import (
    UploadedFile,
    Visualization
)

import pandas as pd

CHART_TYPES = [
    'bar',
    'line',
    'scatter',
    'histogram',
    'pie'
]

def register(request):

    if request.method == 'POST':

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'login'
            )

    else:

        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {
            'form': form
        }
    )


@login_required
def dashboard(request):

    files = UploadedFile.objects.filter(
        user=request.user
    )

    return render(
        request,
        'dashboard.html',
        {
            'files': files
        }
    )


@login_required
def upload_file(request):

    if request.method == "POST":

        form = UploadFileForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            uploaded_file = form.save(
                commit=False
            )

            uploaded_file.user = request.user

            uploaded_file.save()

            return redirect(
                'preview',
                uploaded_file.id
            )

    else:

        form = UploadFileForm()

    return render(
        request,
        'upload.html',
        {
            'form': form
        }
    )


@login_required
def preview_file(request, file_id):

    uploaded_file = get_object_or_404(
        UploadedFile,
        id=file_id,
        user=request.user
    )

    file_path = uploaded_file.file.path

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    preview = df.head(10).to_html(
        classes='table table-striped',
        index=False
    )

    return render(
        request,
        'preview.html',
        {
            'file': uploaded_file,
            'preview': preview,
            'columns': list(df.columns),
            'chart_types': CHART_TYPES
        }
    )



@login_required
def generate_visualization(request, file_id):
    import os

    charts_dir = os.path.join(
        settings.MEDIA_ROOT,
        'charts'
    )

    os.makedirs(
        charts_dir,
        exist_ok=True
    )

    uploaded_file = get_object_or_404(
        UploadedFile,
        id=file_id,
        user=request.user
    )

    file_path = uploaded_file.file.path

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    chart_type = request.POST.get('chart_type')
    x_column = request.POST.get('x_column')
    y_column = request.POST.get('y_column')

    image_name = f"{request.user.id}_{uploaded_file.id}_{chart_type}.png"

    image_path = os.path.join(
        settings.MEDIA_ROOT,
        'charts',
        image_name
    )

    

    generate_chart(
        df,
        chart_type,
        x_column,
        y_column,
        image_path
    )

    Visualization.objects.create(
        user=request.user,
        uploaded_file=uploaded_file,
        chart_type=chart_type,
        x_column=x_column,
        y_column=y_column,
        image=f'charts/{image_name}'
    )

    return redirect('history')



@login_required
def history(request):

    visualizations = Visualization.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'history.html',
        {
            'visualizations': visualizations
        }
    )