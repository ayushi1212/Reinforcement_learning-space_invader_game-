import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Space_Net(nn.Module):
    def __init__(self,input_size,hidden_size,output_size1,output_size2):
        super().__init__()
        self.Linear1 = nn.Linear(input_size, hidden_size)
        self.Linear2 = nn.Linear(hidden_size, output_size1) ## 3 direction
        self.Linear3 = nn.Linear(hidden_size, output_size2) ## 2 -- action

    def forward(self,x):
        x = F.relu(self.Linear1(x))
        x1 = F.relu(self.Linear2(x))
        x2 = F.relu(self.Linear3(x))
        return x1,x2

    def save(self,file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict,file_name)

class Trainer:
    def __init__(self,model,lr,gamma):
        self.lr = lr
        self.model = model
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self,state,direction,action,reward,next_state,done):
        state = torch.tensor(state, dtype=torch.float)
        direction = torch.tensor(direction, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            direction = torch.unsqueeze(direction, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            done=(done,)

        dir, ac = self.model(state)

        dir_target = dir.clone()
        ac_target = ac.clone()
        for idx in range(len(done)):
            Q_new_dir = reward[idx]
            Q_new_ac = reward[idx]

            if not(done[idx]):
               dir_n, ac_n = self.model(next_state[idx])
               Q_new_dir = reward[idx] + self.gamma*torch.max(dir_n)
               Q_new_ac = reward[idx] + self.gamma+torch.max(ac_n)

            dir_target[idx][torch.argmax(direction).item()] = Q_new_dir
            ac_target[idx][torch.argmax(action).item()] = Q_new_ac

        self.optimizer.zero_grad()

        loss=0
        loss1 = self.criterion(dir_target, dir)
        print('loss1',loss1)
        loss2 = self.criterion(ac_target, ac )
        print('loss2',loss2)
        loss = loss1+loss2
        print('loss',loss)
        loss.backward()

        self.optimizer.step()