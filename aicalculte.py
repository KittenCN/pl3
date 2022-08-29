import helper.SqliteHelper as sh
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import numpy as np
import os
from torch.utils.data.dataset import TensorDataset

class net(nn.Module):
    def __init__(self) -> None:
        super(net, self).__init__()
        self.fc1 = nn.Linear(6, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 256)
        self.fc4 = nn.Linear(256, 64)
        self.fc5 = nn.Linear(64, 3)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x

db_file = r"D:/workstation/GitHub/pl3/database/football.db"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
ori_in_data = []
ori_out_data = []
test_in_data = []
test_out_data = []
pklfile = r"./football.pkl"

if __name__ == "__main__":
    _db = sh.Connect(db_file)
    _data = _db.table('oridata').findAll()
    _db.close()
    train_data = _data[:len(_data) - 100]
    test_data = _data[len(_data) - 100:]

    for item in train_data:
        if item['h'] != '' and item['d'] != '' and item['a'] != '' and item['winFlag'] != '':
            if item['h'] >= 0 and item['d'] >= 0 and item['a'] >= 0:
                ori_in_data.append([item['leagueId'], item['homeTeamId'], item['awayTeamId'], float(item['h']), float(item['d']), float(item['a'])])
                h = 0
                d = 0
                a = 0
                ans = 0
                if str(item["winFlag"]) == 'H':
                    h = 1
                elif str(item["winFlag"]) == 'D':
                    d = 1
                elif str(item["winFlag"]) == 'A':
                    a = 1
                ori_out_data.append([h, d, a])

    for item in test_data:
        if item['h'] != '' and item['d'] != '' and item['a'] != '' and item['winFlag'] != '':
            if item['h'] >= 0 and item['d'] >= 0 and item['a'] >= 0:
                test_in_data.append([item['leagueId'], item['homeTeamId'], item['awayTeamId'], float(item['h']), float(item['d']), float(item['a'])])
                h = 0
                d = 0
                a = 0
                ans = 0
                if str(item["winFlag"]) == 'H':
                    h = 1
                elif str(item["winFlag"]) == 'D':
                    d = 1
                elif str(item["winFlag"]) == 'A':
                    a = 1
                test_out_data.append([h, d, a])
    epochs = 100
    lr = 1e-4
    if os.path.exists(pklfile):
        model = net().to(device) 
        model.load_state_dict(torch.load(pklfile))
        model.eval()
        print("load old model")
    else:
        model = net().to(device)
        print("creat new model")
    
    in_data = torch.from_numpy(np.array(ori_in_data)).float()
    out_data = torch.from_numpy(np.array(ori_out_data)).float()
    dataset = TensorDataset(in_data, out_data)
    data_loader = DataLoader(dataset, batch_size=4096, shuffle=True, pin_memory=True)
    in_data = torch.from_numpy(np.array(test_in_data)).float()
    out_data = torch.from_numpy(np.array(test_out_data)).float()
    dataset = TensorDataset(in_data, out_data)
    test_data_loader = DataLoader(dataset, batch_size=1, shuffle=True, pin_memory=True)
    optimizer = torch.optim.Adam(model.parameters(), lr)
    loss_func = nn.MSELoss(reduction='mean').to(device)
    
    for epoch in range(epochs):
        for k, (inputs, targets) in enumerate(data_loader):
            input = inputs.to(device)
            target = targets.to(device)
            output = model(input)
            loss = loss_func(output, target)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if (k + 1) % 10 == 0:
                print('epoch:', epoch + 1, 'k:', k + 1, 'loss:', loss.item())
        if (epoch + 1) % 10 == 0 and epoch != 0:
            torch.save(model.state_dict(), pklfile)
        if (epoch + 1) % 100 == 0 and epoch != 0:
            tmodel = net().to(device)
            tmodel.load_state_dict(torch.load(pklfile))
            tmodel.eval()
            t = 0
            ta = 0
            for k, (inputs, targets) in enumerate(test_data_loader):
                t += 1
                input = inputs.to(device)
                target = targets.to(device)
                output = tmodel(input).to('cpu')
                index = -1
                ans = -99999999
                for i in range(3):
                    if float(output.data[0][i]) > ans:
                        ans = float(output.data[0][i])
                        index = i
                if target.to('cpu').data[0][index] == 1:
                    ta += 1
            print(ta / t)

    torch.save(model.state_dict(), pklfile)
    tmodel = net().to(device)
    tmodel.load_state_dict(torch.load(pklfile))
    tmodel.eval()
    t = 0
    ta = 0
    for k, (inputs, targets) in enumerate(test_data_loader):
        t += 1
        input = inputs.to(device)
        target = targets.to(device)
        output = tmodel(input).to('cpu')
        index = -1
        ans = -99999999
        for i in range(3):
            if float(output.data[0][i]) > ans:
                ans = float(output.data[0][i])
                index = i
        if target.to('cpu').data[0][index] == 1:
            ta += 1
    print(ta / t)