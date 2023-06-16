import requests

controller_ip = "controller_ip"
controller_port = "controller_port"

def learn_services():
    response = requests.get(f"http://{controller_ip}:{controller_port}/api/services")
    if response.status_code == 200:
        service_list = response.json()
        print("Services responsible for layer2/layer3 forwarding:")
        for service in service_list:
            print(service)

def deactivate_existing_service():
    response = requests.get(f"http://{controller_ip}:{controller_port}/api/existing-service")
    if response.status_code == 200:
        existing_service_id = response.json()["id"]
        response = requests.post(f"http://{controller_ip}:{controller_port}/api/services/{existing_service_id}/deactivate")
        if response.status_code == 200:
            print(f"Service {existing_service_id} deactivated successfully.")
        else:
            print(f"Failed to deactivate service {existing_service_id}.")
    else:
        print("No existing service found.")

def activate_service(service_id):
    response = requests.post(f"http://{controller_ip}:{controller_port}/api/services/{service_id}/activate")
    if response.status_code == 200:
        print(f"Service {service_id} activated successfully.")
    else:
        print(f"Failed to activate service {service_id}.")

def get_packet_count(switch):
    response = requests.get(f"http://{controller_ip}:{controller_port}/api/switches/{switch}/packet-count")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve packet count for switch {switch}.")
        return None

def calculate_intensity(pc_t, pc_t_plus_1):
    return (pc_t_plus_1 - pc_t) / (t_plus_1 - t)

def find_shortest_path():
    switches = get_switches()
    packet_counts = {switch: get_packet_count(switch) for switch in switches}
    intensities = {switch: calculate_intensity(packet_count['t'], packet_count['t+1']) for switch, packet_count in packet_counts.items()}
    max_intensity_switch = max(intensities, key=intensities.get)
    shortest_path = dijkstra_shortest_path(max_intensity_switch)
    return shortest_path

def dijkstra_shortest_path(start_switch):
    distances = {switch: float('inf') for switch in switches}
    distances[start_switch] = 0
    previous = {switch: None for switch in switches}
    visited = set()
    heap = [(0, start_switch)]

    while heap:
        current_distance, current_switch = heapq.heappop(heap)
        if current_switch in visited:
            continue
        visited.add(current_switch)
        neighbors = get_neighbors(current_switch)
        for neighbor in neighbors:
            neighbor_distance = current_distance + get_distance(current_switch, neighbor)
            if neighbor_distance < distances[neighbor]:
                distances[neighbor] = neighbor_distance
                previous[neighbor] = current_switch
                heapq.heappush(heap, (neighbor_distance, neighbor))

    shortest_path = []
    switch = switches[-1]
    while switch:
        shortest_path.append(switch)
        switch = previous[switch]

    shortest_path.reverse()
    return shortest_path

def get_neighbors(switch):
    response = requests.get(f"http://{controller_ip}:{controller_port}/api/switches/{switch}/neighbors")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve neighbors for switch {switch}.")
        return []

def get_distance(switch1, switch2):
    response = requests.get(f"http://{controller_ip}:{controller_port}/api/switches/{switch1}/distance/{switch2}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve distance between switch {switch1} and {switch2}.")
        return float('inf')

def embed_flow_rules(shortest_path):
    for i in range(len(shortest_path) - 1):
        switch1 = shortest_path[i]
        switch2 = shortest_path[i + 1]
        add_flow_rule(switch1, switch2)

def add_flow_rule(switch, output_port):
    payload = {
        "switch_id": switch,
        "priority": 1,
        "match": "any",
        "actions": f"output:{output_port}"
    }
    response = requests.post(f"http://{controller_ip}:{controller_port}/api/flow-rules", json=payload)
    if response.status_code == 201:
        print(f"Flow rule added successfully to switch {switch}.")
    else:
        print(f"Failed to add flow rule to switch {switch}.")

def main():
    learn_services()
    deactivate_existing_service()
    shortest_path = find_shortest_path()
    embed_flow_rules(shortest_path)

if __name__ == "__main__":
    main()
