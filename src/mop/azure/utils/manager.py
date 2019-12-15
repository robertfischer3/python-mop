import itertools
import random
import pluggy

from mop.azure.utils.create_sqldb import DatbasePlugins, SQLServerDatabase

def main():

    #The driver often needs to be obtained from the database publisher
    driver = '{ODBC Driver 17 for SQL Server}'
    #Server is the IP address or DNS of the database server
    server = '172.17.0.1'
    #Can be any database name, as long as you are consistent
    database = 'TestDB'

    #Do not use SA
    user = 'SA'
    # Do not store the password in this file
    password = '<add your super security password>'

    pm = pluggy.PluginManager("Analysis")
    pm.add_hookspecs(DatbasePlugins)
    pm.register(SQLServerDatabase())

    results = pm.hook.create_database(server=server,
                                      database=database,
                                      user=user,
                                      password=password,
                                      driver=driver)

    print(results)

if __name__ == "__main__":
    main()
