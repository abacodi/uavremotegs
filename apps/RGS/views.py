# Imports
import json
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.apps import apps
from django.http import JsonResponse
from django.db.models.query_utils import Q
from django.core.files.storage import FileSystemStorage
from .general import getModel
from datetime import datetime
from dronekit import connect, VehicleMode
import dronekit_sitl

# All users
class HomeView(TemplateView):
    template_name = 'RGS/home_page.html'  # The template
    template_name2 = 'RGS/manual_page.html'  # The template
    template_name3 = 'RGS/auto_page.html'  # The template

    @staticmethod
    
    def dashboard(request):
        # Connect to the Vehicle
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()
        vehicle = connect(connection_string, wait_ready=True)

        # Collect some data from the vehicle
        data = {
            'altitude': vehicle.location.global_relative_frame.alt,
            'location': str(vehicle.location.global_frame),
            'heading': vehicle.heading,
            'velocity': vehicle.velocity,
            'battery': str(vehicle.battery),
            'mode': vehicle.mode.name,
            'is_armed': vehicle.armed,
            'config': dict(vehicle.parameters),  # Convert parameters to dictionary for JSON serialization
        }

        # Disconnect from the Vehicle
        vehicle.close()
        sitl.stop()

        # Return a JSON response
        return render(request, HomeView.template_name, context=data)

    @staticmethod
    def mc_flight(request):
        return render(request, HomeView.template_name2)
    
    @staticmethod
    def auto_flight(request):
        return render(request, HomeView.template_name3)