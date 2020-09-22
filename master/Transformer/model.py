#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import torch
import pandas as pd
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import time
from sklearn.preprocessing import MultiLabelBinarizer
import copy


# In[2]:


device = torch.device('cuda:0')


# ## Dataset

# Custom dataset to load patient data from csv files

# In[3]:


padding_value = 0

class CustomDataset(Dataset):
    def __init__(self, root_dir, ids, diag_vocab, max_visits, max_diag):
        '''
        Args:
        root_dir (string): Path to csv directory
        ids (string): Path to csv file containing list of patient ids for training/testing
        diag_vocab (string): Path to csv file containing all diagnose labels
        max_visits (int): Maximum number of visits
        max_diag (int): Maximum number of diagnoses per visit that are considered
        Outputs:
        inputs (torch.tensor): Concatenated info of diagnoses and times between visits (batch_size, max_visits, vocab_size+1)
        labels (torch.tensor): Labels for visits
        '''
        self.root = root_dir #/home/afohr/data/stroke_binary
        self.ids = pd.read_csv(ids,dtype=str) #/home/afohr/data/pat_ids_stroke.csv
        #make vocabulary for diagnoses
        self.word2idx = self.indexify_vocab(pd.read_csv('/home/afohr/data/diag_vocab.csv')) #/home/afohr/data/diag_vocab.csv
        self.max_visits = max_visits
        self.max_diag = max_diag
    
    def __len__(self):
        return len(self.ids)
    
    def __getitem__(self, idx):
        #load patient data
        file_name = self.root + '/patient_' + self.ids.iloc[idx,0] + '.csv'
        patient = pd.read_csv(file_name, parse_dates=[1], converters = {'diag': lambda x: x.strip('[]').replace("'","").replace("\"","").split(', ')}) 
        #take only visits before 2013-01-01
        patient = patient.loc[patient.date <  np.datetime64('2013-01-01')]
        #take only last 100 visits
        patient=patient.tail(self.max_visits)
        #patient contains columns [id,date,age,sex,f_id,m_id,diag,delta_t,label]
        
        label = patient.label.to_list()[0] # 0 or 1
        # transform visit's diagnoses into indexes in vocabulary
        diag = self.transform_diag(patient.diag) #(max_diag, max_visits)
        delta_t = np.nan_to_num(patient.delta_t.to_numpy()).reshape(len(patient),1) #(n_visits_before/max_visits,1)
        mask = np.concatenate((np.full((len(patient)), 0), np.full((100-len(patient)), 1) ))
        
        #check if needs padding
        if len(patient) < self.max_visits:
            delta_t = np.concatenate((delta_t, np.full((100-len(patient),1), padding_value))) #(max_visits, 1)
        
        return torch.from_numpy(diag).to(device), torch.from_numpy(delta_t).to(device), torch.tensor(label).to(device), torch.from_numpy(mask).bool().to(device)
    
    def indexify_vocab(self, vocab):
        '''
        Arg:
        vocab (pandas.dataframe): Contains all diagnoses
        Return: 
        word2idx (dictionary): Diagnoses linked with unique index
        '''
        word2idx = {}
        word2idx['pad_val'] = 0
        values=vocab.values
        for i in range(len(vocab)):
            word2idx[values[i][0]] = i+1
        return word2idx
    
    def transform_diag(self, patient):
        '''
        Arg:
        patient (pandas.Series): Contains diagnoses of patients visits
        Return:
        ret (numpy.array): Indexes of diagnoses of all the visits (max_diag, max_visits) 
        '''
        ret = np.full((self.max_diag, self.max_visits), padding_value) 
        for i in range(len(patient)):
            for j in range(len(patient.values[i])):
                if j==self.max_diag:
                    break
                ret[j,i] = self.word2idx[patient.values[i][j]]
        return ret


# ## Embedding

# In[4]:


class Embedding(nn.Module):
    def __init__(self, vocab_size, max_visits, emb_dim):
        """
        vocab_size (int): Number of unique diagnoses
        max_visits (int): Maximum number of visits
        emb_dim (int): Embedding dimension
        """
        super(Embedding, self).__init__()
        self.emb_diag = nn.Embedding(vocab_size, emb_dim, padding_idx=0)
        self.emb_pos = nn.Embedding(max_visits, emb_dim)

    def forward(self, x):
        """
        Args:
        x = inputs shape (batch_size, max_diag, max_visits)
        Returns:
        emb =embedded shape (max_visits, batch_size, emb_dim)
        """
        pos = torch.arange(x.shape[-1], device=device) #(max_visits)
        pos = pos.repeat(x.shape[0],1)#(batch_size, max_visits)
        pos_emb = self.emb_pos(pos)#(batch_size, max_visits, emb_dim)
        
        emb = self.emb_diag(x) #(batch_size, max_diag, max_visits, embedded_dimension)
        emb = emb.sum(axis=1) #(batch_size, max_visits, embedded_dimension)
        emb = emb + pos_emb
        emb = emb.transpose(0,1) #(max_visits, batch_size, embedded_dim)
        return emb


# ## Encoder block

# In[5]:


