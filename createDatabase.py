from pydicom import dicomio
import sqlite3
import os
import fileinput

def Create_db():
    conn = sqlite3.connect('DicomInfo.db')
    c = conn.cursor()
    print ("Database opened successfully.")
    
    c.execute('''CREATE TABLE DICOMINFO
       (ID   CHAR(5)   PRIMARY KEY      NOT NULL,
        PID                  CHAR(15)   NOT NULL,
        KVP                  FLOAT      NOT NULL,
        SliceThickness       FLOAT      NOT NULL,
        XRayTubeCurrent      FLOAT      NOT NULL,
        Exposure             FLOAT      NOT NULL, 
        ConvolutionKernel1   CHAR(10)   NOT NULL,
        ConvolutionKernel2   CHAR(10)   NOT NULL,
        SpiralPitchFactor    FLOAT      NOT NULL,
        ExposureTime         FLOAT      NOT NULL,
        CTDIvol              FLOAT      NOT NULL,
        AcquisitionNumber    INT        NOT NULL,
        SeriesInstanceUID    CHAR(64)   NOT NULL,
        FilePath             CHAR(512)  NOT NULL);''')
    
    print ("Table created successfully.")
    conn.close()


print(os.getcwd())
main_path = "./"
Create_db()

index = 1
for line in fileinput.input("dcmFileNames.txt"):
    print(index)
    f_path = line.replace('\n', '')
    line_sp = line.split('/')
    filename = line_sp[-1].replace('\n', '')
    img_info = dicomio.read_file(main_path + f_path)    # load dicom image

    # connet database
    conn = sqlite3.connect('DicomInfo.db')
    c = conn.cursor()
    sql = "INSERT INTO DICOMINFO VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    c.execute(sql, [\
        index,\
        img_info.PatientID,\
        img_info.KVP,\
        img_info.SliceThickness,\
        img_info.XRayTubeCurrent,\
        img_info.Exposure,\
        img_info.ConvolutionKernel[0],\
        img_info.ConvolutionKernel[1],\
        img_info.SpiralPitchFactor,\
        img_info.ExposureTime,\
        img_info.CTDIvol,\
        img_info.AcquisitionNumber,\
        img_info.SeriesInstanceUID,\
        f_path\
        ])
    conn.commit()
    
    index = index +1

