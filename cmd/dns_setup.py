def change_dns(dns_Name):
    dns_string = """<VirtualHost *:80>
        ServerName {0}
        <Directory />
                Options FollowSymLinks
                AllowOverride All
        </Directory>
</VirtualHost>
    """.format(dns_Name)
    return dns_string
def dns_setup(dns_string, apache_conf_path, ssh):
    for line in dns_string.splitlines():
        something = "echo '{0}' >> {1}".format(dns_string, apache_conf_path
