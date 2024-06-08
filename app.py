from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# set your own database
db = "dbname='test' user='postgres' host='127.0.0.1' password = '123'"
conn = psycopg2.connect(db)

@app.route('/')
def hello():
    return "Hello World!"

def select_problems(tags, rating_lower_bound, rating_upper_bound):
    cur = conn.cursor()
    sql = "SELECT id, name, rating FROM problems"
    constraints = []
    if rating_upper_bound:
        constraints.append(f"rating <= {rating_upper_bound}")
    if rating_lower_bound:
        constraints.append(f"rating >= {rating_lower_bound}")
    if tags:
        con = "tag IN (" + ', '.join(f"\'{tag}\'" for tag in tags) + f") GROUP BY id HAVING COUNT (DISTINCT tag) = {len(tags)}"
        constraints.append(con)
    if constraints:
        sql += " WHERE " + " AND ".join(constraints)
    print(sql)
    cur.execute(sql)
    problems = Problem(cur.fetchall())
    cur.close()

    return problems

class Problem:
    def __init__(self, id, rating, name):
        self.name = name
        self.rating = rating
        self.id = id

@app.route('/problems/')
def problem_list():
    problems = select_problems(["fft", "binary search"], 3000, 3500)
    return render_template('index.html', problems=problems)

if __name__ == "__main__":
    app.run(debug=True, port=7000)