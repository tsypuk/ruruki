from assertpy import assert_that
from behave import when, given, then
from ruruki.graphs import Graph

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


@given("we have a empty graph object")
def setup_empty_graph(context):
    """
    Setup a empty graph object and attach it to the context object for later.

    :param context: Context object share between all the setups.
    :type context: :class:`behave.runner.Context`
    """
    context.graph = Graph()


@given(u'we have a file object with the following dump content')
def create_dump_file_obj(context):
    """
    Create a file object containting the dumpt text specified in the
    step scenario and attach it to the context object for later use.

    :param context: Context object share between all the setups.
    :type context: :class:`behave.runner.Context`
    """
    context.dump_file = StringIO(context.text)


@when(u'we load the dump into the database')
def load_graph_dump_into_the_graph_obj(context):
    """
    Load the dump file into the graph object.

    :param context: Context object share between all the setups.
    :type context: :class:`behave.runner.Context`
    """
    context.graph.load(context.dump_file)


@when(u'we remove vertex "{text}"')
def remove_vertex_from_graph(context, text):
    v = context.graph.get_vertex(int(text))
    context.removed_vertex = v
    context.graph.remove_vertex(v)


@then(
    u'we expect the vertex "{text}" to be removed from the graph '
    'vertices entity set'
)
def check_vertex_is_not_in_graph_after_removal(context, text):
    v = context.removed_vertex
    assert_that(
        context.graph.get_vertices("facility").sorted()
    ).does_not_contain(v)


@then(u'we expect vertex "{text}" to be unbound')
def check_removed_vertex_is_nolonger_bound_to_the_graph(context, text):
    assert_that(context.removed_vertex.is_bound()).is_false()


@when(u'we add a new vertex with constraint uid "{text}"')
def add_new_vertext_with_constraint_of_deleted_vertex(context, text):
    v = context.graph.add_vertex("facility", uid=text)
    context.new_vertex = v


@then(u'we expect the vertex with id "{ident}" to be added with constraint uid "{text}"')
def step_impl(context, ident, text):
    ident = int(ident)
    assert_that(context.new_vertex.ident).is_equal_to(ident)
    assert_that(context.new_vertex.properties["uid"]).is_equal_to(text)


@then(u'when we try to add another vertex with uid "{text}" it raises a violation error')
def step_impl(context, text):
    err = None
    try:
        context.graph.add_vertex("facility", uid=text)
    except Exception as err:
        err = err
    assert_that(err.__class__.__name__).is_equal_to("ConstraintViolation")


@then(u'we expect to have "{count}" edge')
def check_edge_count(context, count):
    """
    Check the edge count in the graph object.

    :param context: Context object share between all the setups.
    :type context: :class:`behave.runner.Context`
    :param count: Expected edge count.
    :type count: :class:`int`
    """
    assert_that(context.graph.edges).is_length(int(count))


@then(u'the edges have')
def check_edge(context):
    """
    Check the edge has the correct data.

    :param context: Context object share between all the setups.
    :type context: :class:`behave.runner.Context`
    """
    for row in context.table:
        edge = context.graph.get_edge(int(row["ident"]))
        head = edge.head
        tail = edge.tail

        assert_that(edge.label).is_equal_to(row["label"])
        assert_that(edge.properties).is_equal_to(eval(row["properties"]))

        assert_that(head.ident).is_equal_to(int(row["head_ident"]))
        assert_that(tail.ident).is_equal_to(int(row["tail_ident"]))


@then(u'we expect to have "{count}" vertices')
def check_vertices_count(context, count):
    """
    Check the vertices count in the graph object.

    :param context: Context object share between all the setups.
    :type context: :class:`behave.runner.Context`
    :param count: Expected vertex count.
    :type count: :class:`int`
    """
    assert_that(context.graph.vertices).is_length(int(count))


@then(u'the vertices have')
def check_edge(context):
    """
    Check the vertex has the correct data.

    :param context: Context object share between all the setups.
    :type context: :class:`behave.runner.Context`
    """
    for row in context.table:
        vertex = context.graph.get_vertex(int(row["ident"]))
        assert_that(vertex.ident).is_equal_to(int(row["ident"]))
        assert_that(vertex.label).is_equal_to(row["label"])
        assert_that(vertex.properties).is_equal_to(eval(row["properties"]))


@when(u'we remove edge "{head_ident}"-["{label}"]->"{tail_ident}"')
def remove_edge(context, head_ident, label, tail_ident):
    e = context.graph.get_edge(0)
    context.graph.remove_edge(e)


@when(u'we add a new edge "{head_ident}"-["{label}"]->"{tail_ident}"')
def add_new_edge(context, head_ident, label, tail_ident):
    context.head = context.graph.get_vertex(int(head_ident))
    context.tail = context.graph.get_vertex(int(tail_ident))
    context.new_edge = context.graph.add_edge(context.head, label, context.tail)


@then(u'we expect the edge with id "{ident}", "{head_ident}"-["{label}"]->"{tail_ident}" to be added')
def check_new_edge_is_created(context, ident, head_ident, tail_ident, label):
    assert_that(context.new_edge.ident).is_equal_to(int(ident))
    assert_that(context.new_edge.label).is_equal_to(label)
    assert_that(context.new_edge.head.ident).is_equal_to(int(head_ident))
    assert_that(context.new_edge.tail.ident).is_equal_to(int(tail_ident))


@then(u'when we add a another edge "{head_ident}"-["{label}"]->"{tail_ident}"  it raises a violation error')
def step_impl(context, head_ident, label, tail_ident):
    err = None
    try:
        context.head = context.graph.get_vertex(int(head_ident))
        context.tail = context.graph.get_vertex(int(tail_ident))
        context.new_edge = context.graph.add_edge(context.head, label, context.tail)
    except Exception as err:
        err = err
    assert_that(err.__class__.__name__).is_equal_to("ConstraintViolation")

