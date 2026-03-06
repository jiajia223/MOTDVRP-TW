import torch
import numpy as np
def state_change(s,args):
    s_change_vt = [0 for i in range(args.action_dim + 2)]
    for x in s[0]:
        s_change_vt[x] = 1
    s_change_vt = torch.tensor(s_change_vt).to(device)
    s_rest = torch.tensor(s[1:]).to(device)  
    s_change = torch.cat((s_change_vt, s_rest), 0)
    return s_change
  
class ReplayBuffer:
    def __init__(self, args):
        self.args = args
        self.s = [None for _ in range(args.batch_size)]
        self.a = torch.zeros((args.batch_size, 2)).to(device)
        self.a_logprob = torch.zeros((args.batch_size, 1)).to(device)
        self.r = torch.zeros((args.batch_size, 1)).to(device)
        self.s_ = [None for _ in range(args.batch_size)]
        self.done = torch.zeros((args.batch_size, 1)).to(device)
        self.dw = torch.zeros((args.batch_size, 1)).to(device)
        self.mask = torch.zeros((args.batch_size, 2, args.action_dim + 1)).to(device)
        self.count = 0

    def store(self, s, a, a_logprob, r, s_,dw,done,mask):
            self.s[self.count] = s
            self.a[self.count] = torch.as_tensor(a, device=device)
            self.a_logprob[self.count] = torch.as_tensor(a_logprob, device=device)
            self.r[self.count] = torch.as_tensor(r, device=device)
            self.s_[self.count] = s_
            self.dw[self.count] = torch.as_tensor(dw, device=device)
            self.done[self.count] = torch.as_tensor(done, device=device)
            self.mask[self.count] = torch.as_tensor(mask, device=device)
            self.count += 1

    def numpy_to_tensor(self):
        if self.count == 0:
            s = torch.empty((0,))
            s_ = torch.empty((0,))
        else:
            if torch.is_tensor(self.s[0]):
                s = torch.stack(self.s[:self.count]).float().to(device)
            else:
                s = torch.stack([state_change(self.s[i], args=self.args) for i in range(self.count)]).float().to(device)
            if torch.is_tensor(self.s_[0]):
                s_ = torch.stack(self.s_[:self.count]).float().to(device)
            else:
                s_ = torch.stack([state_change(self.s_[i], args=self.args) for i in range(self.count)]).float().to(device)
        return s, a, a_logprob, r, s_, dw, done, mask
      # Other code is being updated。。。
