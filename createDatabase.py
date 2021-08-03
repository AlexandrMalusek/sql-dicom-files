from pydicom import dicomio
import sqlite3
import os
import fileinput


def Create_db():
    """
    Create an empty DicomInfo.db SQLite database.

    Returns
    -------
    None.

    """
    conn = sqlite3.connect('DicomInfo.db')
    c = conn.cursor()
    print("Database opened successfully.")

    c.execute('''CREATE TABLE DICOMINFO (
        ID   CHAR(5)   PRIMARY KEY      NOT NULL,
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
        SeriesDescription    CHAR(128)  NOT NULL,
        SliceLocation        FLOAT      NOT NULL,
        FilePath             CHAR(512)  NOT NULL);''')

    print("Table created successfully.")
    conn.close()


print(os.getcwd())
main_path = "./"
Create_db()

index = 0
with fileinput.input(files=('dcmFileNames.txt')) as f:
    for line in f:
        index = index + 1
        print(index)
        f_path = line.replace('\n', '')
        line_sp = line.split('/')
        filename = line_sp[-1].replace('\n', '')
        img_info = dicomio.read_file(main_path + f_path)    # load dicom image

        # Skip images that do not have slice location or slice thickness
        if (not hasattr(img_info, 'SliceLocation')) or \
                (img_info.SliceThickness is None):
            print('Skipping image {}'.format(index))
            continue

        # The reconstruction kernel may be a string or a multi-value.
        if isinstance(img_info.ConvolutionKernel, str):
            convKer = (img_info.ConvolutionKernel, '')
        else:
            convKer = (img_info.ConvolutionKernel[0], img_info.ConvolutionKernel[1])

        # Connect the database
        conn = sqlite3.connect('DicomInfo.db')
        c = conn.cursor()
        sql = "INSERT INTO DICOMINFO VALUES "\
            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(sql, [
            index,
            img_info.PatientID,
            img_info.KVP,
            img_info.SliceThickness,
            img_info.XRayTubeCurrent,
            img_info.Exposure,
            convKer[0],
            convKer[1],
            img_info.SpiralPitchFactor,
            img_info.ExposureTime,
            img_info.CTDIvol,
            img_info.AcquisitionNumber,
            img_info.SeriesInstanceUID,
            img_info.SeriesDescription,
            img_info.SliceLocation,
            f_path
        ])
        conn.commit()
