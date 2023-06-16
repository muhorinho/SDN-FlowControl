import requests

# REST API Case: Send a GET request to retrieve the list of switches
def get_switches():
    response = requests.get("http://controller_ip:controller_port/api/switches")
    if response.status_code == 200:
        switches = response.json()
        return switches
    else:
        print("Failed to retrieve switches.")
        return None

# REST API Case: Send a POST request to add a flow rule
def add_flow_rule(switch_id, priority, match, actions):
    payload = {
        "switch_id": switch_id,
        "priority": priority,
        "match": match,
        "actions": actions
    }
    response = requests.post("http://controller_ip:controller_port/api/flow-rules", json=payload)
    if response.status_code == 201:
        print("Flow rule added successfully.")
    else:
        print("Failed to add flow rule.")

# REST API Case: Send a DELETE request to remove a flow rule
def remove_flow_rule(rule_id):
    url = f"http://controller_ip:controller_port/api/flow-rules/{rule_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        print("Flow rule removed successfully.")
    else:
        print("Failed to remove flow rule.")

# REST API Case: Send a GET request to retrieve network statistics
def get_network_statistics():
    response = requests.get("http://controller_ip:controller_port/api/network-statistics")
    if response.status_code == 200:
        statistics = response.json()
        return statistics
    else:
        print("Failed to retrieve network statistics.")
        return None

# Main function
def main():
    # Send a GET request to retrieve the list of switches
    switches = get_switches()
    if switches:
        print("Switches:")
        for switch in switches:
            print(switch)

    # Send a POST request to add a flow rule
    add_flow_rule("s1", 1, "00:00:00:00:00:01", "output:1")

    # Send a DELETE request to remove a flow rule
    remove_flow_rule("rule_id")

    # Send a GET request to retrieve network statistics
    statistics = get_network_statistics()
    if statistics:
        print("Network Statistics:")
        print(statistics)

if __name__ == "__main__":
    main()
