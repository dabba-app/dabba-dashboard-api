from flask_jsondash.charts_builder import charts
from flask_cors import cross_origin
from flask import jsonify


def init(app):
    app.register_blueprint(charts)

    app.config.update(
        JSONDASH_FILTERUSERS=False,
        JSONDASH_GLOBALDASH=True,
        JSONDASH_GLOBAL_USER='global',
    )

    def _can_edit_global():
        return True

    def _can_delete():
        return True

    def _can_clone():
        return True

    def _get_username():
        return 'Team TeenLaddu'

    # Config
    app.config['JSONDASH'] = dict(
        metadata=dict(
            created_by=_get_username,
            username=_get_username,
        ),
        static=dict(
            js_path='js/vendor/',
            css_path='css/vendor/',
        ),
        auth=dict(
            edit_global=_can_edit_global,
            clone=_can_clone,
            delete=_can_delete,
        )
    )

    @cross_origin()
    @app.route('/test-chart')
    def c3ts():
        data = dict(
            x='x',
            xFormat='%Y%m%d',
            columns=[
                ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
                ['data1', 30, 200, 100, 400, 150, 2],
                ['data2', 130, 340, 200, 500, 250, 350]
            ]
        )
        return jsonify(dict(data=data))
