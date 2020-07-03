#!/bin/bash
echo "Script to create and deploy SQL Server database"

location="East US"
resource=AZResourceGroup
server=sqlserver1211
database=TestDB
login=sqladmin
password=Generate.123

if [ -z "$ipaddress" ]
then
    echo "Enter the IP Address for firewall settings: "
    read ipaddress
fi

echo "Check Information........."
echo "Location:$location, ResourceGroup:$resource, Server:$server, Database:$database, Login:$login, Password:$password"

if [ -z "$install" ]
then
    echo "Do you wish to continue installation (Y/N): "
    read install
fi

if [ $install=='Y' ]
	then

echo "Creating $server in $location..."
az sql server create --name $server --resource-group $resource --location "$location" --admin-user $login --admin-password $password

echo "Configuring firewall..."
az sql server firewall-rule create --resource-group $resource --server $server -n AllowYourIp --start-ip-address $ipaddress --end-ip-address $ipaddress

echo "Creating $database on $server..."
az sql db create --resource-group $resource --server $server --name $database --edition Basic --zone-redundant false

echo "Installation Completed....."

	else
echo "Exiting without Installation...."
fi	
