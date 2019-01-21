# coding:utf-8

import binascii
import struct
import time

Header_A = "b5"  # UBX protocol header
Header_B = "62"  # UBX protocol header
NAV_ID = "01"    # UBX-NAV-PVT(0x01 0x07)
PVT_ID = "07"
NAV_PVT_Length = 96 # NAV-PVT data length

ubx_data = open("navpvt.ubx", "rb").read() # open u-center's .ubx output file
ubx_bytearray = bytearray(ubx_data)   # transform .ubx binary file to ASCII data
i = 0
NAV_PVT_Data = []

while True:
    if i > len(ubx_bytearray):
        break

    #print binascii.b2a_hex(ubx_bytearray[i:i+4])
    if binascii.b2a_hex(ubx_bytearray[i:i+1]) == Header_A:
        if binascii.b2a_hex(ubx_bytearray[i+1:i+2]) == Header_B:
            if binascii.b2a_hex(ubx_bytearray[i+2:i+3]) == NAV_ID:
                if binascii.b2a_hex(ubx_bytearray[i+3:i+4]) == PVT_ID: 
                    NAV_PVT_Data = ubx_bytearray[i+4:i+100]

    if NAV_PVT_Data.__len__() == 96:
        # time
        year = int(struct.unpack('h', struct.pack('BB', NAV_PVT_Data[6], NAV_PVT_Data[7]))[0])
        month = int(struct.unpack('B', struct.pack('B', NAV_PVT_Data[8]))[0])
        day = int(struct.unpack('B', struct.pack('B', NAV_PVT_Data[9]))[0])
        hour = int(struct.unpack('B', struct.pack('B', NAV_PVT_Data[10]))[0])
        minute = int(struct.unpack('B', struct.pack('B', NAV_PVT_Data[11]))[0])
        second = int(struct.unpack('B', struct.pack('B', NAV_PVT_Data[12]))[0])
        time_data = str(year) + "," + str(month) + "," + str(day) + "," + str(hour) + "," + str(minute) + "," + str(second)

        # fix flag
        fix_flag = int(struct.unpack('B', struct.pack('B', NAV_PVT_Data[23]))[0])
        fix_flag = bin(fix_flag)[2:].zfill(8)
        if fix_flag[0:2] == "10":
            fix_status = "fixed"
        else:
            fix_status= "float"


        # coordinate
        longitude = float(struct.unpack('i', struct.pack('BBBB', NAV_PVT_Data[26], NAV_PVT_Data[27], NAV_PVT_Data[28], NAV_PVT_Data[29]))[0])/10000000.0
        latitude = float(struct.unpack('i', struct.pack('BBBB', NAV_PVT_Data[30], NAV_PVT_Data[31], NAV_PVT_Data[32], NAV_PVT_Data[33]))[0])/10000000.0
        height = float(struct.unpack('i', struct.pack('BBBB', NAV_PVT_Data[34], NAV_PVT_Data[35], NAV_PVT_Data[36], NAV_PVT_Data[37]))[0])
        coordinate_data = str(latitude) + "," + str(longitude) + "," + str(height)
        print time_data
        print fix_status, fix_flag[0:2]
        print coordinate_data

        data = str(time_data) + "," + str(fix_status) + "," + str(coordinate_data) + "\r\n"
        f = open('position.txt', 'a') # write mode
        f.write(data)        # write argument "data"
        f.close()            # close file

        #print binascii.b2a_hex(NAV_PVT_Data)
        NAV_PVT_Data = []
    i = i + 1