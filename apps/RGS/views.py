#CODE DEVELOPED BY ABA SARGIOUS / TFE> STUDY OF REMOTE OPERATIONS
# Import necessary modules and libraries
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative
from pymavlink import mavutil
import dronekit_sitl
import time

# global variable for storing the SITL instance
global_vehicle = None
global_sitl = None

def start_sitl_vehicle():
    global global_sitl
    global global_vehicle
    # If global_sitl is None, start the simulation
    if global_sitl is None:
        global_sitl = dronekit_sitl.start_default()

    connection_string = global_sitl.connection_string()
    
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

class HomeView(TemplateView):
    template_name = 'RGS/home_page.html'  
    template_name2 = 'RGS/manual_page.html' 
    template_name3 = 'RGS/auto_page.html'  

    @staticmethod
    def dashboard(request):
        if request.method == "POST":
            # Call start_sitl() when our server starts
            
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

                # Disconnect from the Vehicle
                vehicle.close()

                # Return response
                return JsonResponse(data)

        # Render the dashboard template with the data
        return render(request, HomeView.template_name)

    @staticmethod
    def manual_control(request):
        if request.method == "POST":
            vehicle = global_vehicle
            if request.POST['trigger'] == 'update_data':
                data = {
                    'altitude': vehicle.location.global_relative_frame.alt,
                    'heading': vehicle.heading,
                    'velocity': vehicle.velocity,
                    'is_armed': vehicle.armed,
                }

                # Disconnect from the Vehicle
                vehicle.close()

                # Return response
                return JsonResponse(data)
            
            if request.POST['trigger'] == 'arm_uav':
                
                print ("Basic pre-arm checks")
                # Don't try to arm until autopilot is ready
                while not vehicle.is_armable:
                    print (" Waiting for vehicle to initialise...")
                    time.sleep(1)

                print ('Arming motors')
                # Copter should arm in GUIDED mode
                vehicle.mode    = VehicleMode("GUIDED")
                vehicle.armed   = True

                # Confirm vehicle armed before attempting to take off
                while not vehicle.armed:
                    print (" Waiting for arming...")
                    time.sleep(1)
                data = {
                    'altitude': vehicle.location.global_relative_frame.alt,
                    'heading': vehicle.heading,
                    'velocity': vehicle.velocity,
                    'is_armed': vehicle.armed,
                }

                vehicle.close()
                # Return response
                return JsonResponse(data)

            if request.POST['trigger'] == 'move_drone':
                direction = request.POST['direction']

                # Set the vehicle mode to LOITER
                vehicle.mode = VehicleMode("LOITER")
                time.sleep(1) # allow time for mode to change

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

                # Disconnect from the Vehicle
                vehicle.close()

                data = {
                    'altitude': vehicle.location.global_relative_frame.alt,
                    'heading': vehicle.heading,
                    'velocity': vehicle.velocity,
                    'is_armed': vehicle.armed,
                }

                # Return response
                return JsonResponse(data)

        # Render the dashboard template with the data
        return render(request, HomeView.template_name2)
        
    @staticmethod
    def auto_flight(request):
        vehicle = global_vehicle

        cmds = vehicle.commands
        cmds.clear()

        # Define the waypoints for your mission
        waypoint1 = LocationGlobalRelative(51.5074, 0.1278, 20)
        waypoint2 = LocationGlobalRelative(51.5075, 0.1279, 20)
        waypoint3 = LocationGlobalRelative(51.5076, 0.1280, 20)

        # Add a takeoff command
        cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 20))

        # Add waypoint commands
        cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 
                        waypoint1.lat, waypoint1.lon, waypoint1.alt))
        cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 
                        waypoint2.lat, waypoint2.lon, waypoint2.alt))
        cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 
                        waypoint3.lat, waypoint3.lon, waypoint3.alt))

        # Upload mission
        cmds.upload()

        # Change vehicle mode to AUTO to start the mission
        vehicle.mode = VehicleMode('AUTO')

        return render(request, HomeView.template_name3)


