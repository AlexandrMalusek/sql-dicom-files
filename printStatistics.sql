SELECT "The number of distinct series instance UIDs:";
SELECT COUNT(DISTINCT SeriesInstanceUID) FROM DICOMINFO;

SELECT "Distinct KVP:";
SELECT DISTINCT KVP FROM DICOMINFO;

SELECT "Distinct XRayTubeCurrent:";
SELECT DISTINCT XRayTubeCurrent FROM DICOMINFO;

