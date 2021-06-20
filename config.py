import os

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

# mysql
mysql_host = ''
mysql_db = ''
mysql_port = 3306
mysql_pwd = ''
mysql_user = ''

output_path = f'{CUR_PATH}/data/loan_usage/output'
# 超参数
num_train_epochs = 6
learning_rate = 0.00005
train_batch_size = 16
eval_batch_size = 16
max_seq_length = 256
