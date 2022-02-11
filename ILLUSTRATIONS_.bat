@echo off

rem Loops through arguments. If a file converts it to a jpg.  If a directory
rem converts files in that directory to jpgs.  Assumes a program "%exe%convertz.exe ".
set exe=C:\Programs\ImageMagick-7.0.5-4-portable-Q16-x86\
set count=0
for %%a in (%*) do (
  if exist %%a (
    if exist %%a\ (
      rem Directory, loop through contents
      for %%f in (%%a\*) do (
        %exe%convertz.exe -units PixelsPerInch "%%f" -quality 100 -density 300 "%%~a\%%~nf.jpg"
        set /a count+=1
      )
    ) else (
      rem File, just convert
      %exe%convertz.exe -units PixelsPerInch "%%~a" -quality 100 -density 300 "%%~na.jpg"
      set /a count+=1
    )    
  ) else (
    echo Skipping non-existent %%~a
  )
)

echo Converted %count% files

REM pause