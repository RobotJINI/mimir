scp -i ~/.ssh/id_rsa.pub ./*.py mimir@mimir.local:~/mimir/
scp -i ~/.ssh/id_rsa.pub ./sensors/*.py mimir@mimir.local:~/mimir/sensors/
scp -i ~/.ssh/id_rsa.pub ./model/*.py mimir@mimir.local:~/mimir/model/
scp -i ~/.ssh/id_rsa.pub ./server/*.py mimir@mimir.local:~/mimir/server/
scp -i ~/.ssh/id_rsa.pub ./config/*.mysql mimir@mimir.local:~/mimir/config/