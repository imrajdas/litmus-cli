import sys
import os, platform
import json
from prettytable import PrettyTable
import yaml
from helpers import inject

if platform.system() == "Windows":
    import msvcrt

def version():
    os.system(""" echo $(curl -s https://api.github.com/repos/litmuschaos/litmus/releases/latest | grep tag_name | cut -d '"' -f 4) """)

def install():
    os.system("""
        # CLUSTER_STATUS=$(kubectl version --short)
        # if [[ "$CLUSTER_STATUS" =~ ^Unable to connect to the server* ]]; then
        #     echo "hi"
        # fi

        kubectl apply -f https://litmuschaos.github.io/pages/litmus-operator-latest.yaml
    """)

def list_experiments():
    with open('experiments.json') as f:
        data = json.load(f)

    table = PrettyTable(['Chaos name', 'Chaos Description'])
    for exp in data['experiments']:
        table.add_row([exp['name'], exp['description']])

    print(table)

def help():
    help = """Chaos Engineering for Kubernetes
Usage:
litmus [command]

Available Commands:
install           Install all dependencies for using Litmus Chaos
experiments       Prints list of available experiments
version           Print the version of LitmusChaos
clean             Delete all dependencies related to litmus 
inject            Inject Chaos

Flags:
-h, --help   help for litmuschaos

Use "litmus [command] --help" for more information about a command.
    """
    print(help)


for arg in sys.argv:
    # print(arg)
    if (arg == "version"): version()
    elif (arg == "install"): install()
    elif (arg == "experiments"): list_experiments()
    elif (arg == "-h" or  arg == "--help"): help()
    elif (arg == "inject"): inject.inject()
    else: help