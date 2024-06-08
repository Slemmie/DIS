## Setup
1. Clone the repository, i.e. `$ git clone https://github.com/Slemmie/DIS.git`.
2. Install the required packages, i.e. `$ pip install -r requirements.txt`.
    - \[known issue\]: If the `psycopg2` package fails to install, try installing it manually with `$ pip install psycopg2-binary`.
3. Create a new database in PostgreSQL, fill out the information in `config.py`.
4. Run the `setup.py` script to automatically fill out the database with the data found in the `data` directory, i.e. `$ python3 setup.py`.
5. To launch the application, run `$ python3 app.py` in the terminal.
