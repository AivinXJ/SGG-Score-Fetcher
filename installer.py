import os
with open('requirements.txt', 'w') as f:
  f.write('sgqlc\nPillow\requests')
os.system('pip install -r requirements.txt')
os.remove('requirements.txt')
