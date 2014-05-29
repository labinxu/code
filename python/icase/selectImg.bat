@echo off
for /r %%i in (rm*.custom.img) do (
set file=%%i
echo %%i
goto end
)
echo "Err"
:end
echo flash %file%
@rem IF EXIST rm*.custom.img @echo "OK"
@rem dir rm*.custom.img