###########################################################
#  Computer Project #5
#
#  Print the welcome statements 
#    define functions
#       1. open file
#       2. make float using parameters
#       3. density
#       4. temp in range
#       5. temp in range
#    define main
#       open file --> skip the first line 
#       define all the variables in the main not at the begining 
#       convert distance to PARSEC Light Year (by multiplication)
#       lines can directly be converted to make_float() 
#       call the functions to calculate habitibilty and clasify them as rocky 
#       or gaseous 
#       use string.txt for formating (be careful it is ENTER NOT INPUT for openfile)
#       the parameters for rocky and gaseous should be smalled than max_distance
#       close file
#       print the last 6 statements (put conditions for rocky and gaseous)
###########################################################
import math

#Constants
PI = math.pi   
EARTH_MASS =  5.972E+24    # kg
EARTH_RADIUS = 6.371E+6    # meters
SOLAR_RADIUS = 6.975E+8    # radius of star in meters
AU = 1.496E+11             # distance earth to sun in meters
PARSEC_LY = 3.262

def open_file():
    ''' 
    open the promted file.
    value: No argument.
    return: file_pointer.
    '''
    file_pointer= input("Input data to open: ")
    while True:
        try:
            file_pointer= open(file_pointer + ".csv", 'r')
            return file_pointer
        except FileNotFoundError:
            print('\nError: file not found.  Please try again.')
            file_pointer= input('Enter a file name: ')

def make_float(s):
    ''' 
    coverts a string to float, if there is a ValueError returns -1.
    value: the str to be processed (flt).
    return: float or -1.
    '''
    try:
        make_float= float(s)
        return make_float
    except ValueError: 
        return -1

def get_density(mass, radius): 
    ''' 
    calculating the density using mass, radius and volume. (Multiply radius and mass with constants).
    value: the str that is converted to flt then used to calculate the volume which is used to calculate the density.
    return: float or -1.
    '''
    if mass>0 and radius>0:
        volume= (4/3)*PI*((radius*EARTH_RADIUS)**3)
        density= (mass*EARTH_MASS)/volume
        return density
    else:
        return -1

def temp_in_range(axis, star_temp, star_radius, albedo, low_bound, upp_bound):
    ''' 
    this function is used to check for habitability, if true can be used in main to check whether it is a gaseous or rocky planet.
    value: the star temp, star radius and axis values are used to check the temperature, if temp is within the upp and low bounds it is true else false. 
    return: bool.
    '''
    if axis<0 or star_temp<0 or star_radius<0 or albedo<0: 
        return False
    star_radius*=SOLAR_RADIUS
    axis*=AU
    planet_temp= (star_temp)*((star_radius/(2*axis))**0.5)*((1-albedo)**0.25)
    if planet_temp >= low_bound and planet_temp <= upp_bound:
        return True 
    else:
        return False

def get_dist_range():
    '''
    converts the distance (str) to distance(flt) in light years
    value: need to multiply distance (flt) with PARSEC_LY (in the main)
    return: float. 
    '''
    while True:
        try:
            distance = float(input('''\nEnter maximum distance from Earth ''' \
                                  '''(light years): '''))
            if distance > 0:
                return distance
            elif distance <= 0:
                print("\nError: Distance needs to be greater than 0.")
        except ValueError:
            print("\nError: Distance needs to be a float.")

def main():       
    print('''Welcome to program that finds nearby exoplanets '''\
          '''in circumstellar habitable zone.''')
    file_pointer = open_file() #open file
    file_pointer.readline() #skip first line
    distance = get_dist_range() #set a variable for distance range function
    max_distance = distance 
    #define all the varibales in the main to avoid unboundlocalerror
    low_bound= 200
    upp_bound= 350
    albedo= 0.5
    total_planet_mass = 0
    planet_count =0
    closest_rocky = max_distance
    closest_gaseous = max_distance
    habitable_planet_count= 0
    max_star= -1
    max_planet= -1
    rocky_planet = 0

    #main code starts here when we take values and names from the lines in the file specification
    for line in file_pointer:
        distance_flt = make_float(line[114:])
        if distance_flt*PARSEC_LY<=0 or distance_flt* PARSEC_LY>=max_distance: 
            continue
        #convert the lines to make_float() or int based on their specifications
        axis_flt = make_float(line[66:77])
        planet_radius_flt = make_float(line[78:85])
        planet_mass_flt = make_float(line[86:96])
        star_temperature_flt = make_float(line[97:105])
        star_radius_flt_flt = make_float(line[106:113])
        number_of_stars_int = int(line[50:57])
        number_of_planets_int = int(line[58:65])
        planet_name= line[:25] #stays as a str becasue it is a name
        #finding the maximum number of stars by making the maax_star= -1
        if number_of_stars_int > max_star:
            max_star = number_of_stars_int
        #finding the maximum number of planets by making the maax_planet= -1
        if number_of_planets_int > max_planet:
            max_planet = number_of_planets_int
        
        if planet_mass_flt > 0:
            total_planet_mass += planet_mass_flt #total planet mass calculation
            planet_count += 1 #planet number count 
            
        #assigning density and temp function a variable 
        density = get_density(planet_mass_flt, planet_radius_flt)
        temp= temp_in_range(axis_flt, star_temperature_flt,\
                            star_radius_flt_flt, albedo, low_bound, upp_bound)

        #based on the parameters, clasifying if the planet is rocy or gaseous
        if temp:
            habitable_planet_count += 1 #keeping a habitable planet count if temp is True
            if (0<planet_mass_flt<10) or (0<planet_radius_flt<1.5) or\
                density>2000:
                if distance_flt <= closest_rocky:
                    closest_rocky= distance_flt
                    rocky_planet= planet_name.strip()    
            else:
                if distance_flt <= closest_gaseous:
                    closest_gaseous= distance_flt
                    gaseous_planet= planet_name.strip()        
    file_pointer.close()  #close file 

    average=  total_planet_mass/planet_count
    print(("\nNumber of stars in systems with the most stars: {:d}.")\
          .format(max_star))
    print(("Number of planets in systems with the most planets: {:d}.")\
          .format(max_planet))
    print(("Average mass of the planets: {:.2f} Earth masses.")\
          .format(average))
    print(("Number of planets in circumstellar habitable zone: {:d}.")\
          .format(habitable_planet_count))
    
    #if the rocky planet is habitable it goes in if (based on the condition) otherwise goes to else
    if closest_rocky<max_distance: 
        print(('''Closest rocky planet in the circumstellar habitable zone {} '''\
               '''is {:.2f} light years away.''').format(rocky_planet,\
                   closest_rocky*PARSEC_LY))
    else:
        print("No rocky planet in circumstellar habitable zone.")
    
    #if the rocky planet is habitable it goes in if (based on the condition) otherwise goes to else
    if closest_gaseous<max_distance:
        print(('''Closest gaseous planet in the circumstellar habitable zone {} '''\
               '''is {:.2f} light years away.''').format(gaseous_planet,\
                   closest_gaseous*PARSEC_LY))
    else: 
        print("No rocky planet in circumstellar habitable zone.")

if __name__ == "__main__":
    main()