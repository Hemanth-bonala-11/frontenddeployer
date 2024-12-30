from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .utils import reverse_parse_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Project
import subprocess
from django.http import StreamingHttpResponse
from .utils import clone_repo, deploy_app
# Create your views here.


class RenderTemplateView(View):

    def get(self, request):
        try:
            url = request.META.get('HTTP_HOST')
            # print(request.get_host(), "host")
            # print("request url is ", url)
            subdomain = reverse_parse_string(url)
            print(subdomain, "subdomain")

            if not subdomain:
                return HttpResponse("hii")
            project = Project.objects.filter(subdomain=subdomain).first()

            if project:
                file_location = f"{subdomain}/build/index.html"
                print(project, "project")
                print(file_location, "file location")
                return render(request, file_location )
        except Exception as e:
            pass

class DeployView(APIView):
    permission_classes = [AllowAny]



    def post(self, request):
        try:
            data = request.data
            github_url = data.get('github_url')
            # framework = data.get('framework')
            subdomain = data.get('subdomain')

            if Project.objects.filter(subdomain=subdomain).exists():
                return Response({"subdomain": "Subdomain is already taken"}, status=status.HTTP_409_CONFLICT)
            if Project.objects.filter(github_url=github_url).exists():
                return Response({"project": "This Repo is already deployed"}, status=status.HTTP_409_CONFLICT)

            Project.objects.create(github_url=github_url, subdomain=subdomain)
            # folder_name = subdomain


            # subprocess.run(['npm', 'i'], cwd=f"templates/{subdomain}", check=True, shell=True)
            #
            # subprocess.run(['npm', 'run', 'build'], cwd=f"templates/{subdomain}", check=True, shell=True)


            response = StreamingHttpResponse(deploy_app(github_url=github_url, subdomain=subdomain),
                content_type='text/event-stream'
            )
            response["Cache-Control"] = "no-cache"
            response["Connection"] = "keep-alive"
            response["Transfer-Encoding"] = "chunked"
            return response


        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)