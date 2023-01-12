from flask import render_template, url_for, request, current_app, g, redirect
from app.models import Artobject
from app.main import bp
from app.main.forms import SearchForm

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Home')

@bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    objects = Artobject.query.order_by(Artobject.id.asc()).paginate(
        page, current_app.config['OBJECTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=objects.next_num) \
        if objects.has_next else None
    prev_url = url_for('main.explore', page=objects.prev_num) \
        if objects.has_prev else None
    return render_template('index.html', title='Explore', objects=objects.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    objects, total = Artobject.search(g.search_form.q.data, page,
                                      current_app.config['OBJECTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['OBJECTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page -1) \
        if page > 1 else None
    return render_template('search.html', title='Zoeken', objects=objects,
                           next_url=next_url, prev_url=prev_url)

