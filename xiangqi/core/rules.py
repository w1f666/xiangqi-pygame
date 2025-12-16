from __future__ import annotations
from .board import Board
from .const import Side, Piece, i_to_rc, rc_to_i

def is_face_to_face(board: Board) -> bool:
    """将帅照面：同列无遮挡则为 True（非法/将军的一部分）。占位实现后面补。"""
    SHUAI = board.find_piece(+Piece.SHUAI)
    JIANG = board.find_piece(-Piece.SHUAI)
    if SHUAI is None or JIANG is None:
        return False
    r_s, c_s = i_to_rc(SHUAI)
    r_j, c_j = i_to_rc(JIANG)
    if c_s != c_j:
        return False
    for r in range(r_j + 1, r_s):
        if board.piece_at(rc_to_i(r, c_s)) != 0:
            return False
    return True

def in_check(board: Board, side: Side) -> bool:
    """side 方是否被将军。占位：后续实现（含照面）。"""
    # TODO: 需要对方的攻击走法判断（可用 movegen 的攻击判定或专用函数）

    return False

def is_checkmate(board: Board, side: Side, legal_moves_provider) -> bool:
    """side 方是否将死：被将军且无合法走法"""
    if not in_check(board, side):
        return False
    return len(legal_moves_provider(board, side)) == 0
