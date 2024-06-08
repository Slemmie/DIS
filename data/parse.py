import json

with open("problems.json") as f:
	data = json.load(f)

problems = data["result"]["problems"]

problem_entries = []
for problem in problems:
	problem_entry = {
		"contestId": problem.get("contestId"),
		"index": problem.get("index"),
		"name": problem.get("name"),
		"type": problem.get("type"),
		"points": problem.get("points"),
		"rating": problem.get("rating"),
		"tags": problem.get("tags"),
	}
	problem_entries.append(problem_entry)

problems_inserted = 0
problems_skipped = 0
num_entries = 0

exists = set()

with open("problems.sql", "w") as f:
	f.write("DROP TABLE IF EXISTS problems;\n\n")
	f.write("CREATE TABLE problems (\n")
	f.write("\ttag VARCHAR(255) NOT NULL,\n")
	f.write("\tid VARCHAR(255) NOT NULL,\n")
	f.write("\trating INTEGER,\n")
	f.write("\tname VARCHAR(255) NOT NULL,\n")
	f.write("\tPRIMARY KEY (tag, id)\n")
	f.write(");\n\n")
	insert_str = ""
	for problem in problem_entries:
		if problem["contestId"] and problem["index"] and problem["rating"] and problem["name"] and problem["tags"]:
			problems_inserted += 1
			ID = f"{problem['contestId']}{problem['index']}"
			name = problem["name"].replace("'", "''")
			for tag in problem["tags"]:
				if (tag, ID) in exists:
					continue
				exists.add((tag, ID))
				insert_str += f"('{tag}', '{ID}', {problem['rating']}, '{name}'),\n"
				num_entries += 1
		else:
			problems_skipped += 1
	f.write(f"INSERT INTO problems (tag, id, rating, name) VALUES\n{insert_str[:-2]};\n")

print("done")
print(f"inserted {problems_inserted} problems")
print(f"skipped {problems_skipped} problems due to missing data")
print(f"inserted {num_entries} entries in total")
