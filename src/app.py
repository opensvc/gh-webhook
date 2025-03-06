import logging
import os
import sys
import connexion


def main():
    extra_path = os.environ.get('EXTRA_LIB')
    branches = os.environ.get('BRANCHES', '(main)')
    release_branches = os.environ.get('RELEASE_BRANCHES', '(main)')

    logging.basicConfig(level=logging.INFO)

    if extra_path:
        sys.path.append(extra_path)
    logging.info('BRANCHES=%s', branches)
    logging.info('RELEASE_BRANCHES=%s', release_branches)

    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "127.0.0.1")

    app = connexion.App(__name__)
    apis = os.environ.get('APIS', os.path.join('swagger', 'github.yaml'))
    for api in apis.split():
        logging.info('adding api from %s', api)
        app.add_api(api, arguments={'branches': branches, 'release_branches': release_branches})

    logging.info(f'webhook-job app listen on {host}:{port}')
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
