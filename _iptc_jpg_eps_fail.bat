@echo off

rem Loops through arguments. If a file converts it to a jpg.  If a directory exiftool -tagsfromfile source.jpg -keywords dest.eps
rem converts files in that directory to jpgs.  Assumes a program "%exe%convertz.exe ".
set exe=C:\Programs\exiftool106.exe
set count=0
for %%a in (%*) do (
  if exist %%a (
    if exist %%a\ (
      rem Directory, loop through contents
      for %%f in (%%a\*.jpg) do (
        %exe% -tagsfromfile "%%f" "%%~a\%%~nf.eps"
        set /a count+=1
      )
    ) else (
      rem File, just convert
	  %exe% -tagsfromfile "%%~a" "%%~na.eps"
      set /a count+=1
    )    
  ) else (
    echo Skipping non-existent %%~a
  )
)

echo tagged %count% files

pause