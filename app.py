from flask import Flask, render_template, request
import psycopg2
from config import db, port

app = Flask(__name__)

conn = psycopg2.connect(db)

@app.route('/')
def hello():
    return "Hello World!"

def select_problems(tags, rating_lower_bound, rating_upper_bound):
    cur = conn.cursor()
    sql = "SELECT name, id, rating FROM problems"
    constraints = []
    if rating_upper_bound:
        constraints.append(f"rating <= {rating_upper_bound}")
    if rating_lower_bound:
        constraints.append(f"rating >= {rating_lower_bound}")
    if tags:
        con = "tag IN (" + ', '.join(f"\'{tag}\'" for tag in tags) + f") GROUP BY name, id, rating HAVING COUNT (DISTINCT tag) = {len(tags)}"
        constraints.append(con)
    if constraints:
        sql += " WHERE " + " AND ".join(constraints)
    print(sql)
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

@app.route('/problems/', methods=['GET'])
def problem_list():
    rating_lower_bound = request.args.get('rating_lower_bound', type=int)
    rating_upper_bound = request.args.get('rating_upper_bound', type=int)
    problems = select_problems(["bitmasks", "greedy"], rating_lower_bound, rating_upper_bound)
    return render_template('index.html', problems=problems)

if __name__ == "__main__":
    app.run(debug=True, port=port)
