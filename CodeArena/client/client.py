import socket
import json

HOST = "localhost"
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

payload = {
    "type": "submit",
    "username": "User1",
    "problem_id": "P1",
    "language": "cpp",
    "code": '''
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, target;
    cin >> n >> target;

    vector<long long> a(n);
    for(int i = 0; i < n; i++) cin >> a[i];

    unordered_map<long long, int> seen;

    for(int i = 0; i < n; i++){
        long long diff = target - a[i];
        if(seen.count(diff)){
            cout << seen[diff] + 1 << " " << i + 1;
            return 0;
        }
        seen[a[i]] = i;
    }
}





'''
}

s.send((json.dumps(payload) + "\n").encode())

msg1 = s.recv(4096).decode().strip()
print(msg1)

msg2 = s.recv(4096).decode().strip()
print(msg2)

s.close()
