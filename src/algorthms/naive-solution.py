def clarke_wright_savings(distance_matrix, customers, vehicle_capacity):
  num_customers = len(customers);
  savings = [];

  # Step 1: Calculate savings S(i,j) = d(0,i) + d(0,j) - d(i,j)
  for i in range(1, num_customers):
    for j in range(i + 1, num_customers):
      s_val = distance_matrix[0][i] + distance_matrix[0][j] - distance_matrix[i][j];
      savings.append({ 'pair': (i, j), 'saving': s_val });

  # Step 2: Sort savings in descending order
  savings.sort(key=lambda x: x['saving'], reverse=True);

  # Step 3: Initialize routes (each customer starts with their own route)
  routes = [[i] for i in range(1, num_customers)];

  for entry in savings:
    i, j = entry['pair'];
    # Logic to find which routes i and j belong to
    route_i = _.find(routes, lambda r: i in r);
    route_j = _.find(routes, lambda r: j in r);

    if route_i != route_j:
      # Check capacity and if they are at the ends of their respective routes
      total_demand = sum(customers[c].demand for c in route_i + route_j);
      if total_demand <= vehicle_capacity:
        # Merge routes based on connectivity logic
        if route_i[-1] == i and route_j[0] == j:
          route_i.extend(route_j);
          routes.remove(route_j);

  # Add depot (0) to start and end of all final routes
  final_routes = [[0] + r + [0] for r in routes];
  return final_routes;