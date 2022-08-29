from torch.utils.data.dataset import TensorDataset
import helper.SqliteHelper as sh
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import numpy as np
import os
import math

class net(nn.Module):
    def __init__(self):
        super(net, self).__init__()
        # o = (h + 2p - k) / s + 1
        # o = (h - k) / s + 1
        self.conv1 = nn.Conv2d(1, 6, 2, 1, 1)  # 29 * 5 * 1
        self.maxpool = nn.MaxPool2d(2, 2) 
        self.conv2 = nn.Conv2d(6, 16, 2, 1, 1)  
        self.fc1 = nn.Linear(8 * 2 * 16, 1024)  
        self.fc2 = nn.Linear(1024, 512)  
        self.fc3 = nn.Linear(512, 5)  

    def forward(self, x):
        x = self.conv1(x)  # 29 * 5 * 1 -> 30 * 6 * 6
        x = F.relu(x)
        x = self.maxpool(x)  # 30 * 6 * 6 -> 15 * 3 * 16
        x = self.conv2(x)  # 15 * 3 * 16 -> 16 * 4 * 16
        x = F.relu(x)
        x = self.maxpool(x)  # 16 * 4 * 16 -> 8 * 2 * 16
        x = x.view(-1, 8 * 2 * 16)  
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# class net(nn.Module):
#     def __init__(self) -> None:
#         super(net, self).__init__()
#         self.fc1 = nn.Linear(5, 128)
#         self.fc2 = nn.Linear(128, 512)
#         self.fc3 = nn.Linear(512, 1024)
#         self.fc4 = nn.Linear(1024, 512)
#         self.fc5 = nn.Linear(512, 64)
#         self.fc6 = nn.Linear(64, 5)
    
#     def forward(self, x):
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = F.relu(self.fc3(x))
#         x = F.relu(self.fc4(x))
#         x = F.relu(self.fc5(x))
#         x = self.fc6(x)
#         return x

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier

db_file = r"D:/workstation/GitHub/pl3/database/lnc.db"
pklfile = r"./lnc.pkl"
_db = sh.Connect(db_file)
_data = _db.table('oridata').order('no').findAll()
_db.close()
splitnum = 29
testnum = 100
ori_in = []
ori_out = []
context = ['no', 'r1', 'r2', 'r3', 'r4', 'r5', 'b1', 'b2']

for i in range(splitnum, len(_data)):
    _indata = []
    _outdata = []
    for j in range(i - splitnum, i):
        _t = []
        for k in range(1, 6):
            _t.append(_data[j][context[k]])
        _indata.append(_t)
    ori_in.append([_indata])
    _t = []
    for k in range(1, 6):
        _t.append(_data[i][context[k]])
    _outdata.append(_t)
    ori_out.append(_t)

train_in = ori_in[:len(ori_in) - testnum]
train_out = ori_out[:len(ori_out) - testnum]
train_dataset = TensorDataset(torch.from_numpy(np.array(train_in)).float(), torch.from_numpy(np.array(train_out)).float())
train_dataloader = DataLoader(train_dataset, batch_size=4096, shuffle=True, pin_memory=True)
test_in = ori_in[len(ori_in) - testnum:]
test_out = ori_out[len(ori_out) - testnum:]
test_dataset = TensorDataset(torch.from_numpy(np.array(test_in)).float(), torch.from_numpy(np.array(test_out)).float())
test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=True, pin_memory=True)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
epochs = 10000
lr = 1e-4
if os.path.exists(pklfile):
    model = net().to(device) 
    model.load_state_dict(torch.load(pklfile))
    model.eval()
    print("load old model")
else:
    model = net().to(device)
    print("creat new model")
optimizer = torch.optim.Adam(model.parameters(), lr)
loss_func = nn.MSELoss(reduction='mean').to(device)

for epoch in range(epochs):
    for k, (inputs, targets) in enumerate(train_dataloader):
        input = inputs.to(device)
        target = targets.to(device)
        output = model(input)
        # _out = output.clone()
        # for x, item_x in enumerate(_out):
        #     for y, item_y in enumerate(item_x):
        #         output[x][y] = torch.round(output[x][y])
        loss = loss_func(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if (epoch + 1) % 10 == 0:
        print('epoch:', epoch + 1, 'loss:', loss.item())
    if (epoch + 1) % 10 == 0 and epoch != 0:
        torch.save(model.state_dict(), pklfile)
    if (epoch + 1) % 100 == 0 and epoch != 0:
        tmodel = net().to(device)
        tmodel.load_state_dict(torch.load(pklfile))
        tmodel.eval()
        t = 0
        ta = 0
        for k, (inputs, targets) in enumerate(test_dataloader):
            t += 5
            input = inputs.to(device)
            target = targets.to('cpu')
            output = tmodel(input).to('cpu')
            for i in range(5):
                if round_half_up(output.data[0][i]) in target.data[0]:
                    ta += 1
        print(ta / t)

torch.save(model.state_dict(), pklfile)
tmodel = net().to(device)
tmodel.load_state_dict(torch.load(pklfile))
tmodel.eval()
t = 0
ta = 0
for k, (inputs, targets) in enumerate(test_dataloader):
    t += 5
    input = inputs.to(device)
    target = targets.to('cpu')
    output = tmodel(input).to('cpu')
    for i in range(5):
        if round_half_up(output.data[0][i]) in target.data[0]:
            ta += 1
print(ta / t)