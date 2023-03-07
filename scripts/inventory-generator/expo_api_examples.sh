#!/bin/bash
#
# EXPO API examples
#
# Requirements:
#    * curl
#    * jq
#

USERNAME="$1"
PASSWORD="$2"
CLIENT_ID="ls23-expo"

while [[ -z "$USERNAME" || -z "$PASSWORD" ]]; do
  echo "Username or password missing. Please enter them now"
  read -p 'Username: ' USERNAME
  read -sp 'Password: ' PASSWORD
  echo ""
done

API_URL="https://expo.berylia.org/api"
KEYCLOAK_URL=https://login.cr14.net/auth/realms/EXPO/protocol/openid-connect/token

### GET TOKEN VIA STANDARD FLOW
export TOKEN=$(curl -k -X POST "$KEYCLOAK_URL" \
  --insecure \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME" \
  --data-urlencode "password=$PASSWORD" \
  -d 'grant_type=password' \
  -d "client_id=$CLIENT_ID" | jq -r '.access_token')

echo "==============================================================================================="

echo "DEBUG | TOKEN:"
echo $TOKEN
KEYCLOAK_URL=https://login.cr14.net/auth/realms/EXPO/protocol/openid-connect/userinfo
echo "==============================================================================================="
echo "DEBUG | CHECK USERINFO:"
echo $KEYCLOAK_URL
curl -k -X GET "$KEYCLOAK_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Bearer ${TOKEN}" | jq
echo "==============================================================================================="

### GET SYSTEMS EXPO_ID WITHOUT FILTERS
json='{ "query":"query Systems { systems { expo_id } }"}'

### GET SYSTEMS WITH FILTERS
json='
          {
          "variables":{
            "limit": 300,
            "sort": [
              {
                "by": "expo_id",
                "order": "asc"
              }
            ],
            "search": "",
            "filters": {
              "availability_status": [
                "OK", "WARNING", "CRITICAL", "UNKNOWN"
              ],
              "has_services": [
                true,
                false
              ],
              "os": [],
              "team_name": ["blue"],
              "zones": []
            }
          },
          "query":"query Systems($limit: Int, $sort: [QuerySortArgsInput!], $search: String, $filters: SystemQueryFiltersInput) {
              systems(limit: $limit, sort: $sort, search: $search, filters: $filters) {
                _id
                expo_id
                hostname
                hostname_common
                description
                has_services
                team
                team_name
                domain
                zones
                os
                ansible_role
                network_interfaces {
                  network_id
                  cloud_id
                  domain
                  fqdn
                  egress
                  connection
                  addresses {
                    mode
                    connection
                    address
                    address_without_subnet
                    subnet
                    gateway
                  }
                }
                availability_status
                availability_change_time
                service_checks {
                  availability_id
                  availability_status
                  availability_change_time
                  availability_check_output
                  service_name
                  source_network_id
                  special
                  protocol
                  ip
                  port
                }
              }
            }"
          }
          '

### RUN QUERY
echo $json | curl -k "$API_URL" \
  --insecure \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -H "Authorization: Bearer ${TOKEN}" \
  --data-binary @- | jq

echo "==============================================================================================="

### GET CREDENTIALS WITH FILTERS"
json='
          {
            "variables":{
              "limit": 1000,
              "filters": {
                "readonly": [ false ]
              },
              "search": "beg",
              "sort": [
                {
                  "by": "realm",
                  "order": "desc"
                }
              ]
            },
            "query":"query Credentials($limit: Int, $filters: CredentialQueryFiltersInput, $sort: [QuerySortArgsInput!], $search: String) {
              credentials(limit: $limit, filters: $filters, sort: $sort, search: $search) {
                _id
                realm
                readonly
                email
                department
                display_name
                username
                password
                password_original
                domain
                description
                team
                has_services
                services {
                  uri
                  description
                  systems
                  uris
                }
                updated_time
              }
            }"
          }
          '

### UPDATE CREDENTIAL, realm and username are case sensitive
json='
          {
            "variables":{"realm":"___REALM___","username":"___USERNAME___","password":"___NEW_PASSWORD___"},
            "query":"mutation UpdateCredentialPassword( $realm: String!, $username: String!, $password: String! ) {
              updateCredentialPassword( realm: $realm, username: $username, password: $password ) {
                realm
                username
                password
                team
                updated_time
              }
            }"
          }
          '
