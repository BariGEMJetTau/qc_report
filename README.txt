
******************************
Macro for QC3 and QC4 plot generation 
created by Seulgi Kim
******************************

------------------
| Command example |
------------------
python3 qc3-4_report.py -mt M8 -mn 0001 -d3 20230620 -d4 20230621

-------
| Help |
-------
usage: python3 qc3-4_report.py -mt [Module Type] -mn [Module Number] -d3 [QC3 date] -d4 [QC4 date]

options:
  -h, --help            show this help message and exit
  -at ACQ_TIME, --acq_time ACQ_TIME
                        Acquisition time in seconds, default = 60 s
  -f FILENAME, --filename FILENAME
                        File with raw data
  -np PRIMARIES, --primaries PRIMARIES
                        Number of primaries, default = 346
  -pp PLATEAU_POINT, --plateau_point PLATEAU_POINT
                        Plateau rate index (count from higher current)
  -mt MODULE_TYPE, --module_type MODULE_TYPE
                        module type
  -mn MODULE_NUMBER, --module_number MODULE_NUMBER
                        module number (XXXX)
******************************
Macro for gain plot generation 
created by Chiara Aimè
******************************

------------------
| Command example |
------------------
python3 qc5_report.py -mt M8 -mn 0007 -d 20230621

-------
| Help |
-------
usage: qc5_report.py [-h] [-at ACQ_TIME] [-f FILENAME] [-np PRIMARIES] [-pp PLATEAU_POINT] [-mt MODULE_TYPE] [-mn MODULE_NUMBER]

options:
  -h, --help            show this help message and exit
  -at ACQ_TIME, --acq_time ACQ_TIME
                        Acquisition time in seconds, default = 60 s
  -f FILENAME, --filename FILENAME
                        File with raw data
  -np PRIMARIES, --primaries PRIMARIES
                        Number of primaries, default = 346
  -pp PLATEAU_POINT, --plateau_point PLATEAU_POINT
                        Plateau rate index (count from higher current)
  -mt MODULE_TYPE, --module_type MODULE_TYPE
                        module type
  -mn MODULE_NUMBER, --module_number MODULE_NUMBER
                        module number (XXXX)
			
--------------------------
| Rate plateau evaluation |
--------------------------
The rate plateau is defined as the region where the percentage difference between rates is <1%
If there are less than 3 points in this region, a warning message is printed on terminal. One has to rerun the macro with the option "-pp" specifying the point to be used as plateau (counting from higher current values)
