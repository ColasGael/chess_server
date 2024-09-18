import csv
import os.path

import flask

from chess_server.elo_ranker import EloRanker
from chess_server.outcome import Outcome


class Server(object):
    """HTML server to record chess games' results"""

    __elo_ranker: EloRanker
    __database_path: str
    __app: flask.Flask

    def __init__(self, database_path: str, template_folder: str = "templates") -> None:
        self.__elo_ranker = EloRanker()
        self.__database_path = database_path
        if os.path.exists(self.__database_path):
            self.read_database()
        self.__app = flask.Flask(__package__, template_folder=template_folder)

    def read_database(self) -> None:
        """Load the past games' results from the database"""
        with open(self.__database_path, "r") as csvfile:
            csv_reader = csv.reader(csvfile)
            for line in csv_reader:
                self.__elo_ranker.update(*line)

    def update_database(self, *args) -> None:
        """Add a new game result to the database"""
        with open(self.__database_path, "a") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(args)

    def start(self) -> None:
        @self.__app.route("/", methods=["GET", "POST"])
        def home() -> str:
            """Home page of the server: display a form to record a new game result"""
            if flask.request.method == "POST":
                white_name = flask.request.form["white_name"]
                black_name = flask.request.form["black_name"]
                outcome_value = flask.request.form["outcome_value"]
                try:
                    self.__elo_ranker.update(white_name, black_name, outcome_value)
                except Exception as e:
                    return flask.render_template("error_page.html", error_msg=str(e))
                self.update_database(white_name, black_name, outcome_value)

            return flask.render_template(
                "game_result.html", players=self.__elo_ranker.players, outcomes=Outcome
            )

        @self.__app.route("/stats")
        def results() -> str:
            """Display the players' stats"""
            return flask.render_template("players_stats.html", players=self.__elo_ranker.players)

        self.__app.run()
