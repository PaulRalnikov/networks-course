import threading
import json
from collections import defaultdict

class Router:
    inf_metric = 16

    def __init__(self, ip, connections):
        self.ip = ip
        self.routing_table = defaultdict(lambda: {'next_hop': "--", 'metric': Router.inf_metric})
        self.connections = []
        for ip in connections:
            self.add_connection(ip)
        self.routing_table[self.ip]["next_hop"] = self.ip
        self.routing_table[self.ip]["metric"] = 0
        self.previous_step_updated_routers = dict()
        self.current_step_updated_routers = dict((neighbor_ip, 1) for neighbor_ip in self.connections)

    def add_connection(self, neighbor_ip):
        self.connections.append(neighbor_ip)
        # Initialize the routing table with direct connections
        self.routing_table[neighbor_ip]['next_hop'] = neighbor_ip
        self.routing_table[neighbor_ip]['metric'] = 1

    def update_routing_table(self, neighbor_ip, neighbor_routing_table):
        updated = False
        for dest_ip, info in neighbor_routing_table.items():
            new_metric = info['metric'] + 1
            if new_metric < self.routing_table[dest_ip]['metric']:
                self.routing_table[dest_ip]['next_hop'] = neighbor_ip
                self.routing_table[dest_ip]['metric'] = new_metric
                self.current_step_updated_routers[dest_ip] = new_metric
                updated = True
        return updated

    def print_routing_table(self, state_name : str):
        print(f"{state_name} of router {self.ip} table:")
        print(f"[Source IP]      [Destination IP]     [Next Hop]       [Metric]")
        for dest_ip, info in self.routing_table.items():
            print(f"{self.ip:<16} {dest_ip:<20} {info['next_hop']:<16} {info['metric']}")

    def go_to_next_step(self):
        self.previous_step_updated_routers = self.current_step_updated_routers.copy()
        self.current_step_updated_routers = dict()

    def send_messages(self, routers):
        if len(self.previous_step_updated_routers) == 0:
            return
        updated = False
        for neighbor_ip in self.connections:
            if routers[neighbor_ip].update_routing_table(self.ip, self.routing_table):
                updated = True
        return updated

def load_network_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)

step_num = 0

def make_step(routers):
    global step_num
    step_num += 1
    for router in routers.values():
        router.go_to_next_step()
    updated = False
    for router in routers.values():
        if router.send_messages(routers):
            updated = True
    print("=" * 100)
    for router in routers.values():
        router.print_routing_table(f"Simulation step {step_num}")
    return updated
def main():
    network_config = load_network_config('network.json')
    routers = {}

    # Create routers
    for router_info in network_config['routers']:
        router = Router(router_info['ip'], router_info['connections'])
        routers[router_info['ip']] = router

    for router in routers.values():
        router.print_routing_table("Initial state")

    while make_step(routers):
        pass


if __name__ == "__main__":
    main()
