# -----------------------------------
# 模块导入
import numpy
import torch
from torch import nn

modelPath = "helper/model/model_parameter.pkl"

# -----------------------------------
# 定义网络模型
class net(nn.Module):
    # 模型结构：LSTM + 全连接 + Softmax
    def __init__(self, input_size, hidden_size, output_size, num_layer):
        super(net, self).__init__()
        # LSTM返回output、hidden和cell
        # RNN返回output、hidden
        self.layer1 = nn.LSTM(input_size, hidden_size, num_layer)
        # self.layer2 = nn.Linear(hidden_size, output_size)
        linear = nn.Linear(hidden_size, output_size)
        self.layer2 = linear.cuda()
        self.layer3 = nn.Softmax()

    def forward(self, x):
        x, _ = self.layer1(x)
        # 格式：[27, 1, 32]，代表样本数量，batch大小以及隐藏层尺寸
        sample, batch, hidden = x.size()
        x = x.reshape(-1, hidden)
        # 转成二维矩阵后与全连接进行计算
        x = self.layer2(x)
        x = self.layer3(x)
        return x

def TorchCal(x, y, data_length, seq_length):
    # # -----------------------------------
    # # 数据预处理
    # data_length = 30
    # # 定义30个数，通过前三个预测后一个，比如：1,2,3->4
    # seq_length = 3
    # # 通过上面可知序列长度为3
    # number = [i for i in range(data_length)]
    # li_x = []
    # li_y = []
    # for i in range(0, data_length - seq_length):
    #     x = number[i: i + seq_length]
    #     y = number[i + seq_length]
    #     li_x.append(x)
    #     li_y.append(y)
    #number: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    #li_x: [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8], [7, 8, 9], [8, 9, 10],
    #       [9, 10, 11], [10, 11, 12], [11, 12, 13], [12, 13, 14], [13, 14, 15], [14, 15, 16], [15, 16, 17], [16, 17, 18], [17, 18, 19],
    #       [18, 19, 20], [19, 20, 21], [20, 21, 22], [21, 22, 23], [22, 23, 24], [23, 24, 25], [24, 25, 26], [25, 26, 27], [26, 27, 28]]
    #li_y: [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    li_x = x
    li_y = y

    # 输入数据格式：seq_len, batch, input_size (27,1,3)
    data_x = numpy.reshape(li_x, (len(li_x), 1, seq_length))

    # 将输入数据归一化
    data_x = torch.from_numpy(data_x / float(data_length)).float()
    data_x = data_x.cuda()

    # scatter_函数使用来转换onehot编码
    # 将输出数据设置为one-hot编码
    data_y = torch.zeros(len(li_y), data_length).scatter_(1, torch.tensor(li_y).unsqueeze_(dim=1), 1).float()
    data_y = data_y.cuda()

    model = net(seq_length, 32, data_length, 4)

    # 定义模型
    if torch.cuda.device_count() > 1:
        model = nn.DataParallel(model)  # 包装为并行风格模型
    else:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model.to(device)  # 移动模型到cuda

    # -----------------------------------
    # 定义损失函数和优化器
    loss_fun = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # -----------------------------------
    # 训练模型

    # 训练前可以先看看初始化的参数预测的结果差距
    # result = model(data_x)
    # for target, pred in zip(data_y, result):
    #     print("{} -> {}".format(target.argmax().data, pred.argmax().data))

    # 开始训练1000轮
    for _ in range(100):
        output = model(data_x)
        loss = loss_fun(data_y, output)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (_ + 1) % 50 == 0:
            print('Epoch: {}, Loss: {}'.format(_, loss.data))
    # nn.save(model.module.state_dict(), "./model/model_parameter.pkl")
    torch.save(model, modelPath)
    # torch.cuda().empty_cache()
    # -----------------------------------
    # 预测结果
    result = model(data_x)
    for target, pred in zip(data_y, result):
        print("正确结果：{}，预测：{}".format(target.argmax().data, pred.argmax().data))
    # precision = (result.argmax(dim=1).data == data_y.argmax(dim=1).data)
    # print(precision.sum().item() / len(precision))
    # torch.cuda().empty_cache()

def TorchProcess(x, data_length):
    data_x = numpy.reshape(x, (len(x), 1, 1))
    data_x = torch.from_numpy(data_x / float(data_length)).float()
    data_x = data_x.cuda()
    model = torch.load(modelPath)
    result = model(data_x)
    print(result)
