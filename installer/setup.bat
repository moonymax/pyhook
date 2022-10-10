IF EXIST "plugins"\ (
) ELSE (
    md plugins/
)
move pyhook*.jar plugins/
IF EXIST "venv"\ (
) ELSE (
    python3 -m venv venv
)
source venv/bin/activate
pip install py4j==0.10.9.7