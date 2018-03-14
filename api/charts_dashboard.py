from flask import request, jsonify
from flask_cors import cross_origin
from flask_jsondash.charts_builder import charts

import controller


def init(app):
    # Config
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
        return 'anonymous'

    # Config examples.
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


# TODO
def register_charts_line_endpoint(app):
    @cross_origin()
    @app.route('/line')
    def linechart():
        """Fake endpoint."""

        all_data = controller.get_all_bins_data()
        data_dict = {}
        # for data in all_data:
        #     data['U_ID'] not in data_dict

        return jsonify({
            "line1": [1, 4, 3, 10, 12, 14, 18, 10],
            "line2": [1, 2, 10, 20, 30, 6, 10, 12, 18, 2],
        })
