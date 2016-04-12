
import serial, os, mraa, math
import gpxpy 
import gpxpy.gpx 
import atexit

gps_Serial_Port = serial.Serial('/dev/ttyUSB0', 19200, timeout = 0.5)

print("Connected to: " + gps_Serial_Port.portstr)

# This string marks the beginning of the positioning data.
place_String = "$GPGGA"

#Radius of the earth in miles
earth_radius = 3963.0  

#Onboard LED on Edison arduino breakout
statusLight = mraa.Gpio(13)	
statusLight.dir(mraa.DIR_OUT)

#Save the gps log file on quit of this program
def exit_handler():
	fo = open("foo.xml", "wb")
	fo.write(gpxLog.to_xml());
	fo.close()

	print("Log file saved as xml")

atexit.register(exit_handler)

#Set up the GPS Datalogging script
gpxLog = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack() 
gpxLog.tracks.append(gpx_track) 

gpx_segment = gpxpy.gpx.GPXTrackSegment() 
gpx_track.segments.append(gpx_segment) 

while True:
	# We read a line from the GPS directly into a variable. We don't care what the line is, we just read it in.
	raw_Data = gps_Serial_Port.readline()
	utc_Adjust = -7 # Enter for your UTC time zone, -7 is PST

	#print raw_Data
	# We check if the line we have received is the position data by checking if it contains the placeString.
	if place_String in raw_Data:
		# Now that we know we have data, we clear the terminal window to ensure that all the data is easily read
		os.system('clear')
		
		# With the line found, we can split the line at each comma. The NMEA 0183 standard splits each data point with a comma. By separating, we can now access any piece of information.
		postion_Line = raw_Data.split(",")

		# The NMEA 0183 standard for position reads: [$GPGGA, Latitude, Latitude Heading, Longitude, Longitude Heading, Fix Quality, Number of Satellites Tracked, Horizontal dilution, Altitude, Height of Geoid] The last three pieces of data are unneeded

		# We assign the data we want into variables. They are stored as raw, unformatted data. Feel free to uncomment the below print line to see the raw data.
		raw_Time = postion_Line[1]
		raw_Latitude = postion_Line[2]
		raw_Latitude_Heading = postion_Line[3]
		raw_Longitude = postion_Line[4]
		raw_Longitude_Heading = postion_Line[5]
		raw_Fix = postion_Line[6]
		raw_Altitude = postion_Line[9]


		# In order to make this data useful, we check the fix to make sure we have valid data. Anything other that 0 means the data is ok to use
		if(raw_Fix > 0):

			airport_latitude = 37.359634 
			airport_longitude = -121.931653

			latitude = []
			longitude = []

			#Parse out the raw latitude
			latitude.append(int(raw_Latitude[0:2]))
			latitude.append(float(raw_Latitude[2:8]))
			longitude.append(int(raw_Longitude[0:3]))
			longitude.append(float(raw_Longitude[3:11]))

			#Convert the degrees/minutes/seconds to decimal degrees
			current_latitude_degrees = latitude[0]+(latitude[1]/60.0)
			current_longitude_degrees = longitude[0]+(longitude[1]/60.0)
			current_altitude = float(raw_Altitude)

			#Make sure that the lat/long coordinates are correctly signed
			if(raw_Latitude_Heading == 'S'):
				current_latitude_degrees = current_latitude_degrees*-1

			if(raw_Longitude_Heading == 'W'):
				current_longitude_degrees = current_longitude_degrees*-1				
			
			#Log current GPS position
			gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(longitude = current_longitude_degrees,
				latitude = current_latitude_degrees, elevation=current_altitude)) 

			print(raw_Data)
			print("LAT: %f LONG: %f" % (current_latitude_degrees, current_longitude_degrees))

			distance_x = (airport_latitude-current_latitude_degrees)*(math.pi/180.0)*earth_radius
			distance_y = (airport_longitude-current_longitude_degrees)*(math.pi/180.0)*earth_radius

			#print("XDIST: %f YDIST %f, %f" % (distance_x,distance_y,math.pow(distance_x,2)))

			distance = math.sqrt(math.pow(distance_x,2)+math.pow(distance_y,2))
			if(distance<5):
				statusLight.write(1)
			else:
				statusLight.write(0)

			print("Distance:%f" %distance)
		
		# In case we have a bad fix, we print out "No fix" so that anyone can tell an error has occurred
		else:
			print("No fix")



