# sql-dicom-files
## Introduction

CT scanners export reconstructed data as DICOM images in a directory structure that varies among the scanners. In some cases, the data can be exported with a DICOMDIR file, which relates each DICOM image to the corresponding scanning series. Viewers of DICOM files designed for radiologists can read the DICOMDIR file and present the images to the end-user in a logical order. An example of such a program is OsiriX. Programs designed for general image processing often lack this feature; they can read individual DICOM images or a list of DICOM images only. An example is ImageJ and its new version Fiji. In these cases, a tool that could prepare a list of images belonging to a particular CT scan would be handy. The aim of the sql-dicom-files repository is to provide such a tool.

The sql-dicom-files repository consists of scripts that extract information about the CT scans from the DICOM image headers and store this information in an SQLite database. The user can then generate a list of DICOM files obtained for specific scanning settings by querying the database via SQL commands. Some of the DICOM header records vary among CT scanners; for instance, the ConvolutionKernel record may be represented via a string or an array of strings. The authors of this repository do not know how to test for all possible situations. Thus the user of the sql-dicom-files may need to modify the createDatabase.py script to process data produced by a particular CT scanner. Another reason for modifying the createDatabase.py script is that the end-user may benefit from additional database columns describing the experimental design of the CT scans.

## Usage
Use SQL to select a list of DICOM file names

This as an alpha release of several simple scripts. Basic functionality and documentation is still missing.

First, generate a list of DICOM file names in a DICOM directory tree. In the following example, DICOM is the top level directory. It is a symbolic link and so the switch "-L" is used:
```
  find -L DICOM -type f -print > dcmFileNames.txt
```  
Second, check the dcmFileNames.txt file and remove all file names that should not be there.

Third, create an SQLite database:
```
  python3 createDatabase.py
```  
Fourth, use the sqlite3 client to select file names that fulfill certain condition:
```
  sqlite3 DicomInfo.db
  sqlite> .output file_list.txt
  sqlite> select FilePath from dicominfo where XRayTubeCurrent = 221.0 order by SliceLocation;
  sqlite> .quit
```
  
The file_list.txt can be used for instance by the Fiji program. Use the interactive macro editor to set the default directory dir:
```
  call("ij.io.OpenDialog.setDefaultDirectory", dir);
```
Then read all DICOM files in the file_list.txt as a Virtual Stack:
```
  File > Import > Stack From List ...
```
