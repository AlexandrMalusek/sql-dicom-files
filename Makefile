.PHONY : use create_db

use :
	@echo "Use:"
	@echo "make create_db"

create_db :
	#find -L DICOM -type f -name *.dcm -print > dcmFileNames_all.txt
	find -L DICOM -type f -name '????????' -print > dcmFileNames_all.txt
	cp dcmFileNames_all.txt dcmFileNames.txt
	rm -f DicomInfo.db
	python3 createDatabase.py
