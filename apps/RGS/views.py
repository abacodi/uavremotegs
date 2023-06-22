#CODE DEVELOPED BY ABA SARGIOUS / TFE> STUDY OF REMOTE OPERATIONS
# Import necessary modules and libraries
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative, LocationGlobal
from math import sin, cos, sqrt, atan2, radians
from pymavlink import mavutil
import dronekit_sitl
import time

def get_distance_metres(lat1, lon1, lat2, lon2):
    # approximate radius of earth in meters
    R = 6371000.0

    # convert latitude and longitude to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # calculate the difference between the latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # apply Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # calculate distance in meters
    distance = R * c

    return distance

# global variable for storing the SITL instance
global_vehicle = None

def start_sitl_vehicle():
    global global_vehicle
    connection_string = 'tcp:127.0.0.1:5760'
    
    while global_vehicle is None:
        try:
            global_vehicle = connect(connection_string, wait_ready=True)
        except Exception as e:
            print("Connection failed with error: ", e)
            print("Retrying...")
            time.sleep(1)
    return global_vehicle

# Call start_sitl() when our server starts
start_sitl_vehicle()

# Call real vehicle when our server starts
def start_real_vehicle():
    global global_vehicle

    connection_string = 'udp:192.168.1.176:14551'

    while global_vehicle is None:
        try:
            global_vehicle = connect(connection_string, wait_ready=True)
            # Get the set of all enabled checks (it's a bitmask)
            enabled_checks = global_vehicle.parameters['ARMING_CHECK']

            # To completely disable all arming checks:
            global_vehicle.parameters['ARMING_CHECK'] = 0

            # Make sure to re-enable the checks after you're done:
            global_vehicle.parameters['ARMING_CHECK'] = enabled_checks
        except Exception as e:
            print("Connection failed with error: ", e)
            print("Retrying...")
            time.sleep(1)
    return global_vehicle

# start_real_vehicle()

