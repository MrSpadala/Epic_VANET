
def get_largest_conn_component(cars):
	plates_to_cars = {car.plate: car for car in cars}
	
	components = []
	all_visited_cars = set()
	for car in plates_to_cars.keys():
		if not car in all_visited_cars:
			visited = set([car])
			_dfs(plates_to_cars[car], visited, plates_to_cars)
			all_visited_cars = all_visited_cars.union(visited)
			components.append(visited)

	max_c = max(components, key=lambda x: len(x))   #get biggest connected component
	return [plates_to_cars[plate] for plate in max_c if plate in plates_to_cars]  #return biggest connected component expressed as list of car objects


def _dfs(curr_car, visited, plates_to_cars):
	for c, i in zip(curr_car.adj, range(len(curr_car.adj))):
		if c == 1 and (not i in visited) and (i in plates_to_cars):
			visited.add(i)
			new_car = plates_to_cars[i]
			_dfs(new_car, visited, plates_to_cars)
