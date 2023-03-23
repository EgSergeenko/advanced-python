import ast
import operator
from typing import Any

from ast_graph_builder.graph_visitor import GraphVisitor


def get_block_start(block_name: str) -> str:
    return r'\begin{{{0}}}'.format(block_name)


def get_block_end(block_name: str) -> str:
    return r'\end{{{0}}}'.format(block_name)


def get_horizontal_line() -> str:
    return r'\hline'


def get_table_start(n_columns: int) -> str:
    table_start = get_block_start('tabular')
    n_columns = operator.add(n_columns, 1)
    alignment = ' c '.join(operator.mul(list('|'), n_columns))
    return operator.add(table_start, '{{ {0} }}'.format(alignment))


def get_table_row(data: list[Any]) -> str:
    row_values = ' & '.join(map(str, data))
    row_values = operator.add(row_values, r' \\ ')
    return operator.add(row_values, get_horizontal_line())


def generate_latex_table(data: list[list[Any]]) -> list[str]:
    return [
        get_table_start(len(data[0])),
        get_horizontal_line(),
        *list(map(get_table_row, data)),
        get_block_end('tabular'),
    ]


def generate_latex_image(
    image_path: str, caption: str, label: str,
) -> list[str]:
    return [
        get_block_start('figure'),
        r'\includegraphics[width=\linewidth]{{{0}}}'.format(image_path),
        r'\caption{{{0}}}'.format(caption),
        r'\label{{fig:{0}}}'.format(label),
        get_block_end('figure'),
    ]


if __name__ == '__main__':
    with open('fixtures/fib.py') as code_file:
        ast_object = ast.parse(code_file.read())
    visitor = GraphVisitor()
    visitor.visit(ast_object)
    visitor.draw_graph('fixtures/image.png')

    sample_data = [
        ['Node', 'Count'],
        ['Assign', 2],
        ['BinOp', 1],
        ['Call', 1],
        ['Constant', 2],
        ['For', 1],
        ['FunctionDef', 1],
        ['Name', 11],
        ['Tuple', 4],
        ['Yield', 1],
    ]

    lines = [
        r'\documentclass{article}',
        r'\usepackage{graphicx}',
        get_block_start('document'),
        get_block_start('center'),
        *generate_latex_table(sample_data),
        *generate_latex_image('fixtures/image.png', 'AST graph.', 'graph'),
        get_block_end('center'),
        get_block_end('document'),
    ]

    with open('artifacts/doc.tex', 'w') as tex_file:
        for line in lines:
            tex_file.write(line)
            tex_file.write('\n')
