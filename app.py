from flask import Flask, render_template, request
import psycopg2
import re
from config import db, port

app = Flask(__name__)

conn = psycopg2.connect(db)

def all_tags():
    cur = conn.cursor()
    sql = "SELECT DISTINCT tag FROM problems ORDER BY tag"
    cur.execute(sql)
    tags = cur.fetchall()
    cur.close()
    # Convert from 1-tuples to string
    return [tag[0] for tag in tags]

def select_problems(tags, rating_lower_bound, rating_upper_bound):
    cur = conn.cursor()
    sql = "SELECT DISTINCT name, id, rating FROM problems"
    constraints = []
    if rating_upper_bound:
        constraints.append(f"rating <= {rating_upper_bound}")
    if rating_lower_bound:
        constraints.append(f"rating >= {rating_lower_bound}")
    if tags:
        con = "tag IN (" + ', '.join(f"\'{tag}\'" for tag in tags) + f") GROUP BY name, id, rating HAVING COUNT (DISTINCT tag) = {len(tags)}"
        # fx "WHERE tag IN ('dp', 'math') GROUP BY name, id, rating HAVING COUNT (DISTINCT tag) = 2"
        constraints.append(con)
    if constraints:
        sql += " WHERE " + " AND ".join(constraints)
    cur.execute(sql)
    result = cur.fetchall()
    problems = [Problem(problem) for problem in result]
    cur.close()

    return problems

class Problem:
    def __init__(self, data):
        self.name = data[0]
        self.id = data[1]
        self.rating = data[2]
        letter_index = next(i for i, c in enumerate(self.id) if not c.isdigit())
        contest_id = self.id[:letter_index]
        index = self.id[letter_index:]
        self.link = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"

@app.route('/', methods=['GET'])
def problem_list():
    rating_lower_bound = request.args.get('rating_lower_bound', type=int)
    rating_upper_bound = request.args.get('rating_upper_bound', type=int)
    regex = request.args.get('regex', type=str)
    selected_tags = request.args.getlist('tags')
    problems = select_problems(selected_tags, rating_lower_bound, rating_upper_bound)
    regex_invalid = False
    if regex:
        try:
            problems = [problem for problem in problems if re.search(regex, problem.name)]
        except re.error:
            regex_invalid = True
    return render_template('index.html', problems=problems, possible_tags=all_tags(), regex_invalid=regex_invalid)

if __name__ == "__main__":
    app.run(debug=True, port=port)
