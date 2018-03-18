from flask_jsondash.charts_builder import charts


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
