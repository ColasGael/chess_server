from argparse import ArgumentParser
import os.path

from chess_server.server import Server


def get_args():
    parser = ArgumentParser(description="Chess server")
    parser.add_argument(
        "--database_path",
        type=str,
        default="data/game_results.csv",
        help="Path to the CSV database file",
    )
    parser.add_argument(
        "--template_folder", type=str, default="templates", help="Path to the templates folder"
    )
    parser.add_argument("--host", type=str, help="Host IP address")
    parser.add_argument("--port", type=int, help="Port number")
    args = parser.parse_args()
    # Convert relative path to absolute path
    args.database_path = os.path.abspath(args.database_path)
    os.makedirs(os.path.dirname(args.database_path), exist_ok=True)
    args.template_folder = os.path.abspath(args.template_folder)
    return args


def main():
    args = get_args()
    server = Server(args.database_path, template_folder=args.template_folder)
    server.start(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
