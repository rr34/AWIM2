import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, ICRS, get_sun, get_moon, get_body, solar_system_ephemeris
import formatters

def get_AzArts(earth_latlng, moments, celestial_object):

    astropy_moments = Time(moments)
    img_astropy_location = EarthLocation(lat=earth_latlng[0]*u.deg, lon=earth_latlng[1]*u.deg)
    img_astropy_AltAzframe = AltAz(obstime=astropy_moments, location=img_astropy_location)
    if celestial_object == 'sun':
        object_SkyCoords = get_sun(astropy_moments)
    elif celestial_object == 'moon':
        object_SkyCoords = get_moon(astropy_moments)
    elif celestial_object in ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']:
        object_SkyCoords = get_body(celestial_object, astropy_moments)
    
    object_AltAz = object_SkyCoords.transform_to(img_astropy_AltAzframe)

    azimuths = [x.az.degree for x in object_AltAz]
    artifaes = [x.alt.degree for x in object_AltAz]

    # known_azart = [object_AltAz.az.degree, object_AltAz.alt.degree]

    return azimuths, artifaes


def AzArts_to_RADecs(AWIMtag_dictionary, azarts):
    input_shape = azarts.shape
    azarts = azarts.reshape(-1,2)
    capture_moment = formatters.format_datetimes(AWIMtag_dictionary['CaptureMoment'], 'from AWIM string')
    earth_latlng = AWIMtag_dictionary['Location']

    astropy_moment = Time(capture_moment)
    img_astropy_location = EarthLocation(lat=earth_latlng[0]*u.deg, lon=earth_latlng[1]*u.deg)
    astropy_AltAzsframe = AltAz(obstime=astropy_moment, location=img_astropy_location, az=azarts[:,0]*u.deg, alt=azarts[:,1]*u.deg)
    astropy_SkyCoord = SkyCoord(astropy_AltAzsframe)

    RADecs = np.ndarray(azarts.shape)

    RADecs[:,0] = astropy_SkyCoord.icrs.ra.hourangle
    RADecs[:,1] = astropy_SkyCoord.icrs.dec.degree

    RADecs = RADecs.reshape(input_shape)

    return RADecs


def day_night_twilight(sun_arts):
    lights = []
    movement = sun_arts[1] - sun_arts[0]
    for i in range(0, len(sun_arts)):
        if sun_arts[i] >= -0.833:
            lights.append('day')
        elif sun_arts[i] < -18:
            lights.append('night')
        elif movement < 0 and -0.833 > sun_arts[i] >= -6:
            lights.append('ECT')
        elif movement < 0 and -6 > sun_arts[i] >= -12:
            lights.append('ENT')
        elif movement < 0 and -12 > sun_arts[i] >= -18:
            lights.append('EAT')
        elif movement > 0 and -0.833 > sun_arts[i] >= -6:
            lights.append('MCT')
        elif movement > 0 and -6 > sun_arts[i] >= -12:
            lights.append('MNT')
        elif movement > 0 and -12 > sun_arts[i] >= -18:
            lights.append('MAT')
        if i > 0:
            movement = sun_arts[i] - sun_arts[i-1]

    return lights