class EncoderBlock(nn.Module):
    def __init__(self, emb_dim, n_heads, n_hidden=64, dropout=0.1):
        """
        emb_dim (int): Number of input and output features (embedding_dim)
        n_heads (int): Number of attention heads in the Multi-Head Attention
        n_hidden (int): Number of hidden units in the Feedforward (MLP) block
        dropout: Dropout rate after the first layer of the MLP and the two skip connections.
        """
        super(EncoderBlock, self).__init__()
        self.mh_att = nn.MultiheadAttention(emb_dim, n_heads) #(inputs of shape (max_visits, batch_size, embed_dim))
        self.feed1 = nn.Linear(emb_dim, n_hidden)
        self.feed2 = nn.Linear(n_hidden, emb_dim)
        self.norm1 = nn.LayerNorm(emb_dim)
        self.norm2 = nn.LayerNorm(emb_dim)
        self.drop1 = nn.Dropout(dropout)
        self.drop2 = nn.Dropout(dropout)

    def forward(self, x, mask):
        """
        Args:
        x = inputs shape (max_visits, batch_size, emb_dim)
        mask = Boolean tensor indicating which visits should be ignored shape (batch_size, max_visits)
        
        Returns:
        z = encoded inputs shape (max_visits, batch_size, emb_dim)
        """
        x = self.norm1(x + self.drop1(self.mh_att(x, x, x, mask)[0]))
        x = self.norm2(x + self.drop2(self.feed2(F.relu(self.feed1(x)))))
        return x


# ## Encoder

# global average pooling pools visits (batch, visit, emb) -> (batch, emb)

# In[6]:


class Encoder(nn.Module):
    def __init__(self, vocab_size, max_visits, n_blocks, emb_dim, n_heads, n_hidden1=64, n_hidden2=100, dropout=0.1):
        """
        Args:
        vocab_size (int): Number of words in vocabulary.
        max_visits (int): Number of maximum visits. 
        n_blocks (int): Number of EncoderBlock blocks.
        emb_dim (int): Number of embedding dimensions.
        n_heads (int): Number of attention heads inside the EncoderBlock.
        n_hidden1 (int): Number of hidden units in the Feedforward block of EncoderBlock.
        n_hidden2 (int): Number of hidden units in the Linear layer.
        dropout (float): Dropout level used in EncoderBlock and Encoder.
        Returns:
        embedded (float): Probabilities of having and not having stroke
        """
        # YOUR CODE HERE
        super(Encoder, self).__init__()
        self.emb = Embedding(vocab_size, max_visits, emb_dim)
        self.blocks = nn.ModuleList([EncoderBlock(emb_dim + 1, n_heads, n_hidden1, dropout) for _ in range(n_blocks)])
        self.lin1 = nn.Linear(emb_dim + 1, n_hidden2)
        self.lin2 = nn.Linear(n_hidden2, 2)
        self.drop1 = nn.Dropout(dropout)
        self.drop2 = nn.Dropout(dropout)

    def forward(self, x, delta_times, mask):
        """
        Args:
        x of shape (batch_size, max_diag, max_visits): LongTensor with the input sequences.
        delta_times of shape (batch_size, max_visits, 1)
        mask of shape (batch_size, max_seq_length): BoolTensor indicating which elements should be ignored.
        Returns:
        z of shape (max_seq_length, batch_size, n_features): Encoded input sequence.
        """
        embedded = self.emb(x) #shape (max_visits, batch_size, emb_dim)
        #add delta times
        embedded = torch.cat((embedded, delta_times.transpose(0,1)), 2) #shape (max_visits, batch_size, emb_dim+1)
        for layer in self.blocks:
            embedded = layer(embedded, mask) #(max_visits, batch_size, emb_dim)
        #global average pooling (reduces the max_visits dimension)
        embedded = self.drop1(embedded.mean(dim = 0)) #shape (batch_size, emb_dim)
        embedded = self.drop2(F.relu(self.lin1(embedded))) #shape (batch_size, n_hidden2)
        embedded = F.log_softmax(self.lin2(embedded), dim=1) #returns log probablities of binary prediction
        return embedded


# In[ ]:





# In[ ]:





# # test forward

# In[7]:


ds = CustomDataset("/home/afohr/data/stroke_binary", "/home/afohr/data/pat_ids_stroke.csv", "/home/afohr/data/diag_vocab.csv", 100, 6)


# ## Training

# In[8]:


device


# In[9]:


encoder = Encoder(5012, 100, 6, 127, 4)
encoder.to(device)


# In[10]:


parameters = encoder.parameters()
optimizer = torch.optim.Adam(parameters, lr=0.001)


# ### Split into train and test datasets. Used seed 42 so the datasets are reproducibles.

# In[11]:


test, train = torch.utils.data.random_split(ds, [round(4181297*0.2), round(4181297*0.8)], generator=torch.Generator().manual_seed(42))


# In[12]:


trainloader = DataLoader(dataset=train, batch_size=128, shuffle=True)


# ### make training loop

# 40 epochs or early stopping

# In[13]:


criterion = nn.NLLLoss(ignore_index=padding_value)
train_losses=[]
for e in range(20):
    start= time.time()
    for i, data in enumerate(trainloader):
        diags, delta_ts, labels, masks = data
        
        optimizer.zero_grad()
        
        outputs = encoder(diags, delta_ts.type('torch.cuda.FloatTensor'), masks) # returns log probablities of binary prediction, shape(batch_size, 2) 
        loss = criterion(outputs, labels) #labels, shape(batch_size, 1)
        loss.backward()
        
        optimizer.step()
        train_losses.append(loss.item())
        
        if i%99==1:
            print("Epoch: %d.Epoch Step: %d Loss: %f" %(e, i, np.average(train_losses)))
            train_losses=[]
            print(time.time()-start)


# batch 32, 992 batches took 167,34 sec 

# batch 128, 101 batches took 58,05 sec, 40 batches would take 166 hours. 7 days. early stopping. uses 10% vram.

# batch 256, 101 batches took 124.5 sec, 40 batches would take 178.5 hours. 7.4 days. early stopping. uses 10% vram.

# In[ ]:


torch.save(encoder.state_dict(), '/home/afohr/encoder1.pth')


# In[ ]:




