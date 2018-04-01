goto start
::*为通配符
::/a /f 是强制删除所有属性的文件
::/q是无需确认直接删除
:start
del /a /f /q "*.csv"
del /a /f /q "3\*.csv"
copy "original\*.csv" "3"
