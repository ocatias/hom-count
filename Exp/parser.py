"""
Helper functions that do argument parsing for experiments.
"""

import argparse
import yaml
import sys
from copy import deepcopy

def parse_args(passed_args=None):
    """
    Parse command line arguments. Allows either a config file (via "--config path/to/config.yaml")
    or for all parameters to be set directly.
    A combination of these is NOT allowed.
    Partially from: https://github.com/twitter-research/cwn/blob/main/exp/parser.py
    """

    parser = argparse.ArgumentParser(description='An experiment.')

    # Config file to load
    parser.add_argument('--config', dest='config_file', type=argparse.FileType(mode='r'),
                        help='Path to a config file that should be used for this experiment. '
                        + 'CANNOT be combined with explicit arguments')

    parser.add_argument('--tracking', type=int, default=1,
                        help='If 0 runs without tracking')


    # Parameters to be set directly
    parser.add_argument('--seed', type=int, default=42,
                        help='random seed to set (default: 42)')
    parser.add_argument('--split', type=int, default=0,
                        help='split for cross validation (default: 0)')
    parser.add_argument('--dataset', type=str, default="ZINC",
                            help='dataset name (default: ZINC)')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='learning rate (default: 0.001)')
    parser.add_argument('--lr2', type=float, default=0.0001,
                        help='learning rate for finetuning with graph features(default: 0.0001)')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='input batch size for training (default: 32)')
    parser.add_argument('--epochs', type=int, default=100,
                        help='number of epochs to train (default: 100)')
    
    parser.add_argument('--max_params', type=int, default=1e9,
                        help='Maximum number of allowed model paramaters')
    
    parser.add_argument('--device', type=int, default=0,
                    help='which gpu to use if any (default: 0)')
    parser.add_argument('--model', type=str, default='GIN',
                    help='model, possible choices: default')
                    
    # LR SCHEDULER
    parser.add_argument('--lr_scheduler', type=str, default='ReduceLROnPlateau',
                    help='learning rate decay scheduler (default: ReduceLROnPlateau)')
    parser.add_argument('--lr_scheduler_decay_rate', type=float, default=0.5,
                        help='strength of lr decay (default: 0.5)')

    # For StepLR
    parser.add_argument('--lr_scheduler_decay_steps', type=int, default=50,
                        help='(StepLR) number of epochs between lr decay (default: 50)')

    # For ReduceLROnPlateau
    parser.add_argument('--min_lr', type=float, default=1e-5,
                        help='(ReduceLROnPlateau) min LR for `ReduceLROnPlateau` lr decay (default: 1e-5)')
    parser.add_argument('--lr_schedule_patience', type=int, default=10,
                        help='(ReduceLROnPlateau) number of epochs without improvement until the LR will be reduced')

    parser.add_argument('--max_time', type=float, default=12,
                        help='Max time (in hours) for one run')

    parser.add_argument('--drop_out', type=float, default=0.0,
                        help='dropout rate (default: 0.0)')
    parser.add_argument('--emb_dim', type=int, default=64,
                        help='dimensionality of hidden units in models (default: 64)')
    parser.add_argument('--num_layers', type=int, default=5,
                        help='number of message passing layers (default: 5)')
    parser.add_argument('--num_mlp_layers', type=int, default=1,
                        help='number of final mlp layers (default: 5)')
    parser.add_argument('--virtual_node', type=int, default=0,
                        help='virtual_node')

    parser.add_argument('--pooling', type=str, default="mean",
                        help='')
    parser.add_argument('--dim_pooling', type=int, default=0,
                        help='(needs cliques or rings)')
    parser.add_argument('--node_encoder', type=int, default=1,
                        help="Set to 0 to disable to node encoder")

    parser.add_argument('--graph_feat', type=str, default="",
                        help="Path to a file that contains the graph features.")
    parser.add_argument('--freeze_gnn', type=int, default=0,
                        help="Freeze GNN layers after training it.")
    parser.add_argument('--nr_graph_feat', type=int, default=0,
                        help='Number of graph features to use')
    
    parser.add_argument('--drop_feat', type=int, default=0,
                        help="Drop all features from the graph")
                    

    # Load partial args instead of command line args (if they are given)
    if passed_args is not None:
        # Transform dict to list of args
        list_args = []
        for key,value in passed_args.items():
            # The case with "" happens if we want to pass an argument that has no parameter
            list_args += [key, str(value)]

        args = parser.parse_args(list_args)
    else:
        args = parser.parse_args()

    args.__dict__["use_tracking"] = args.tracking == 1
    args.__dict__["use_virtual_node"] = args.virtual_node == 1
    args.__dict__["use_node_encoder"] = args.node_encoder == 1
    args.__dict__["do_freeze_gnn"] = args.freeze_gnn == 1
    args.__dict__["do_drop_feat"] = args.drop_feat == 1

    # https://codereview.stackexchange.com/a/79015
    # If a config file is provided, write it's values into the arguments
    if args.config_file:
        data = yaml.load(args.config_file)
        delattr(args, 'config_file')
        arg_dict = args.__dict__
        for key, value in data.items():
                arg_dict[key] = value

    return args
