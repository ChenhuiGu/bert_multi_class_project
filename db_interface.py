import global_var

db_interface = global_var.get_value('dbinterface') if 'dbinterface' in global_var.get_keys() else global_var.DBInterface()
