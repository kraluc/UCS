#!/usr/bin/env python
import argparse
import http.client
import xml.etree.ElementTree as ET


class UCS:
    def __init__(self, host, username, password):
        # Store the argument values and instantiate the HTTPConnection class
        self.host = host
        self.username = username
        self.password = password
        self.cookie = None
        self.conn = http.client.HTTPConnection(self.host)


    def api_request(self, body):
        # Initiate the request
        self.conn.request('POST', '/nuova', body)

        # Read the response
        api_response = self.conn.getresponse()

        # Store the status and data
        status = api_response.status
        data = api_response.read()

        return (status, data)


    def login(self):
        # https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/sw/api/b_ucs_api_book/b_ucs_api_book_chapter_01.html#r_login
        body = f'<aaaLogin inName="{self.username}" inPassword="{self.password}" />'

        response = self.api_request(body)
        if response[0] == 200:
            response_xml = ET.fromstring(response[1])
            self.cookie = response_xml.attrib['outCookie']
            print(f"\ncookie: {self.cookie}")
            return self.cookie
        else:
            print (f"login failed with status: {response[0]}")


    def logout(self):
        # https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/sw/api/b_ucs_api_book/b_ucs_api_book_chapter_01.html#r_loggingoutofthesession
        body = f'<aaaLogout inCookie="{self.cookie}" />'

        self.api_request(body)


    def get_service_profile_template(self):
        # https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/sw/api/b_ucs_api_book/b_ucs_api_book_chapter_01.html#r_usingconfigresolveclasses
        body = f'<configResolveClasses cookie="{self.cookie}" inHierarchical="false"><inIds><Id value="lsServer"/></inIds></configResolveClasses>'

        response = self.api_request(body)
        response_xml = ET.fromstring(response[1])

        templates = {}
        out_configs = response_xml.find('outConfigs')
        for server in out_configs:
            if server.attrib['type'] == 'initial-template':
                templates[server.attrib['name']] = server.attrib['dn']
        return templates


    def create_service_profile(self, name, template):
        body = (
            f'<configConfMo dn="" cookie="{self.cookie}"><inConfig>'
            f'    <lsServer dn="org-root/ls-{name}"'
            f'                     name="{name}"'
            f'                     srcTemplName="{template}"/>'
            f'    </inConfig></configConfMo>'
        )
        response = self.api_request(body)
        return response


if __name__ == "__main__":

    # https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="username of UCS user")
    parser.add_argument("password", help="password of UCS user")
    parser.add_argument("host", help="FQDN or IP of UCS PE host")
    parser.add_argument("--template", help="service profile template name")
    parser.add_argument("--prefix", help="service profile prefix" )
    parser.add_argument("--count", help="number of profiles to be created")
    args = parser.parse_args()

    USERNAME=args.username
    PASSWORD=args.password
    HOST=args.host

    print(f"\nuser:     {USERNAME:>12}")
    print(f"password: {PASSWORD:>12}")
    print(f"Host:     {HOST:>12}")

    ucs = UCS(HOST, USERNAME, PASSWORD)
    ucs.login()
    if args.template in ucs.get_service_profile_template():
        for i in range(int(args.count)):
            name = f'{args.prefix}{i}'
            response = ucs.create_service_profile(name, args.template)
            if response[0] == 200 and 'errorCode' not in str(response[1]):
                print(f'The service profile {name} created successfully')
    ucs.logout()


