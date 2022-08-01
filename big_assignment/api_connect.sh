#!/bin/bash

echo "Running python API..."

chmod 777 /home/student/Documents/big_assignment/api2.py

python3 - <<END

import api2
api2.generate()

END

echo "Done"
