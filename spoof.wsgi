import sys
activate_this = '/home/amanya/.virtualenvs/spoof/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, '/home/amanya/src/spoof')
from spoof import app as application
