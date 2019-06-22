# NMEA coordinates is degrees minutes: (d)ddmm.mmmm
# function converts it to degrees: D.d


# data = '5213.19563,02100.57196\r\n'
data = "5000.19563,02100.57196"

def nmea2deg(raw):
    def degmin(val):    # splits deg&mins in NMEA data
        valt = val.split('.')
        threshold = 3 if len(valt[0]) == 5 else 2
        return (float(val[0:threshold]), float(val[threshold:]))

    raw = raw.split(',')
    lat = degmin(raw[0])
    lon = degmin(raw[1])
    latdeg = lat[0] + lat[1]/60.0  # *(-1) for W and S
    londeg = lon[0] + lon[1]/60.0  # *(-1) for W and S
    return (latdeg, londeg)

position_deg = nmea2deg(data)
print(f"total: {position_deg}")
