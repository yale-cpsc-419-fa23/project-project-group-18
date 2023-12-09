
import argparse
from api_services import socketio, app

def get_args():
    """Parse arguments from command line input"""
    parser = argparse.ArgumentParser(description='InstaGame 2023.'
                                     , allow_abbrev=False)
    parser.add_argument('port', type=int,
                        help='the port at which the server should listen')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    port = args.port
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
