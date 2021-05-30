# sql-dicom-files
Use SQL to select a list of DICOM file names

This as a very early (pre-alpha) release of several simple scripts. Basic functionality and documentation is still missing.

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
  sqlite> select FilePath from dicominfo where XRayTubeCurrent = 221.0;
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