class HomeView(TemplateView):
    template_name = 'RGS/home_page.html'  
    template_name2 = 'RGS/manual_page.html' 
    template_name3 = 'RGS/auto_page.html'  

    @staticmethod
    def dashboard(request):
        if request.method == "POST":
            # Initialize our vehicle connection           
            vehicle = global_vehicle
            if request.POST['trigger'] == 'update_telemetry':
                data = {
                    'altitude': vehicle.location.global_relative_frame.alt,
                    'location': str(vehicle.location.global_frame),
                    'heading': vehicle.heading,
                    'velocity': vehicle.velocity,
                    'battery': str(vehicle.battery),
                    'mode': vehicle.mode.name,
                    'is_armed': vehicle.armed,
                    'config': dict(vehicle.parameters),
                }

                # Return response
                return JsonResponse(data)

        # Render the dashboard template with the data
        return render(request, HomeView.template_name)
    
    @staticmethod
    def manual_control(request):
        vehicle = global_vehicle  # Initialize our vehicle connection

        if request.method == "POST":
            if request.POST['trigger'] == 'update_data':
                # Additional data: current location
                data = {
                    'altitude': vehicle.location.global_relative_frame.alt,
                    'heading': vehicle.heading,
                    'velocity': vehicle.velocity,
                    'is_armed': vehicle.armed,
                    'location': [vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon],
                }
                return JsonResponse(data)
            
            elif request.POST['trigger'] == 'land_drone':
                vehicle.mode = VehicleMode("LAND")
                while not vehicle.mode.name=='LAND':  # wait until mode has changed
                    print("Waiting for drone to enter LAND mode")
                    time.sleep(1)
                print("Drone is landing")
                data = {
                    'altitude': vehicle.location.global_relative_frame.alt,
                }
                return JsonResponse(data)
            
            elif request.POST['trigger'] == 'take_off':
                altitude = float(request.POST['altitude']) 
                vehicle.mode = VehicleMode("GUIDED")
                vehicle.armed = True
                while not vehicle.armed:
                    print (" Waiting for arming...")
                    time.sleep(1)
                vehicle.simple_takeoff(altitude)
                while True:
                    print (f" Altitude: {vehicle.location.global_relative_frame.alt}")
                    #Break and return from function just below target altitude.
                    if vehicle.location.global_relative_frame.alt>=altitude*0.95:
                        print (f"Reached target altitude...")
                        break
                    time.sleep(1)
                data = {
                    'altitude': vehicle.location.global_relative_frame.alt,
                }
                return JsonResponse(data)

            elif request.POST['trigger'] == 'move_drone':
                direction = request.POST['direction']

                if direction == 'north':
                    # Code to move the drone north
                    vehicle.simple_goto(LocationGlobalRelative(vehicle.location.global_relative_frame.lat + 0.0001, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt))

                elif direction == 'south':
                    # Code to move the drone south
                    vehicle.simple_goto(LocationGlobalRelative(vehicle.location.global_relative_frame.lat - 0.0001, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt))

                elif direction == 'east':
                    # Code to move the drone east
                    vehicle.simple_goto(LocationGlobalRelative(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon + 0.0001, vehicle.location.global_relative_frame.alt))

                elif direction == 'west':
                    # Code to move the drone west
                    vehicle.simple_goto(LocationGlobalRelative(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon - 0.0001, vehicle.location.global_relative_frame.alt))

                elif direction == 'up':
                    # Code to move the drone up
                    vehicle.simple_goto(LocationGlobalRelative(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt + 1))

                elif direction == 'down':
                    # Code to move the drone down
                    vehicle.simple_goto(LocationGlobalRelative(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt - 1))
                
                data = {
                    'altitude': vehicle.location.global_relative_frame.alt,
                    'heading': vehicle.heading,
                    'velocity': vehicle.velocity,
                    'is_armed': vehicle.armed,
                }

                # Return response
                return JsonResponse(data)

        return render(request, HomeView.template_name2,context={'lat':vehicle.location.global_relative_frame.lat, 'lon':vehicle.location.global_relative_frame.lon, 'alt':vehicle.location.global_relative_frame.alt})
        
    @staticmethod
    def auto_flight(request):
        if request.method == "POST":
            if request.POST['trigger'] == 'update_data':
                data = {
                    'altitude': global_vehicle.location.global_relative_frame.alt,
                    'velocity': global_vehicle.velocity,
                    'is_armed': global_vehicle.armed,
                    'location': [global_vehicle.location.global_relative_frame.lat, global_vehicle.location.global_relative_frame.lon],
                }
                return JsonResponse(data)
            
            if request.POST['trigger'] == 'add_waypoint':
                lat = float(request.POST['latitude'])
                lon = float(request.POST['longitude'])
                alt = float(request.POST['altitude'])
                
                # Add waypoint to vehicle commands
                cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, lat, lon, alt)
                global_vehicle.commands.add(cmd)
                
                data = {'success': True}
                return JsonResponse(data)
            
            if request.POST['trigger'] == 'start_mission':
                # Upload mission and start
                global_vehicle.commands.upload()
                home_lat = global_vehicle.location.global_relative_frame.lat
                home_lon = global_vehicle.location.global_relative_frame.lon
                home_alt = global_vehicle.location.global_relative_frame.alt
                global_vehicle.home_location = LocationGlobal(home_lat, home_lon, home_alt)

                global_vehicle.mode = VehicleMode('GUIDED')
                while not global_vehicle.is_armable:  # wait until vehicle is armable
                    print("Waiting for vehicle to become armable")
                    time.sleep(1)
                
                global_vehicle.armed = True
                while not global_vehicle.armed:  # wait until vehicle is armed
                    print("Waiting for vehicle to arm")
                    time.sleep(1)
                
                global_vehicle.simple_takeoff(30)
                while True:
                    print (f" Altitude: {global_vehicle.location.global_relative_frame.alt}")
                    #Break and return from function just below target altitude.
                    if global_vehicle.location.global_relative_frame.alt>=30*0.95:
                        print (f"Reached target altitude...")
                        break
                    time.sleep(1)
                
                global_vehicle.mode = VehicleMode('AUTO')
                while not global_vehicle.mode.name == 'AUTO':  # wait until mode has changed
                    print("Waiting for drone to enter AUTO mode")
                    time.sleep(1)
                
                print("Drone is starting mission..")
                data = {'success': True}
                return JsonResponse(data)
            
            if request.POST['trigger'] == 'end_mission':
                # Change vehicle mode to RTL (Return to Launch)
                global_vehicle.mode = VehicleMode('RTL')
                while not global_vehicle.mode.name == 'RTL':  # wait until mode has changed
                    print("Waiting for drone to enter RTL mode")
                    time.sleep(1)
                
                # Wait until the UAV reaches home
                home_location = global_vehicle.home_location
                while True:
                    print("Drone is returning to launch point..")
                    vehicle_location = global_vehicle.location.global_relative_frame
                    distance_to_home = get_distance_metres(vehicle_location.lat, vehicle_location.lon, home_location.lat, home_location.lon)
                    if distance_to_home < 1:  # Assuming 1 meter proximity to home
                        break
                    time.sleep(1)
                
                print("UAV has reached home. Ending mission...")
                print("Mission ended")
                
                data = {'success': True}
                return JsonResponse(data)
                
        return render(request, HomeView.template_name3)

