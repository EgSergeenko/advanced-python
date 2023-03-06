import ast
import uuid
from typing import Any

import networkx as nx


class GraphVisitor(ast.NodeVisitor):
    def __init__(self, user_color_map: dict | None = None) -> None:
        super().__init__()
        self.color_map = {
            'Assign': 'lightpink',
            'BinOp': 'lightyellow',
            'Call': 'lightseagreen',
            'Constant': 'lightgreen',
            'For': 'lightcyan',
            'FunctionDef': 'bisque',
            'Name': 'lightskyblue',
            'Tuple': 'lightgray',
            'Yield': 'aquamarine',
        }
        if user_color_map is not None:
            self.color_map.update(user_color_map)
        self.graph = nx.DiGraph()
        self.graph.graph['node'] = {'shape': 'rectangle'}

    def draw_graph(self, output_path: str) -> None:
        agraph = nx.drawing.nx_agraph.to_agraph(self.graph)
        agraph.layout('dot')
        agraph.draw(output_path)

    def visit_Add(self, node: ast.Add) -> str:
        return '+'

    def visit_Assign(self, node: ast.Assign) -> uuid.UUID:
        node_id = self._add_node('assign', self._get_color(node))
        self._add_edge(node_id, 'target', *node.targets)
        self._add_edge(node_id, 'value', node.value)
        return node_id

    def visit_BinOp(self, node: ast.BinOp) -> uuid.UUID:
        node_id = self._add_node(
            'operation: {0}'.format(self.visit(node.op)),
            self._get_color(node),
        )
        self._add_edge(node_id, 'left', node.left)
        self._add_edge(node_id, 'right', node.right)
        return node_id

    def visit_Call(self, node: ast.Call) -> uuid.UUID:
        node_id = self._add_node('call', self._get_color(node))
        self._add_edge(node_id, 'func', node.func)
        self._add_edge(node_id, '*args', *node.args)
        self._add_edge(node_id, '**kwargs', *node.keywords)
        return node_id

    def visit_Constant(self, node: ast.Constant) -> uuid.UUID:
        return self._add_node(
            'constant\nvalue: {0}'.format(node.value),
            self._get_color(node),
        )

    def visit_Expr(self, node: ast.Expr) -> Any:
        return self.visit(node.value)

    def visit_For(self, node: ast.For) -> uuid.UUID:
        node_id = self._add_node('for', self._get_color(node))
        self._add_edge(node_id, 'target', node.target)
        self._add_edge(node_id, 'iter', node.iter)
        self._add_edge(node_id, 'body', *node.body)
        return node_id

    def visit_FunctionDef(self, node: ast.FunctionDef) -> uuid.UUID:
        node_id = self._add_node(
            'function\nname: {0}'.format(node.name),
            self._get_color(node),
        )
        self._add_edge(node_id, 'body', *node.body)
        return node_id

    def visit_Name(self, node: ast.Name) -> uuid.UUID:
        return self._add_node(
            'variable\nname: {0}'.format(node.id),
            self._get_color(node),
        )

    def visit_Tuple(self, node: ast.Tuple) -> uuid.UUID:
        node_id = self._add_node('tuple', self._get_color(node))
        self._add_edge(node_id, 'item', *node.elts)
        return node_id

    def visit_Yield(self, node: ast.Yield) -> uuid.UUID:
        node_id = self._add_node('yield', self._get_color(node))
        if node.value is not None:
            self._add_edge(node_id, 'value', node.value)
        return node_id

    def _add_edge(
        self, src_node_id: uuid.UUID, label: str, *dst_nodes: ast.AST,
    ) -> None:
        dst_node_ids = [self.visit(dst_node) for dst_node in dst_nodes]
        for dst_node_id in dst_node_ids:
            if dst_node_id is not None:
                self.graph.add_edge(src_node_id, dst_node_id, label=label)

    def _add_node(self, label: str, color: str) -> uuid.UUID:
        node_id = uuid.uuid4()
        self.graph.add_node(
            node_id, label=label, style='filled', fillcolor=color,
        )
        return node_id

    def _get_color(self, node):
        node_type = type(node).__name__
        return self.color_map.get(node_type, 'white')


if __name__ == '__main__':
    with open('fib.py') as code_file:
        ast_object = ast.parse(code_file.read())
    visitor = GraphVisitor()
    visitor.visit(ast_object)
    visitor.draw_graph('artifacts/output.png')
