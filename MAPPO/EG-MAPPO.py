import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class EG_GATLayer(nn.Module):
    def __init__(self, in_dim, out_dim, edge_dim, n_heads, use_edge, use_gate):
        super().__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.edge_dim = edge_dim
        self.n_heads = n_heads
        self.use_edge = use_edge
        self.use_gate = use_gate
        self.W_node = nn.Parameter(torch.Tensor(n_heads, in_dim, out_dim))
        self.W_edge = nn.Parameter(torch.Tensor(n_heads, edge_dim, out_dim)) if use_edge else None






class EG_GATEncoder(nn.Module):
    def __init__(self, node_dim, edge_dim, embed_dim, n_heads, n_layers, use_edge, use_gate):
        super().__init__()
        self.init_proj = nn.Linear(node_dim, embed_dim)
        self.layers = nn.ModuleList(
            [EG_GATLayer(embed_dim, embed_dim, edge_dim, n_heads, use_edge, use_gate) for _ in range(n_layers)]
        )

    def forward(self, node_features, edge_features):
        x = self.init_proj(node_features)
        for layer in self.layers:
            x = F.elu(layer(x, edge_features))
        return x










class ActorWithGraph(nn.Module):
    def __init__(self, args, graph_embed_dim):
        super().__init__()
        input_dim = args.state_dim + graph_embed_dim
        hidden_sizes = args.hidden_sizes if args.hidden_sizes else [args.hidden_width, args.hidden_width]
        layer_sizes = [input_dim] + list(hidden_sizes)






class Critic(nn.Module):
    def __init__(self, args, graph_embed_dim):
        super().__init__()
        input_dim = args.state_dim * args.agent_number + graph_embed_dim
        hidden_sizes = args.hidden_sizes if args.hidden_sizes else [args.hidden_width, args.hidden_width]






 # -- The code is being updated...




        
