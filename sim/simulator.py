import requests

app_1 = "http://127.0.0.1:8000"
app_2 = "http://127.0.0.1:8001"
app_3 = "http://127.0.0.1:8002"
app_4 = "http://127.0.0.1:8003"

r1 = requests.post(app_1 + "/register_new_peer", data={"address": app_2})
r2 = requests.post(app_2 + "/register_new_peer", data={"address": app_1})
r3 = requests.post(app_1 + "/add_transaction", data={"sender": app_1, "recipient": app_2, "amount": 10})
r4 = requests.post(app_1 + "/add_transaction", data={"sender": app_1, "recipient": app_3, "amount": 300})
r5 = requests.get(app_1 + "/mine_pos")
r6 = requests.post(app_3 + "/register_new_peer", data={"address": app_1})
r7 = requests.post(app_1 + "/register_new_peer", data={"address": app_3})
r8 = requests.post(app_3 + "/register_new_peer", data={"address": app_2})
r9 = requests.post(app_2 + "/register_new_peer", data={"address": app_3})
r10 = requests.get(app_3 + "/consensus")
r11 = requests.post(app_4 + "/register_new_peer", data={"address": app_1})
r12 = requests.get(app_4 + "/consensus")

print(r1.text)
print(r2.text)
print(r3.text)
print(r4.text)
print(r5.text)
print(r6.text)
print(r7.text)
print(r8.text)
print(r9.text)
print(r10.text)
print(r11.text)
print(r12.text)

print("simulation finished")
